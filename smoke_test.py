from pathlib import Path
from zipfile import ZipFile
from shapely.geometry import Point
from src.hidro_kmz_core import (
    read_kmz_or_kml,
    parse_kml_features,
    classify_features,
    compute_basin_metrics,
    compute_contour_metrics,
    isohyet_features_from_kml,
    nearest_isohyet_to_point,
)

kmz = Path("data/Quebrada_Las_Cardas_2_1.kmz")
assert kmz.exists(), "No se encontró el KMZ de demostración"
text = read_kmz_or_kml(str(kmz))
features = parse_kml_features(text)
classes = classify_features(features)
assert classes["basin"] is not None, "No se detectó polígono de cuenca"
metrics = compute_basin_metrics(classes["basin"])
contours = compute_contour_metrics(classes["contours"])
assert metrics.area_km2 > 0, "Área inválida"
assert contours.n_contours > 0, "No se detectaron curvas de nivel"

# Prueba específica v1.8: KMZ/KML de isoyetas robusto.
iso_kml = '''<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2"><Document>
<Placemark><name>Isoyeta P10D 60 mm</name><LineString><coordinates>-71.1,-30.1,0 -71.0,-30.0,0</coordinates></LineString></Placemark>
<Placemark><name>Isoyeta_80</name><LineString><coordinates>-71.2,-30.1,0 -71.0,-29.9,0</coordinates></LineString></Placemark>
<Placemark><name>Band P24_10 75</name><Polygon><outerBoundaryIs><LinearRing><coordinates>-71.3,-30.2,0 -71.2,-30.2,0 -71.2,-30.1,0 -71.3,-30.1,0 -71.3,-30.2,0</coordinates></LinearRing></outerBoundaryIs></Polygon></Placemark>
</Document></kml>'''
iso_path = Path("outputs/test_iso_v18.kmz")
iso_path.parent.mkdir(exist_ok=True)
with ZipFile(iso_path, "w") as z:
    z.writestr("doc.kml", iso_kml)
iso_text = read_kmz_or_kml(str(iso_path))
isos = isohyet_features_from_kml(iso_text)
assert len(isos) == 3, "No se leyeron correctamente las isoyetas sintéticas"
vals = sorted(round(float(f.properties["p_mm"])) for f in isos)
assert vals == [60, 75, 80], f"Valores de isoyeta mal detectados: {vals}"
nearest = nearest_isohyet_to_point(isos, Point(-71.05, -30.05), 32719)
assert nearest["ok"] and round(nearest["p_mm"]) == 60, "No se detectó la isoyeta más cercana"

print("Smoke test OK")
print(f"Área demo: {metrics.area_km2:.2f} km2")
print(f"Curvas demo: {contours.n_contours}")

# Prueba v1.9: KMZ DGA real de precipitaciones máximas diarias.
real_iso_path = Path("data/Precipitaciones_Maxima_Diarias.kmz")
assert real_iso_path.exists(), "No se encontró el KMZ DGA de isoyetas incluido"
real_iso_text = read_kmz_or_kml(str(real_iso_path))
real_isos = isohyet_features_from_kml(real_iso_text)
assert len(real_isos) >= 200, f"Se esperaban más de 200 isoyetas DGA, se leyeron {len(real_isos)}"
real_vals = [float(f.properties.get("p_mm")) for f in real_isos if f.properties.get("p_mm") is not None]
assert len(real_vals) == len(real_isos), "No se detectó VALOR_MM o nombre numérico en todas las isoyetas DGA"
nearest_real = nearest_isohyet_to_point(real_isos, Point(metrics.centroid_lon, metrics.centroid_lat), metrics.epsg_utm)
assert nearest_real["ok"], "No se detectó la isoyeta DGA más cercana a Las Cardas"

print(f"Isoyetas test: {len(isos)} valores={vals}")
print(f"Isoyetas DGA reales: {len(real_isos)}; rango={min(real_vals):.0f}-{max(real_vals):.0f} mm; Las Cardas cercana={nearest_real['p_mm']:.0f} mm, dist={nearest_real['distance_m']:.0f} m")

# Prueba v2.0: KML con prefijo XML no declarado.
broken_kml = real_iso_text.replace(' xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"', '')
broken_isos = isohyet_features_from_kml(broken_kml)
assert len(broken_isos) == len(real_isos), "El reparador de prefijos XML no recuperó las isoyetas DGA"
print("Reparador XML prefijos: OK")
