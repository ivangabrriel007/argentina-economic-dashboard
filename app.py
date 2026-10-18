
import streamlit as st
import pandas as pd
import requests
import plotly.express as px

st.set_page_config(
    page_title="Argentina Economic Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("🇦🇷 Argentina Economic Dashboard")
st.write("Panel de indicadores económicos de Argentina")

@st.cache_data(ttl=3600)
def obtener_inflacion():
    url = "https://apis.datos.gob.ar/series/api/series"

    parametros = {
        "ids": "145.3_INGNACUAL_DICI_M_38",
        "start_date": "2025-01-01",
        "end_date": "2026-12-31",
        "limit": 100
    }

    respuesta = requests.get(
        url,
        params=parametros,
        timeout=20
    )
    respuesta.raise_for_status()
    datos = respuesta.json()

    tabla = pd.DataFrame(
        datos["data"],
        columns=["Fecha", "Inflacion"]
    )

    tabla["Fecha"] = pd.to_datetime(tabla["Fecha"])
    tabla["Inflacion (%)"] = (
        tabla["Inflacion"] * 100
    ).round(2)

    return tabla

try:
    tabla = obtener_inflacion()
    tabla = tabla.sort_values("Fecha")

    ultimo = tabla.iloc[-1]
    promedio = tabla["Inflacion (%)"].mean()

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Última inflación mensual",
        f"{ultimo['Inflacion (%)']:.2f}%",
        ultimo["Fecha"].strftime("%m/%Y")
    )

    col2.metric(
        "Promedio del período",
        f"{promedio:.2f}%"
    )

    col3.metric(
        "Meses disponibles",
        len(tabla)
    )

    st.subheader("Evolución de la inflación mensual")

    grafico = px.line(
        tabla,
        x="Fecha",
        y="Inflacion (%)",
        markers=True,
        title="IPC nacional: variación mensual"
    )

    grafico.update_layout(
        xaxis_title="Fecha",
        yaxis_title="Inflación mensual (%)"
    )

    st.plotly_chart(grafico, use_container_width=True)

    st.subheader("Datos utilizados")
    st.dataframe(
        tabla[["Fecha", "Inflacion (%)"]],
        use_container_width=True,
        hide_index=True
    )

    st.caption(
        "Fuente: Argentina.gob.ar/Datos — serie de IPC nacional, "
        "con fuente INDEC. Los últimos períodos disponibles "
        "dependen de la actualización de la fuente."
    )

except Exception as error:
    st.error("No pudimos obtener los datos de inflación.")
    st.write("Detalle del error:", error)
    st.info(
        "Revisá la conexión o la disponibilidad de la API "
        "y volvé a intentarlo."
    )
