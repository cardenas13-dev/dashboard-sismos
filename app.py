"""Dashboard interactivo – Sismos significativos 1965–2016 (USGS).
Tarea 4 – Programación para el análisis de datos (UNAD, 203008069).
Extensión comunicativa del EDA desarrollado en la Tarea 3.
"""
import math

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import streamlit as st
from scipy import stats

st.set_page_config(page_title="Sismos significativos 1965–2016", page_icon="🌎", layout="wide")

# ----------------------------------------------------------------------------- estilo (tema oscuro)
FONDO, TARJETA, TEXTO = "#0B1426", "#132238", "#E6EDF7"
VERDE, AMBAR, ROJO, AZUL = "#2ECC71", "#F5A623", "#E5484D", "#4C9AFF"
plt.rcParams.update({
    "figure.facecolor": FONDO, "axes.facecolor": TARJETA, "savefig.facecolor": FONDO,
    "axes.edgecolor": "#3A4F6E", "axes.labelcolor": TEXTO, "text.color": TEXTO,
    "xtick.color": TEXTO, "ytick.color": TEXTO, "axes.titlecolor": TEXTO,
    "grid.color": "#2B3F5C", "legend.facecolor": TARJETA, "legend.edgecolor": "#3A4F6E",
    "axes.titlesize": 13, "axes.labelsize": 11,
})
sns.set_theme(style="darkgrid", rc=dict(plt.rcParams))

CATEGORIAS = ["Moderado (menos de 6)", "Fuerte (6 a 6,9)", "Mayor (7 a 7,9)", "Gran (8 o más)"]
COLORES_CAT = {CATEGORIAS[0]: VERDE, CATEGORIAS[1]: AMBAR, CATEGORIAS[2]: "#F07A3B", CATEGORIAS[3]: ROJO}
TIPOS = {"Earthquake": "Sismo", "Nuclear Explosion": "Explosión nuclear",
         "Explosion": "Otra explosión", "Rock Burst": "Estallido de roca"}


# Texto final del Ejercicio IA T4-C (corregido por el estudiante): se muestra tal cual en la sección de hallazgos.
TEXTO_FUERZA_PROFUNDIDAD = (
    "**En una frase – fuerza y profundidad:** los datos no muestran relación entre qué tan fuerte es un sismo y a qué profundidad "
    "ocurre: hay sismos fuertes tanto superficiales como profundos, y lo mismo pasa con los moderados. En estos datos, saber la "
    "profundidad no ayuda a anticipar qué tan fuerte fue el sismo. Recomendación: evaluar la gravedad de un sismo por su magnitud "
    "(fuerza) y usar la profundidad solo como información complementaria sobre dónde se originó."
)


def mostrar(fig):
    """Muestra la figura en Streamlit y libera la memoria de matplotlib."""
    st.pyplot(fig)
    plt.close(fig)


# ----------------------------------------------------------------------------- datos
@st.cache_data
def cargar_datos():
    df = pd.read_csv("database.csv")
    df["Fecha"] = pd.to_datetime(df["Date"], format="mixed", errors="coerce", utc=True).dt.tz_localize(None)
    df = df.dropna(subset=["Fecha"]).copy()
    df["Año"] = df["Fecha"].dt.year.astype(int)
    df["Tipo de evento"] = df["Type"].map(TIPOS)
    df["Categoría de magnitud"] = pd.cut(df["Magnitude"], [0, 6, 7, 8, 10], right=False, labels=CATEGORIAS)
    return df


@st.cache_data
def prueba_estadistica(_df):
    """Prueba t de Welch: magnitud de sismos vs explosiones nucleares (resultado de la Tarea 3, Parte 1)."""
    sismos = _df.loc[_df["Type"] == "Earthquake", "Magnitude"].dropna()
    nucleares = _df.loc[_df["Type"] == "Nuclear Explosion", "Magnitude"].dropna()
    t, p = stats.ttest_ind(sismos, nucleares, equal_var=False)
    return {"n1": len(sismos), "n2": len(nucleares), "m1": sismos.mean(), "m2": nucleares.mean(), "t": t, "p": p}


df = cargar_datos()

# ----------------------------------------------------------------------------- encabezado
st.title("🌎 Sismos significativos del mundo, 1965–2016")
st.caption(
    "Dashboard del análisis exploratorio (EDA) de la base *Significant Earthquakes 1965–2016* del Servicio "
    "Geológico de EE. UU. (USGS): 23.412 eventos de magnitud 5,5 o mayor. Use los filtros de la izquierda "
    "para explorar los datos."
)

