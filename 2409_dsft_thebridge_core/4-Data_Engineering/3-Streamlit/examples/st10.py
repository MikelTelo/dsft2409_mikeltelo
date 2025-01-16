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


def load_and_split_data():
    """Cargar el dataset Iris y dividirlo en conjuntos de entrenamiento y prueba."""
    iris_data = load_iris()
    features = pd.DataFrame(iris_data.data, columns=iris_data.feature_names)
    target = pd.Series(iris_data.target)
    x_train, x_test, y_train, y_test = train_test_split(
        features, target, test_size=0.2, stratify=target
    )
    return iris_data, features, x_train, x_test, y_train, y_test


def train_model(x_train, y_train):
    """Entrenar el modelo de Random Forest."""
    model = RandomForestClassifier()
    model.fit(x_train, y_train)
    return model


def construct_sidebar(features):
    """Construir la barra lateral de selección en Streamlit."""
    cols = [col for col in features.columns]
    st.sidebar.markdown(
        '<p class="header-style">Iris Data Classification</p>',
        unsafe_allow_html=True
    )

    # Crear selectores para cada característica
    inputs = []
    for col in cols:
        value = st.sidebar.selectbox(f"Select {col}", sorted(features[col].unique()))
        inputs.append(value)

    return inputs


def plot_pie_chart(probabilities, target_names):
    """Graficar un gráfico circular con las probabilidades de predicción."""
    fig = go.Figure(
        data=[go.Pie(
                labels=list(target_names),
                values=probabilities[0]
        )]
    )
    fig = fig.update_traces(
        hoverinfo='label+percent',
        textinfo='value',
        textfont_size=15
    )
    return fig


def display_results(prediction, probabilities, target_names):
    """Mostrar los resultados de predicción en la interfaz de Streamlit."""
    prediction_str = target_names[prediction[0]]
    st.markdown(
        '<p class="header-style"> Iris Data Predictions </p>',
        unsafe_allow_html=True
    )
    column_1, column_2 = st.columns(2)
    column_1.markdown('<p class="font-style">Prediction</p>', unsafe_allow_html=True)
    column_1.write(f"{prediction_str}")

    column_2.markdown('<p class="font-style">Probability</p>', unsafe_allow_html=True)
    column_2.write(f"{probabilities[0][prediction[0]]}")

    fig = plot_pie_chart(probabilities, target_names)
    st.markdown('<p class="font-style">Probability Distribution</p>', unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True)


def main():
    """Función principal para construir la aplicación."""
    st.set_page_config(page_title="Iris Data Classification", layout="centered")

    # Cargar datos y dividirlos
    iris_data, features, x_train, x_test, y_train, y_test = load_and_split_data()

    # Entrenar el modelo
    model = train_model(x_train, y_train)

    # Construir la barra lateral
    user_inputs = construct_sidebar(features)

    # Realizar predicción
    values_to_predict = np.array(user_inputs).reshape(1, -1)
    prediction = model.predict(values_to_predict)
    probabilities = model.predict_proba(values_to_predict)

    # Mostrar resultados
    display_results(prediction, probabilities, iris_data.target_names)


if __name__ == "__main__":
    main()
