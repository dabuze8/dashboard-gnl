import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------
# CONFIGURACIÓN DE LA PÁGINA
# -----------------------------
st.set_page_config(
    page_title="Dashboard de Reportes GNL – ANH",
    layout="wide",
    page_icon="📊"
)

# -----------------------------
# CARGAR DATA
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_excel("1. MASTER_BD_GNL.xlsx", sheet_name="BD_PGNL")

    # Convertir fecha
    df["FECHA"] = pd.to_datetime(df["FECHA"], errors="coerce")

    # Identificar columnas numéricas relevantes
    numeric_columns = [
        "GNL\nPRODUCCION GNL\n(TN)",
        "GNL\nPRODUCCION GNL\n(M3)",
        "GAS PSL\nCOMBUSTIBLE\n(MMPCD)",   # NUEVO GRÁFICO
        "GAS PSL\nGAS A GNL\n(MMPCD)",
        "GAS GASYRG\nGAS A GNL\n(MMPCD)"
    ]

    # Convertir a número
    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    return df


df = load_data()

# -----------------------------
# SIDEBAR – FILTROS
# -----------------------------
st.sidebar.title("Filtros de Análisis")

periodos = ["Último Mes", "Últimos 3 Meses", "Último Año", "Todo"]
periodo_sel = st.sidebar.selectbox("Periodo:", periodos)

fecha_min = df["FECHA"].min()
fecha_max = df["FECHA"].max()

fecha_i = st.sidebar.date_input("Fecha inicial", fecha_min)
fecha_f = st.sidebar.date_input("Fecha final", fecha_max)

# Ajuste según período rápido
if periodo_sel == "Último Mes":
    fecha_i = fecha_max - pd.DateOffset(months=1)
elif periodo_sel == "Últimos 3 Meses":
    fecha_i = fecha_max - pd.DateOffset(months=3)
elif periodo_sel == "Último Año":
    fecha_i = fecha_max - pd.DateOffset(years=1)

# Filtrar
df_filtrado = df[(df["FECHA"] >= pd.to_datetime(fecha_i)) &
                 (df["FECHA"] <= pd.to_datetime(fecha_f))]

# -----------------------------
# TÍTULO PRINCIPAL
# -----------------------------
st.title("📊 Dashboard de Reportes GNL – ANH")
st.caption(f"Registros filtrados: **{len(df_filtrado)}**")

# -----------------------------
# GRÁFICO 1 – PRODUCCIÓN GNL (M³ por día)
# -----------------------------
st.subheader("📦 Producción de GNL (m³ por día)")

fig1 = px.bar(
    df_filtrado,
    x="FECHA",
    y="GNL\nPRODUCCION GNL\n(M3)",
    title="Producción diaria de GNL (M³)",
    color_discrete_sequence=["#74b9ff"]
)
st.plotly_chart(fig1, use_container_width=True)

# -----------------------------
# GRÁFICO 2 – GAS NATURAL A GNL (MMPCD)
# -----------------------------
st.subheader("🔥 Gas Natural procesado a GNL (MMPCD)")

col_gn1 = "GAS PSL\nGAS A GNL\n(MMPCD)"
col_gn2 = "GAS GASYRG\nGAS A GNL\n(MMPCD)"

fig2 = px.line(
    df_filtrado,
    x="FECHA",
    y=[col_gn1, col_gn2],
    markers=True,
    title="Gas procesado hacia GNL (MMPCD)",
    color_discrete_sequence=["#55efc4", "#ffeaa7"],
)
st.plotly_chart(fig2, use_container_width=True)

# -----------------------------
# NUEVO GRÁFICO – GAS PSL COMBUSTIBLE
# -----------------------------
st.subheader("🔋 Gas PSL Combustible (MMPCD)")

fig3 = px.line(
    df_filtrado,
    x="FECHA",
    y="GAS PSL\nCOMBUSTIBLE\n(MMPCD)",
    markers=True,
    title="Consumo de Combustible – Gas PSL (MMPCD)",
    color_discrete_sequence=["#00cc96"]
)
st.plotly_chart(fig3, use_container_width=True)

# -----------------------------
# FOOTER
# -----------------------------
st.markdown("---")
st.markdown("🔧 **ANH – Dirección de Distritos Técnica** | Dashboard generado con Streamlit")


