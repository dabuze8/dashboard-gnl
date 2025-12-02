import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dashboard de Reportes GNL – ANH", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_excel("1. MASTER_BD_GNL.xlsx", sheet_name="BD_PGNL")

    # Convertir FECHA a datetime
    df["FECHA"] = pd.to_datetime(df["FECHA"], errors="coerce")

    # Limpiar columnas numéricas
    numeric_cols = [
        "GNL\nPRODUCCION GNL\n(TN)",
        "GNL\nENTREGA  CISTERNAS\n(TN)"
    ]

    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    return df

df = load_data()

# FILTROS ----------
st.sidebar.header("Filtros de Análisis")

periodo = st.sidebar.selectbox(
    "Periodo:",
    ["Último Mes", "Últimos 3 Meses", "Último Año", "Todo"]
)

fecha_min = df["FECHA"].min()
fecha_max = df["FECHA"].max()

fecha_inicial = st.sidebar.date_input("Fecha inicial", fecha_min)
fecha_final = st.sidebar.date_input("Fecha final", fecha_max)

# FILTRAR DATOS
df_filtrado = df[(df["FECHA"] >= pd.to_datetime(fecha_inicial)) &
                 (df["FECHA"] <= pd.to_datetime(fecha_final))]

st.title("📊 Dashboard de Reportes GNL – ANH")
st.subheader(f"Registros filtrados: {len(df_filtrado)}")

# GRAFICO 1 – Producción de GNL
columna_produccion = "GNL\nPRODUCCION GNL\n(TN)"

if columna_produccion in df.columns:
    fig1 = px.bar(
        df_filtrado,
        x="FECHA",
        y=columna_produccion,
        title="📦 Producción de GNL (TN por día)",
        color_discrete_sequence=["#74b9ff"]
    )
    st.plotly_chart(fig1, use_container_width=True)
else:
    st.error(f"La columna {columna_produccion} no existe en el Excel.")

# GRAFICO 2 – Despachos (ENTREGA CISTERNAS)
columna_despacho = "GNL\nENTREGA  CISTERNAS\n(TN)"

if columna_despacho in df.columns:
    fig2 = px.line(
        df_filtrado,
        x="FECHA",
        y=columna_despacho,
        title="🚚 Despachos de GNL a Cisternas (TN por día)",
        markers=True,
        color_discrete_sequence=["#55efc4"]
    )
    st.plotly_chart(fig2, use_container_width=True)
else:
    st.error(f"La columna {columna_despacho} no existe en el Excel.")
