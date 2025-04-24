import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dashboard de Datos y Video", layout="wide")
st.title("📊 Dashboard interactivo de Excel + 🎥 Video")

col1, col2 = st.columns(2)

with col1:
    st.header("📈 Gráficas")
    archivo_excel = st.file_uploader("📂 Sube un archivo Excel", type=["xlsx", "xls"], accept_multiple_files=True)

    if archivo_excel:
        for file in archivo_excel:
            df = pd.read_excel(file)
            columnas = df.columns.tolist()

            default_x = columnas[1] if len(columnas) > 1 else None
            default_y = columnas[0] if len(columnas) > 0 else None

            x_col = st.selectbox("📌 Columna X", columnas, index=1 if default_x else None)
            y_col = st.selectbox("📌 Columna Y", columnas, index=0 if default_y else None)

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

        st.subheader("👁️ Vista previa de datos")
        st.dataframe(df, use_container_width=True)

with col2:
    st.header("🎬 Video")
    video_file = st.file_uploader("🎞️ Sube un video (.mp4, .mov)", type=["mp4", "mov"], accept_multiple_files=True)

    if video_file:
        for video in video_file:
            st.subheader(f"Video: {video.name}")
            video_bytes = video.read()
            st.video(video_bytes)  # Sin ajustar el volumen
