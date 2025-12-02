import streamlit as st
import pandas as pd
import plotly.express as px

# =========================
# CONFIGURACIÓN GENERAL
# =========================
st.set_page_config(
    page_title="Dashboard GNL – ANH",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("📊 Dashboard de Reportes GNL – ANH")

# =========================
# CARGA DE DATOS
# =========================
@st.cache_data
def load_data():
    df = pd.read_excel("1 MASTER_BD_GNL.xlsx", sheet_name="BD_PGNL")
    return df

df = load_data()

# Renombrar columnas clave para simplificar
df = df.rename(columns={
    "FECHA": "Fecha",
    "GAS PSL RECIBIDO (MMPCD)": "GN_Entrada",
    "GNL PRODUCCION GN (M3)": "Produccion_GNL",
    "GNL ENTREGA CISTERNAS (TN)": "Despachos"
})

# Convertir fecha
df["Fecha"] = pd.to_datetime(df["Fecha"])

# =========================
# SIDEBAR DE FILTROS
# =========================
st.sidebar.header("Filtros de Análisis")

# Periodos sugeridos
periodo = st.sidebar.selectbox(
    "Periodo:",
    ["Último Mes", "Últimos 3 Meses", "Últimos 6 Meses", "Año Actual", "Todo"]
)

# Rango de fechas manual
fecha_inicio = st.sidebar.date_input("Fecha inicial", value=df["Fecha"].min())
fecha_fin = st.sidebar.date_input("Fecha final", value=df["Fecha"].max())

# Filtrado
df_filtrado = df[(df["Fecha"] >= pd.to_datetime(fecha_inicio)) &
                 (df["Fecha"] <= pd.to_datetime(fecha_fin))]

st.write(f"**Registros filtrados: {len(df_filtrado)}**")

# =========================
# GRÁFICOS
# =========================

col1, col2 = st.columns(2)

# --------------------------
# GRAFICO 1 – PRODUCCIÓN
# --------------------------
with col1:
    st.subheader("📦 Producción de GNL (m³ por día)")
    fig1 = px.bar(
        df_filtrado,
        x="Fecha",
        y="Produccion_GNL",
        title="Producción GNL",
        text="Produccion_GNL",
        color_discrete_sequence=["#74b9ff"]
    )
    fig1.update_traces(texttemplate="%{text:.2s}", textposition="outside")
    st.plotly_chart(fig1, use_container_width=True)

# --------------------------
# GRAFICO 2 – DESPACHOS
# --------------------------
with col2:
    st.subheader("🚚 Despachos de GNL (TN por día)")
    fig2 = px.line(
        df_filtrado,
        x="Fecha",
        y="Despachos",
        markers=True,
        title="Entregas a Cisterna (Despachos)"
    )
    st.plotly_chart(fig2, use_container_width=True)

# --------------------------
# GRAFICO 3 – GN ENTRADA
# --------------------------
st.subheader("🔥 Gas Natural Recibido (MMPCD)")
fig3 = px.area(
    df_filtrado,
    x="Fecha",
    y="GN_Entrada",
    title="Gas Natural de Entrada",
    color_discrete_sequence=["#55efc4"]
)
st.plotly_chart(fig3, use_container_width=True)
