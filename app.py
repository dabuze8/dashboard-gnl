import streamlit as st
import pandas as pd
import plotly.express as px

# ----------------------------------------------------
# CONFIGURACIÓN GENERAL DEL DASHBOARD
# ----------------------------------------------------
st.set_page_config(
    page_title="Dashboard de Reportes GNL – ANH",
    layout="wide",
    page_icon="📊"
)

st.title("📊 Dashboard de Reportes GNL – ANH")

# ----------------------------------------------------
# FUNCIÓN PARA CARGAR TRAYECTORIA DE DATOS
# ----------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_excel("1 MASTER_BD_GNL.xlsx", sheet_name="BD_PGNL")

    # Renombrar columnas principales
    df = df.rename(columns={
        "FECHA": "Fecha",
        "GAS PSL\nRECIBIDO\n(MMPCD)": "GN_Entrada",
        "GNL\nPRODUCCION GNL\n(M3)": "Produccion_GNL",
        "GNL\nENTREGA  CISTERNAS\n(TN)": "Despachos"
    })

    # Convertir fecha
    df["Fecha"] = pd.to_datetime(df["Fecha"], errors="coerce")

    # Convertir columnas numéricas
    columnas_num = ["Produccion_GNL", "GN_Entrada", "Despachos"]
    for col in columnas_num:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    return df

# ----------------------------------------------------
# CARGAR DATOS
# ----------------------------------------------------
df = load_data()

# Mostrar columnas solo para diagnóstico (puedes borrar luego)
# st.write(df.columns.tolist())

# ----------------------------------------------------
# PANEL LATERAL – FILTROS
# ----------------------------------------------------
st.sidebar.header("Filtros de Análisis")

periodo = st.sidebar.selectbox(
    "Periodo:",
    ["Último Mes", "Últimos 3 Meses", "Último Año", "Todo"]
)

# Filtro de fechas manual
fecha_inicial = st.sidebar.date_input("Fecha inicial", df["Fecha"].min())
fecha_final   = st.sidebar.date_input("Fecha final", df["Fecha"].max())

# Aplicar filtros
df_filtrado = df[(df["Fecha"] >= pd.to_datetime(fecha_inicial)) &
                 (df["Fecha"] <= pd.to_datetime(fecha_final))]

# Filtros por periodo
if periodo == "Último Mes":
    df_filtrado = df_filtrado[df_filtrado["Fecha"] >= (df["Fecha"].max() - pd.DateOffset(months=1))]
elif periodo == "Últimos 3 Meses":
    df_filtrado = df_filtrado[df_filtrado["Fecha"] >= (df["Fecha"].max() - pd.DateOffset(months=3))]
elif periodo == "Último Año":
    df_filtrado = df_filtrado[df_filtrado["Fecha"] >= (df["Fecha"].max() - pd.DateOffset(years=1))]

st.markdown(f"### Registros filtrados: **{len(df_filtrado)}**")

# ----------------------------------------------------
# GRÁFICO 1 – PRODUCCIÓN GNL (m³/día)
# ----------------------------------------------------
st.subheader("🧱 Producción de GNL (m³ por día)")

try:
    fig_prod = px.bar(
        df_filtrado,
        x="Fecha",
        y="Produccion_GNL",
        title="Producción de GNL (m³/día)",
        color_discrete_sequence=["#74b9ff"]
    )
    st.plotly_chart(fig_prod, use_container_width=True)
except Exception as e:
    st.error(f"Error en gráfico de Producción: {e}")

# ----------------------------------------------------
# GRÁFICO 2 – DESPACHOS A CISTERNAS (TN)
# ----------------------------------------------------
st.subheader("🚚 Despachos de GNL a Cisternas (TN)")

try:
    fig_des = px.bar(
        df_filtrado,
        x="Fecha",
        y="Despachos",
        title="Despachos de GNL (TN por día)",
        color_discrete_sequence=["#55efc4"]
    )
    st.plotly_chart(fig_des, use_container_width=True)
except Exception as e:
    st.error(f"Error en gráfico de Despachos: {e}")

# ----------------------------------------------------
# GRÁFICO 3 – GAS NATURAL DE ENTRADA (MMPCD)
# ----------------------------------------------------
st.subheader("🔥 Gas Natural de Entrada a Planta (MMPCD)")

try:
    fig_gn = px.line(
        df_filtrado,
        x="Fecha",
        y="GN_Entrada",
        title="Gas Natural de Entrada (MMPCD)",
        markers=True,
        color_discrete_sequence=["#fdcb6e"]
    )
    st.plotly_chart(fig_gn, use_container_width=True)
except Exception as e:
    st.error(f"Error en gráfico de GN Entrada: {e}")

# ----------------------------------------------------
# TABLA FINAL
# ----------------------------------------------------
st.subheader("📄 Tabla detalle de datos filtrados")
st.dataframe(df_filtrado, use_container_width=True)
