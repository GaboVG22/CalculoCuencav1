# Aplicación KMZ Hidrología de Cuencas v1.9

Aplicación Streamlit para análisis morfométrico, hidrológico, DGA/Verni-King, precipitación por isoyetas KMZ y módulo sedimentológico/detrítico.

## Deploy rápido en Streamlit Cloud

- Repository: `GaboVG22/KuenK_V1`
- Branch: `main`
- Main file path: `app.py`

## Cambios v1.9

- Periodos de retorno fijos: 2, 5, 10, 25, 50, 100 y 200 años.
- Presets DGA-AC y Verni-King recomendados por ubicación, pero editables y con opción manual.
- Factores T=200 precargados como referenciales/editables.
- Módulo detrítico con terreno tipo desfavorable por defecto y edición manual completa.

## Advertencia

Los coeficientes precargados son de apoyo para automatización y revisión técnica. Para diseño definitivo se debe confirmar cuenca oficial DGA, zona homogénea, precipitación de diseño, factores de frecuencia, coeficientes regionales y condiciones locales.


### Corrección v1.9

La carga de KMZ/KML de isoyetas fue reforzada para soportar KMZ con varios KML internos, líneas, polígonos, nombres tipo `P10D 60 mm`, y archivos grandes. Para mapas pesados, deje desactivada la opción **Mostrar isoyetas en el mapa**; la detección de P10D funciona igualmente.


## Nuevo en v1.9

Se validó la lectura del archivo DGA `Precipitaciones_Maxima_Diarias.kmz`. El parser reconoce valores numéricos en el nombre de la isoyeta y también en descripciones HTML tipo `VALOR_MM`. Además se incluye el KMZ DGA como base interna opcional para pruebas y automatización de P10D.


## Cambio v2.1
- La automatización de lluvia queda activa por defecto. Si se carga o usa KMZ de isoyetas, la aplicación genera P24 e IDF desde P10D + CD/CF/K sin requerir edición manual inicial.
