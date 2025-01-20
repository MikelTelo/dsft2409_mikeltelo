"""
Pruebas unitarias para el módulo de visualización
"""

import unittest
import pandas as pd
import numpy as np
from src.datautilityhub.visualization import DataVisualizer
import matplotlib.pyplot as plt

class TestDataVisualizer(unittest.TestCase):
    def setUp(self):
        # Crear DataFrame de prueba
        np.random.seed(42)
        self.df = pd.DataFrame({
            'A': np.random.normal(0, 1, 100),
            'B': np.random.normal(0, 1, 100),
            'C': ['cat1', 'cat2'] * 50
        })

    def test_plot_correlation_matrix(self):
        # Verificar que no hay errores al generar la matriz
        try:
            DataVisualizer.plot_correlation_matrix(
                self.df.select_dtypes(include=[np.number]))
            plt.close()
        except Exception as e:
            self.fail(f"plot_correlation_matrix raised {type(e)} unexpectedly!")

    def test_plot_distribution(self):
        try:
            DataVisualizer.plot_distribution(self.df, columns=['A', 'B'])
            plt.close()
        except Exception as e:
            self.fail(f"plot_distribution raised {type(e)} unexpectedly!")

    def test_plot_categorical_analysis(self):
        try:
            DataVisualizer.plot_categorical_analysis(
                self.df, 'C', value_column='A')
            plt.close()
        except Exception as e:
            self.fail(f"plot_categorical_analysis raised {type(e)} unexpectedly!")

    def test_plot_time_series(self):
        # Crear DataFrame con series temporales
        dates = pd.date_range(start='2023-01-01', periods=100, freq='D')
        df_ts = pd.DataFrame({
            'date': dates,
            'value': np.random.normal(0, 1, 100)
        })
        
        try:
            DataVisualizer.plot_time_series(
                df_ts, 'date', 'value')
            plt.close()
        except Exception as e:
            self.fail(f"plot_time_series raised {type(e)} unexpectedly!")