# ----------------------------------------------------------------------------- sidebar: filtros
with st.sidebar:
    st.header("Filtros")
    tipos_sel = st.multiselect(
        "Tipo de evento", options=list(TIPOS.values()), default=list(TIPOS.values()),
        help="La gran mayoría de los eventos son sismos naturales; las explosiones nucleares son pocas.",
    )
    mag_min, mag_max = float(df["Magnitude"].min()), float(df["Magnitude"].max())
    rango_mag = st.slider("Magnitud (fuerza del sismo)", mag_min, mag_max, (mag_min, mag_max), step=0.1,
                          help="La magnitud mide la fuerza del sismo. El catálogo solo incluye 5,5 o más.")
    prof_min, prof_max = math.floor(df["Depth"].min()), math.ceil(df["Depth"].max())
    rango_prof = st.slider("Profundidad (km)", prof_min, prof_max, (prof_min, prof_max),
                           help="Qué tan por debajo de la superficie ocurrió el sismo.")
    rango_anio = st.slider("Años", int(df["Año"].min()), int(df["Año"].max()),
                           (int(df["Año"].min()), int(df["Año"].max())))
    variable = st.selectbox("Variable para las métricas", ["Magnitud", "Profundidad (km)"],
                            help="Cambia el dato que se resume en las métricas y en el histograma.")

COL = {"Magnitud": "Magnitude", "Profundidad (km)": "Depth"}[variable]

df_f = df[
    df["Tipo de evento"].isin(tipos_sel)
    & df["Magnitude"].between(*rango_mag)
    & df["Depth"].between(*rango_prof)
    & df["Año"].between(*rango_anio)
]

if df_f.empty:
    st.warning("Con estos filtros no hay eventos. Amplíe los rangos o seleccione más tipos de evento.")
    st.stop()

# ----------------------------------------------------------------------------- 1. exploración
st.header("1. Exploración de datos")
c1, c2, c3, c4 = st.columns(4)
c1.metric("Eventos seleccionados", f"{len(df_f):,}".replace(",", "."))
c2.metric(f"Promedio – {variable}", f"{df_f[COL].mean():.2f}")
c3.metric(f"Variación típica – {variable}", f"{df_f[COL].std():.2f}" if len(df_f) > 1 else "—",
          help="Desviación estándar: cuánto se alejan, en promedio, los datos del promedio.")
c4.metric(f"Valor máximo – {variable}", f"{df_f[COL].max():.1f}")

tabla = df_f[["Fecha", "Tipo de evento", "Magnitude", "Depth", "Latitude", "Longitude", "Categoría de magnitud"]].rename(
    columns={"Magnitude": "Magnitud", "Depth": "Profundidad (km)", "Latitude": "Latitud", "Longitude": "Longitud"})
st.dataframe(tabla, height=280, hide_index=True)
st.download_button("⬇️ Descargar los datos filtrados (CSV)", tabla.to_csv(index=False).encode("utf-8"),
                   file_name="sismos_filtrados.csv", mime="text/csv")

# ----------------------------------------------------------------------------- 2. visualizaciones
st.header("2. Visualizaciones")
st.caption("Los gráficos se actualizan con los filtros de la izquierda.")
t1, t2, t3, t4, t5 = st.tabs(["Fuerza de los sismos", "Distribución", "Fuerza y profundidad", "Evolución en el tiempo", "Dónde ocurren"])

with t1:
    conteo = df_f["Categoría de magnitud"].value_counts().reindex(CATEGORIAS).fillna(0)
    fig, ax = plt.subplots(figsize=(8, 4.5))
    barras = ax.bar(conteo.index, conteo.values, color=[COLORES_CAT[c] for c in conteo.index])
    ax.bar_label(barras, fmt="%d", padding=2, color=TEXTO)
    ax.set_title("¿Cuántos eventos hay de cada nivel de fuerza?")
    ax.set_xlabel("Nivel de fuerza (magnitud)")
    ax.set_ylabel("Número de eventos")
    plt.setp(ax.get_xticklabels(), rotation=10)
    mostrar(fig)

