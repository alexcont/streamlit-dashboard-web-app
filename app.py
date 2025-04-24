import streamlit as st
import pandas as pd
import plotly.express as px
import io
import os
import tempfile
import cv2

st.set_page_config(page_title="Dashboard de Datos y Video", layout="wide")
st.title("📊 Dashboard interactivo de Excel + 🎥 Video")

col1, col2 = st.columns(2)

with col1:
    st.header("📈 Gráficas")
    archivo_excel = st.file_uploader("📂 Sube un archivo Excel", type=["xlsx", "xls"])

    if archivo_excel:
        df = pd.read_excel(archivo_excel)
        st.subheader("👁️ Vista previa de datos")
        st.dataframe(df, use_container_width=True)

        columnas = df.columns.tolist()
        x_col = st.selectbox("📌 Columna X", columnas)
        y_col = st.selectbox("📌 Columna Y", columnas)

        if x_col and y_col:
            fig = px.line(
                df,
                x=x_col,
                y=y_col,
                title=f"Evolución de {y_col} respecto a {x_col}",
                markers=True,
                line_shape="spline",
            )
            fig.update_layout(
                xaxis_title=x_col,
                yaxis_title=y_col,
                template="plotly_white",
                title_font_size=20
            )
            st.plotly_chart(fig, use_container_width=True)

            # Botón para descargar los datos filtrados
            csv = df[[x_col, y_col]].to_csv(index=False).encode('utf-8')
            st.download_button(
                label="⬇️ Descargar datos CSV",
                data=csv,
                file_name="datos_filtrados.csv",
                mime="text/csv"
            )

with col2:
    st.header("🎬 Video")
    video_file = st.file_uploader("🎞️ Sube un video (.mp4, .mov)", type=["mp4", "mov"])

    if video_file:
        st.subheader("Video cargado")
        st.video(video_file)

        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            tmp_file.write(video_file.read())
            tmp_path = tmp_file.name

        try:
            cap = cv2.VideoCapture(tmp_path)
            if cap.isOpened():
                frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
                fps = cap.get(cv2.CAP_PROP_FPS)
                duration = frames / fps if fps > 0 else 0
                minutes = int(duration // 60)
                seconds = int(duration % 60)
                st.write(f"📁 Nombre del archivo: `{video_file.name}`")
                st.write(f"⏱️ Duración: {minutes} min {seconds} seg")
            cap.release()
        except Exception as e:
            st.warning(f"⚠️ No se pudo obtener información del video: {e}")
        finally:
            os.remove(tmp_path)
