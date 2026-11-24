# 🌎 Dashboard de sismos significativos del mundo (1965–2016)

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://dashboard-sismos-9hlkyxypoeqwqsp5qtnstq.streamlit.app/)

## Descripción del proyecto

Este proyecto convierte el análisis exploratorio de datos (EDA) desarrollado en la **Tarea 3** del curso *Programación para el
análisis de datos* en un **dashboard interactivo** pensado para personas que no son especialistas en estadística. No es un análisis
nuevo: son los mismos datos y las mismas conclusiones, presentados de forma accesible.

El dataset utilizado es **Significant Earthquakes, 1965–2016**, publicado por el Servicio Geológico de Estados Unidos (USGS) en
[Kaggle](https://www.kaggle.com/datasets/usgs/earthquake-database). Contiene 23.412 eventos sísmicos de magnitud 5,5 o mayor, con
fecha, ubicación, profundidad y magnitud. Se eligió porque es una base real, georreferenciada y con más de 50 años de registro,
útil para entender dónde y cómo ocurren los sismos más importantes.

El dashboard permite filtrar por tipo de evento, magnitud, profundidad y año; ver métricas y una tabla de datos; explorar
gráficos que se actualizan con los filtros; consultar una validación estadística explicada en lenguaje claro y leer los hallazgos y
recomendaciones.

## Dashboard publicado

👉 **https://dashboard-sismos-9hlkyxypoeqwqsp5qtnstq.streamlit.app/**

## Captura de pantalla

<img width="1366" height="768" alt="image" src="https://github.com/user-attachments/assets/128fd304-73ba-47d8-afd6-b9276b40295e" />

## Hallazgos principales del EDA

1. **Los sismos son mayoritariamente superficiales:** cerca del 80 % ocurre a menos de 70 km de profundidad y solo ~6 % a más de 300 km.
2. **Los sismos muy fuertes son poco frecuentes:** ~3 % alcanza una magnitud de 7 o más.
3. **La magnitud no está asociada a la profundidad** (correlación cercana a cero).
4. **Sismos y explosiones nucleares tienen magnitud promedio similar** (5,88 vs 5,85); la prueba de hipótesis no encuentra diferencia significativa (p ≈ 0,12).
5. **El número de sismos registrados por año crece** (≈ 330/año en 1965–1974 a ≈ 520/año en 2007–2016) con magnitud promedio estable; probablemente refleja mejoras en la detección más que mayor actividad sísmica.

## Estructura del repositorio

| Archivo | Descripción |
|---|---|
| `app.py` | Código principal del dashboard (Streamlit) |
| `database.csv` | Dataset USGS (2,4 MB) |
| `requirements.txt` | Librerías necesarias |
| `.streamlit/config.toml` | Tema oscuro del dashboard |
| `README.md` | Este documento |

## Instalación y ejecución local

1. Clonar el repositorio:
   ```bash
   git clone https://github.com/cardenas13-dev/dashboard-sismos.git
   cd dashboard-sismos
   ```
2. (Opcional) Crear un entorno virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate        # En Windows: venv\Scripts\activate
   ```
3. Instalar las dependencias:
   ```bash
   pip install -r requirements.txt
   ```
4. Ejecutar la aplicación:
   ```bash
   streamlit run app.py
   ```
5. Abrir en el navegador: <http://localhost:8501>

## Autor

**Eder Cárdenas** · Curso: Programación para el análisis de datos (203008069) · Universidad Nacional Abierta y a Distancia (UNAD) · Noviembre de 2026
