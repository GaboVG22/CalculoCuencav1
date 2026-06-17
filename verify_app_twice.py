"""Verificación funcional de la aplicación Streamlit.
Ejecuta la app dos veces en modo demo y valida que no existan errores/exceptiones.
"""
from streamlit.testing.v1 import AppTest

for i in range(1, 3):
    at = AppTest.from_file("app.py")
    at.run(timeout=45)
    if len(at.exception) > 0 or len(at.error) > 0:
        print(f"RUN {i}: ERROR")
        for e in at.exception:
            print("EXCEPTION:", e.value)
        for e in at.error:
            print("ERROR:", e.value)
        raise SystemExit(1)
    print(f"RUN {i}: OK | metrics={len(at.metric)} | dataframes={len(at.dataframe)} | warnings={len(at.warning)}")

print("Verificación completa: la app inicia dos veces sin errores en modo demo.")