with t2:
    col_a, col_b = st.columns(2)
    with col_a:
        fig, ax = plt.subplots(figsize=(6, 4.2))
        sns.histplot(df_f[COL], bins=40, color=AZUL, kde=len(df_f) > 5, ax=ax)
        ax.set_title(f"¿Qué valores son más comunes? – {variable}")
        ax.set_xlabel(variable)
        ax.set_ylabel("Número de eventos")
        mostrar(fig)
    with col_b:
        fig, ax = plt.subplots(figsize=(6, 4.2))
        sns.boxplot(y=df_f[COL], color=AMBAR, ax=ax, flierprops=dict(markerfacecolor=ROJO, markeredgecolor=ROJO, markersize=3))
        ax.set_title(f"Valores típicos y valores extremos – {variable}")
        ax.set_ylabel(variable)
        ax.set_xlabel("Los puntos rojos son eventos fuera de lo habitual")
        mostrar(fig)

with t3:
    validas = df_f["Categoría de magnitud"].value_counts()
    orden = [c for c in CATEGORIAS if validas.get(c, 0) >= 2]
    if orden:
        fig, ax = plt.subplots(figsize=(8.5, 5))
        sns.violinplot(data=df_f[df_f["Categoría de magnitud"].isin(orden)], x="Categoría de magnitud", y="Depth",
                       order=orden, palette=[COLORES_CAT[c] for c in orden], hue="Categoría de magnitud",
                       legend=False, inner="quartile", cut=0, ax=ax)
        ax.set_title("¿Los sismos más fuertes ocurren a mayor profundidad?")
        ax.set_xlabel("Nivel de fuerza (magnitud)")
        ax.set_ylabel("Profundidad (km)")
        plt.setp(ax.get_xticklabels(), rotation=10)
        mostrar(fig)
        st.caption("Cuanto más ancha es la figura, más eventos hay a esa profundidad. Con estos datos, la profundidad es parecida en todos los niveles de fuerza.")
    else:
        st.info("Se necesitan al menos 2 eventos por nivel de fuerza para dibujar este gráfico.")

with t4:
    anual = df_f.groupby("Año").size().reset_index(name="n")
    fig, ax = plt.subplots(figsize=(10, 4.5))
    ax.plot(anual["Año"], anual["n"], marker="o", ms=3.5, color=AZUL, label="Eventos por año")
    if len(anual) >= 3:
        z = np.polyfit(anual["Año"], anual["n"], 1)
        ax.plot(anual["Año"], np.polyval(z, anual["Año"]), "--", color=AMBAR, label="Tendencia general")
    ax.set_title("¿Cuántos eventos se registraron cada año?")
    ax.set_xlabel("Año")
    ax.set_ylabel("Número de eventos")
    ax.legend()
    mostrar(fig)

with t5:
    muestra = df_f.sample(min(len(df_f), 5000), random_state=42)
    fig, ax = plt.subplots(figsize=(11, 5.5))
    sc = ax.scatter(muestra["Longitude"], muestra["Latitude"], c=muestra["Depth"], s=(muestra["Magnitude"] - 5) ** 3 * 4,
                    cmap="viridis_r", alpha=0.55, edgecolor="none")
    fig.colorbar(sc, ax=ax, label="Profundidad (km)")
    ax.set_title("Dónde ocurren los eventos (tamaño = fuerza, color = profundidad)")
    ax.set_xlabel("Longitud (°)")
    ax.set_ylabel("Latitud (°)")
    mostrar(fig)
    if len(df_f) > 5000:
        st.caption("Por rapidez se muestra una muestra de 5.000 eventos de los seleccionados.")

# ----------------------------------------------------------------------------- 3. validación estadística
st.header("3. Validación estadística")
r = prueba_estadistica(df)
v1, v2, v3 = st.columns(3)
v1.metric("Magnitud promedio – sismos", f"{r['m1']:.2f}", help=f"Basado en {r['n1']:,} eventos".replace(",", "."))
v2.metric("Magnitud promedio – explosiones nucleares", f"{r['m2']:.2f}", help=f"Basado en {r['n2']} eventos")
v3.metric("Probabilidad de ver esta diferencia solo por azar", f"{r['p'] * 100:.0f} %",
          help="Es el 'valor p' de la prueba. Si es menor a 5 %, se considera que hay una diferencia real.")
st.markdown(
    f"""
**¿Qué se comparó?** Si los sismos naturales y las explosiones nucleares registradas en el catálogo tienen, en promedio, la misma fuerza.

**¿Qué se encontró?** El promedio es casi igual ({r['m1']:.2f} frente a {r['m2']:.2f}). Si ambos grupos fueran en realidad iguales,
una diferencia como esta aparecería por simple azar cerca de {r['p'] * 100:.0f} de cada 100 veces, un nivel que no es lo bastante raro:
por eso **no podemos afirmar que exista una diferencia real** entre ambos grupos.

**Precaución:** esto no demuestra que sean idénticos, solo que con estos datos no se detecta diferencia. Además, los grupos son
muy desiguales ({r['n1']:,} sismos frente a {r['n2']} explosiones), lo que obliga a interpretar con cuidado.
""".replace(",", ".")
)

