# -*- coding: utf-8 -*-
"""
Script didáctico con Streamlit para predecir la clase de iris usando un Random Forest.
"""

import streamlit as st
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
import numpy as np

# Cargar el dataset Iris
iris = load_iris()

# Entrenar el modelo Random Forest
model = RandomForestClassifier()
model.fit(iris.data, iris.target)

# Título y descripción de la aplicación
st.title("Clasificador de Flores Iris")
st.write("""
Esta aplicación predice la especie de una flor Iris en base a las características que selecciones.
""")

# Entrada de datos del usuario
st.header("Introduce las características de la flor:")
sepal_length = st.slider("Longitud del sépalo (cm)", min_value=4.0, max_value=8.0, step=0.1)
sepal_width = st.slider("Ancho del sépalo (cm)", min_value=2.0, max_value=4.5, step=0.1)
petal_length = st.slider("Longitud del pétalo (cm)", min_value=1.0, max_value=7.0, step=0.1)
petal_width = st.slider("Ancho del pétalo (cm)", min_value=0.1, max_value=2.5, step=0.1)

# Preparar los datos para la predicción
input_data = np.array([[sepal_length, sepal_width, petal_length, petal_width]])

# Realizar la predicción
prediction = model.predict(input_data)
prediction_proba = model.predict_proba(input_data)

# Mostrar el resultado
st.header("Resultado de la predicción:")
st.write(f"**Especie Predicha:** {iris.target_names[prediction[0]]}")
st.write("**Probabilidades:**")
for i, prob in enumerate(prediction_proba[0]):
    st.write(f"{iris.target_names[i]}: {prob:.2f}")

# Nota didáctica
st.write("---")
st.write("""
**Nota:** Este ejemplo utiliza un modelo Random Forest preentrenado con el conjunto de datos Iris.
Es una demostración básica para fines educativos.
""")