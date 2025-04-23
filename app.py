import streamlit as st
import pandas as pd
import plotly.express as px

st.title("App de datos y video")

# Carga de archivo Excel
archivo_excel = st.file_uploader("Sube un archivo Excel", type=["xlsx", "xls"])

if archivo_excel:
    df = pd.read_excel(archivo_excel)
    st.subheader("Vista previa de datos")
    st.dataframe(df)

    columnas = df.columns.tolist()
    x_col = st.selectbox("Selecciona columna X", columnas)
    y_col = st.selectbox("Selecciona columna Y", columnas)

    if x_col and y_col:
        fig = px.line(df, x=x_col, y=y_col, title=f"{y_col} vs {x_col}")
        st.plotly_chart(fig)

# Carga de archivo de video
video_file = st.file_uploader("Sube un video (.mp4)", type=["mp4"])

if video_file:
    st.subheader("Video cargado")
    st.video(video_file)