# ----------------------------------------------------------------------------- 4. hallazgos
st.header("4. Hallazgos y recomendaciones")
st.markdown(
    """
### ¿Qué analicé?
Revisé el registro de **23.412 eventos sísmicos de magnitud 5,5 o mayor** ocurridos en el mundo entre 1965 y 2016, publicado por el
Servicio Geológico de Estados Unidos. Para cada evento se conoce cuándo y dónde ocurrió, qué tan fuerte fue y a qué profundidad.
Casi todos (99 %) son sismos naturales; el resto son explosiones, principalmente nucleares.

### ¿Qué encontré?
- **La mayoría de los sismos ocurre cerca de la superficie:** 8 de cada 10 se originan a menos de 70 km de profundidad, y solo
  alrededor de 6 de cada 100 ocurren a más de 300 km.
- **Los sismos muy fuertes son poco frecuentes:** aproximadamente 3 de cada 100 alcanzan una magnitud de 7 o más.
- **La fuerza de un sismo no va ligada a su profundidad:** los sismos fuertes aparecen tanto cerca de la superficie como a gran
  profundidad.
- **El número de sismos registrados por año aumentó** (de unos 330 por año en los primeros diez años a unos 520 en los últimos diez),
  mientras que su fuerza promedio se mantuvo igual.

### ¿Qué significa?
Los sismos se concentran en la parte superficial de la tierra, donde, en general, sus efectos se sienten con más intensidad. Que la fuerza no dependa de la
profundidad quiere decir que, en estos datos, saber a qué profundidad ocurrió un sismo no ayuda a anticipar qué tan fuerte fue.
El aumento de sismos registrados no significa necesariamente que la tierra esté más activa: podría deberse a que hoy se detectan y registran
más eventos que hace 50 años porque hay más y mejores estaciones de medición.

### ¿Qué se recomendaría?
1. **Evaluar la gravedad de un sismo por su magnitud**, y no usar la profundidad como indicador de qué tan fuerte fue.
2. **No concluir que hay más actividad sísmica** solo por el aumento de eventos registrados; antes habría que confirmarlo con información que no dependa de
   la cantidad de estaciones.
3. **Para decisiones en un lugar concreto**, complementar este análisis con datos de esa región (por ejemplo, del Servicio Geológico
   Colombiano), pues aquí se mezclan todos los continentes y solo se incluyen sismos de magnitud 5,5 o más.
"""
)

st.info(TEXTO_FUERZA_PROFUNDIDAD)

# gráficos de apoyo a los hallazgos (datos completos, no dependen de los filtros)
g1, g2 = st.columns(2)
with g1:
    prof = pd.cut(df["Depth"], [-10, 70, 300, 1000], right=False,
                  labels=["Superficiales\n(menos de 70 km)", "Intermedios\n(70 a 300 km)", "Profundos\n(más de 300 km)"])
    porc = prof.value_counts(normalize=True).sort_index() * 100
    fig, ax = plt.subplots(figsize=(6, 4.2))
    barras = ax.bar(porc.index, porc.values, color=[VERDE, AMBAR, ROJO])
    ax.bar_label(barras, fmt="%.0f %%", padding=2, color=TEXTO)
    ax.set_title("¿A qué profundidad ocurren la mayoría de los sismos?")
    ax.set_ylabel("Porcentaje de los eventos")
    ax.set_xlabel("Profundidad del sismo")
    ax.set_ylim(0, 100)
    mostrar(fig)
with g2:
    anual_total = df[df["Type"] == "Earthquake"].groupby("Año").size()
    fig, ax = plt.subplots(figsize=(6, 4.2))
    ax.plot(anual_total.index, anual_total.values, color=AZUL, marker="o", ms=3)
    z = np.polyfit(anual_total.index, anual_total.values, 1)
    ax.plot(anual_total.index, np.polyval(z, anual_total.index), "--", color=AMBAR, label="Tendencia general")
    ax.set_title("Sismos registrados por año: ¿más actividad o mejor registro?")
    ax.set_xlabel("Año")
    ax.set_ylabel("Sismos registrados")
    ax.legend()
    mostrar(fig)

st.divider()
st.caption("Eder Cárdenas · Programación para el análisis de datos (203008069) · UNAD · Tarea 4 · Fuente: USGS (vía Kaggle).")
