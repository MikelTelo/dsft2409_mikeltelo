"""
Pruebas unitarias para el módulo de preprocesamiento
"""

import unittest
import pandas as pd
import numpy as np
from src.datautilityhub.preprocessing import DataCleaner, FeatureEngineer

class TestDataCleaner(unittest.TestCase):
    def setUp(self):
        # Crear DataFrame de prueba con outliers
        self.df = pd.DataFrame({
            'A': [1, 2, 3, 100, 4, 5],
            'B': [1.1, 2.2, 3.3, 4.4, 5.5, 6.6],
            'C': ['a', 'b', 'c', 'd', 'e', 'f']
        })
        
        # DataFrame con valores nulos
        self.df_null = pd.DataFrame({
            'A': [1, None, 3, None, 5],
            'B': [1.1, 2.2, None, 4.4, 5.5]
        })

    def test_remove_outliers(self):
        df_clean = DataCleaner.remove_outliers(
            self.df, columns=['A'], method='zscore')
        self.assertLess(len(df_clean), len(self.df))

    def test_handle_missing_values(self):
        df_imputed = DataCleaner.handle_missing_values(
            self.df_null, strategy='mean')
        self.assertEqual(df_imputed.isnull().sum().sum(), 0)

    def test_handle_infinite_values(self):
        df_inf = self.df.copy()
        df_inf.loc[0, 'A'] = np.inf
        df_clean = DataCleaner.handle_infinite_values(df_inf)
        self.assertFalse(np.isinf(df_clean['A']).any())

class TestFeatureEngineer(unittest.TestCase):
    def setUp(self):
        # Crear DataFrame con fechas
        self.df_dates = pd.DataFrame({
            'date': pd.date_range(start='2023-01-01', periods=5),
            'value': range(5)
        })
        
        # DataFrame para interacciones
        self.df_interact = pd.DataFrame({
            'A': [1, 2, 3, 4, 5],
            'B': [2, 4, 6, 8, 10]
        })

    def test_create_date_features(self):
        df_features = FeatureEngineer.create_date_features(
            self.df_dates, 'date')
        expected_columns = ['date_year', 'date_month', 'date_day']
        for col in expected_columns:
            self.assertIn(col, df_features.columns)

    def test_create_interaction_features(self):
        df_interactions = FeatureEngineer.create_interaction_features(
            self.df_interact, columns=[('A', 'B')])
        self.assertIn('A_multiply_B', df_interactions.columns)

    def test_encode_categorical(self):
        df = pd.DataFrame({
            'cat': ['a', 'b', 'a', 'c'],
            'target': [0, 1, 0, 1]
        })
        df_encoded = FeatureEngineer.encode_categorical(
            df, columns=['cat'], method='onehot')
        self.assertIn('cat_a', df_encoded.columns)
