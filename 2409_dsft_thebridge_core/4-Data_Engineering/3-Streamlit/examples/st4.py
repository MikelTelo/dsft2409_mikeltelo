# -*- coding: utf-8 -*-
"""
Script didáctico con Streamlit para explorar elementos interactivos y visualizaciones.
"""

import streamlit as st
import pandas as pd
import numpy as np
import time

# Título principal
st.title("Explorando Streamlit:")
st.write("""
Este script muestra cómo utilizar múltiples componentes de Streamlit en una interfaz limpia y organizada.
¡Interactúa con los elementos y descubre sus funcionalidades!
""")

# Divider
st.markdown("---")

# Subtítulo
st.header("1. Entrada de datos")
st.write("Streamlit permite capturar datos de diferentes maneras:")

# Texto de entrada
nombre = st.text_input("¿Cuál es tu nombre?", placeholder="Escribe tu nombre aquí")

# Selector de opción
opcion = st.selectbox(
    "¿Cuál es tu lenguaje de programación favorito?",
    ["Python", "R", "JavaScript", "Java", "C++"]
)

# Deslizador
edad = st.slider("¿Cuál es tu edad?", min_value=0, max_value=100, value=25, step=1)

# Botón
if st.button("Enviar"):
    st.write(f"¡Hola {nombre}! Tu lenguaje favorito es {opcion} y tienes {edad} años.")

# Divider
st.markdown("---")

# Subtítulo
st.header("2. Visualización de datos")
st.write("Streamlit facilita la creación de visualizaciones:")

# Crear un DataFrame aleatorio
data = pd.DataFrame(
    np.random.randn(100, 3),
    columns=["A", "B", "C"]
)

# Mostrar el DataFrame
st.write("Aquí tienes un conjunto de datos aleatorios:")
st.dataframe(data)

# Gráficos
st.write("Y aquí algunos gráficos generados a partir de los datos:")
st.line_chart(data)
st.bar_chart(data)

# Divider
st.markdown("---")

# Subtítulo
st.header("3. Widgets interactivos")
st.write("Explora diferentes elementos interactivos:")

# Multiselección
opciones = st.multiselect(
    "Selecciona las columnas que quieres ver:",
    data.columns.tolist(),
    default=data.columns.tolist()
)

if opciones:
    st.write(f"Mostrando datos para las columnas: {', '.join(opciones)}")
    st.dataframe(data[opciones])
else:
    st.warning("Por favor selecciona al menos una columna.")

# Divider
st.markdown("---")

# Subtítulo
st.header("4. Carga de archivos")
st.write("Permite a los usuarios cargar sus propios archivos:")

# Subir archivo
archivo = st.file_uploader("Sube un archivo CSV", type=["csv"])

if archivo is not None:
    df = pd.read_csv(archivo)
    st.write("Archivo cargado con éxito:")
    st.dataframe(df)

# Divider
st.markdown("---")

# Subtítulo
st.header("5. Animaciones y progreso")
st.write("Incorpora barras de progreso y animaciones:")

# Barra de progreso
st.write("Simulando un proceso en ejecución:")
progress_bar = st.progress(0)

for i in range(101):
    time.sleep(0.1)
    progress_bar.progress(i)

st.success("¡Proceso completado!")

# Divider
st.markdown("---")

# Subtítulo
st.header("6. Mensajes informativos")
st.write("Streamlit permite mostrar mensajes útiles:")

st.info("Esto es un mensaje informativo.")
st.success("¡Operación exitosa!")
st.warning("Esto es una advertencia.")
st.error("Ha ocurrido un error.")
st.exception(RuntimeError("Este es un error de ejemplo."))

# Divider
st.markdown("---")

# Subtítulo final
st.header("Conclusión")
st.write("""
En este script hemos explorado diferentes elementos de Streamlit.
Puedes usar estas herramientas para construir aplicaciones web interactivas y efectivas.
""")
