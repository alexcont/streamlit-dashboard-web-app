import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dashboard de Datos y Video", layout="wide")
st.title("📊 Dashboard interactivo de Excel + 🎥 Video")

col1, col2 = st.columns(2)

with col1:
    st.header("📈 Gráficas")
    archivos_excel = st.file_uploader(
        "📂 Sube archivos Excel (puedes seleccionar varios)",
        type=["xlsx", "xls"],
        accept_multiple_files=True
    )

    if archivos_excel:
        nombres_excel = [file.name for file in archivos_excel]
        seleccionado = st.selectbox("Selecciona un archivo para graficar", nombres_excel)
        archivo_seleccionado = next(file for file in archivos_excel if file.name == seleccionado)
        df = pd.read_excel(archivo_seleccionado)

        columnas = df.columns.tolist()
        x_col = st.selectbox("📌 Columna X", columnas, index=0)
        y_col = st.selectbox("📌 Columna Y", columnas, index=1 if len(columnas) > 1 else 0)

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
                file_name=f"{seleccionado}_datos_filtrados.csv",
                mime="text/csv"
            )

        st.subheader("👁️ Vista previa de datos")
        st.dataframe(df, use_container_width=True)

with col2:
    st.header("🎬 Videos")
    archivos_video = st.file_uploader(
        "🎞️ Sube archivos de video (.mp4, .mov) (varios)",
        type=["mp4", "mov"],
        accept_multiple_files=True
    )

    if archivos_video:
        nombres_video = [file.name for file in archivos_video]
        seleccionado_vid = st.selectbox("Selecciona un video para reproducir", nombres_video)
        video_seleccionado = next(file for file in archivos_video if file.name == seleccionado_vid)
        st.subheader(f"Reproduciendo: {seleccionado_vid}")
        st.video(video_seleccionado)
