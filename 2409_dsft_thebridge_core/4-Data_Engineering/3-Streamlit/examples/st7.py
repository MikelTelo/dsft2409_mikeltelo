# -*- coding: utf-8 -*-
"""
Created on Fri Jan 21 02:24:17 2022

@author: 34632
"""

import numpy as np
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# Cargar los datos de iris
iris_data = load_iris()

# Separar las características y el objetivo
features = pd.DataFrame(iris_data.data, columns=iris_data.feature_names)
target = pd.Series(iris_data.target)

# Dividir los datos en entrenamiento y prueba
x_train, x_test, y_train, y_test = train_test_split(
    features, target, test_size=0.2, stratify=target
)

# Entrenar el modelo
model = RandomForestClassifier()
model.fit(x_train, y_train)

# Construir la barra lateral
cols = [col for col in features.columns]

st.sidebar.markdown(
    '<p class="header-style">Iris Data Classification</p>',
    unsafe_allow_html=True
)

sepal_length = st.sidebar.selectbox(
    f"Select {cols[0]}",
    sorted(features[cols[0]].unique())
)

sepal_width = st.sidebar.selectbox(
    f"Select {cols[1]}",
    sorted(features[cols[1]].unique())
)

petal_length = st.sidebar.selectbox(
    f"Select {cols[2]}",
    sorted(features[cols[2]].unique())
)

petal_width = st.sidebar.selectbox(
    f"Select {cols[3]}",
    sorted(features[cols[3]].unique())
)

values = [sepal_length, sepal_width, petal_length, petal_width]
values_to_predict = np.array(values).reshape(1, -1)

# Realizar la predicción
prediction = model.predict(values_to_predict)
prediction_str = iris_data.target_names[prediction[0]]
probabilities = model.predict_proba(values_to_predict)

# Estilo para la aplicación
st.markdown(
    """
    <style>
    .header-style {
        font-size:25px;
        font-family:sans-serif;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <style>
    .font-style {
        font-size:20px;
        font-family:sans-serif;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Mostrar los resultados
st.markdown(
    '<p class="header-style"> Iris Data Predictions </p>',
    unsafe_allow_html=True
)

column_1, column_2 = st.columns(2)
column_1.markdown(
    f'<p class="font-style" >Prediction </p>',
    unsafe_allow_html=True
)
column_1.write(f"{prediction_str}")

column_2.markdown(
    '<p class="font-style" >Probability </p>',
    unsafe_allow_html=True
)
column_2.write(f"{probabilities[0][prediction[0]]}")

# Crear gráfico de pastel
fig = go.Figure(
    data=[go.Pie(
        labels=list(iris_data.target_names),
        values=probabilities[0]
    )]
)
fig = fig.update_traces(
    hoverinfo='label+percent',
    textinfo='value',
    textfont_size=15
)

st.markdown(
    '<p class="font-style" >Probability Distribution</p>',
    unsafe_allow_html=True
)
st.plotly_chart(fig, use_container_width=True)
