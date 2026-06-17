# Aplicación KMZ Hidrología de Cuencas v1.2

Aplicación Streamlit para analizar una cuenca desde KMZ/KML, calcular parámetros morfométricos, leer curvas de nivel con cota Z, definir/dibujar cauce principal y punto de descarga, diagnosticar metodologías hidrológicas y generar una memoria técnica en Word.

## Novedades v1.2

- Sugerencia automática de punto de descarga desde la curva de nivel más baja que intersecta el borde de cuenca.
- Estimación preliminar automática del eje del cauce si no viene precargado ni dibujado.
- Detección preliminar de región/cuenca para Coquimbo y selección editable de preset regional.
- Presets editables para Verni-King y DGA-AC.
- DGA-AC con fórmula preliminar III-IV parametrizada: `Q10 = coef * A^a * P24_10^b` y conversión por `F_T` y `alpha_inst`.
- Verni-King con forma `Q = C(T) * 0,00618 * P24^1,24 * A^0,88`.
- Diagnóstico automático de inputs faltantes/completos.
- Cálculo simultáneo de Racional, Racional modificado, SCS-CN, HUS, Verni-King y DGA-AC cuando existan datos suficientes.
- Verificación automática con `verify_app_twice.py`.

## Ejecución local

```bash
python -m pip install -r requirements.txt
streamlit run app.py
```

## Despliegue en Streamlit Cloud

1. Subir todo el contenido de esta carpeta al repositorio GitHub.
2. En Streamlit Community Cloud seleccionar:
   - Repository: `usuario/repositorio`
   - Branch: `main`
   - Main file path: `app.py`
3. Presionar **Deploy**.

## Advertencia técnica

Los presets regionales incluidos son editables y sirven para automatizar la prueba de la aplicación. Antes de utilizar la memoria como documento de diseño, el especialista debe verificar la cuenca oficial, zona homogénea, precipitación de diseño, factores de frecuencia y coeficientes DGA/Verni-King con fuentes oficiales o con el estudio hidrológico adoptado.


## Novedades v1.5

- Incorpora referencias DGA/Manual de Carreteras para automatizar lluvia de diseño.
- Permite generar intensidades IDF y P24 desde P10D + coeficientes CD/CF + K=1,1 + abatimiento espacial.
- Incluye tablas internas editables para Rivadavia-Elqui, La Paloma-Limarí e Illapel-Choapa.
- Mejora presets DGA-AC y Verni-King para Región de Coquimbo, manteniéndolos editables y sujetos a confirmación del especialista.
- Agrega panel de referencias técnicas y deja trazabilidad en la memoria Word.

> Advertencia: los coeficientes precargados son apoyos de automatización. Para diseño definitivo se debe confirmar la cuenca oficial DGA, zona homogénea, P24, estación representativa, coeficientes regionales y condiciones locales.


## Nuevo en v1.5: KMZ de isoyetas

La aplicación permite cargar un **KMZ/KML de isoyetas**. Cada isoyeta puede traer el valor de precipitación en:

- nombre de la línea, por ejemplo `Isoyeta_60`, `P24_10_55`, `60`;
- descripción o ExtendedData;
- coordenada Z constante de la línea.

El sistema detecta la isoyeta más cercana al punto de descarga/control y, si la opción está activada, usa ese valor como `P10D` para generar lluvia de diseño mediante coeficientes de duración/frecuencia, K=1,1 y abatimiento espacial CA. El valor queda siempre editable por el usuario.

## Novedades v1.9

- Periodos de retorno fijos: **2, 5, 10, 25, 50, 100 y 200 años**.
- El selector DGA/Verni-King recomienda automáticamente presets regionales editables según la ubicación preliminar de la cuenca, pero mantiene la opción **Ingresar manualmente**.
- Se incorporan factores referenciales/editables para T=200 años en presets DGA-AC y Verni-King. Deben confirmarse con fuente oficial o justificación técnica antes de uso definitivo.
- El módulo sedimentológico ahora parte por defecto con **Terreno tipo desfavorable**, considerando alta disponibilidad de material, baja cobertura vegetal y concentraciones volumétricas conservadoras.
- Se mantiene la opción de modificar manualmente Cv, disponibilidad de material, cobertura vegetal, densidad de mezcla, densidad de sólidos, ángulo de fricción, productividad por área y productividad por cauce.


## Nuevo en v1.9: corrección robusta de KMZ/KML de isoyetas

Se corrigió el módulo de isoyetas para evitar errores al cargar KMZ grandes o exportados desde distintas fuentes GIS/Google Earth. La aplicación ahora:

- reinicia de forma segura el archivo cargado en cada rerun de Streamlit;
- selecciona automáticamente el KML interno más representativo si el KMZ trae varios KML;
- reconoce isoyetas como líneas o polígonos;
- evita confundir el período de retorno en nombres como `Isoyeta P10D 60 mm` con el valor de precipitación;
- permite dejar desactivado el dibujo de isoyetas en el mapa para no sobrecargar el navegador;
- dibuja solo una cantidad máxima configurable de isoyetas, manteniendo el cálculo con todas las geometrías leídas;
- conserva la opción de ingresar P10D manualmente si el KMZ no trae atributos claros.

Ejecutar prueba rápida:

```bash
python smoke_test.py
```

La prueba incluye lectura del KMZ demo Las Cardas y una prueba sintética de KMZ de isoyetas con valores 60, 75 y 80 mm.


## Nuevo en v1.9

Se validó la lectura del archivo DGA `Precipitaciones_Maxima_Diarias.kmz`. El parser reconoce valores numéricos en el nombre de la isoyeta y también en descripciones HTML tipo `VALOR_MM`. Además se incluye el KMZ DGA como base interna opcional para pruebas y automatización de P10D.


## Cambio v2.1
- La automatización de lluvia queda activa por defecto. Si se carga o usa KMZ de isoyetas, la aplicación genera P24 e IDF desde P10D + CD/CF/K sin requerir edición manual inicial.
