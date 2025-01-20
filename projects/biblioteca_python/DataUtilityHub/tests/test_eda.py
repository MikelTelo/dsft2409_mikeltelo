"""
Pruebas unitarias para el módulo EDA
"""

import unittest
import pandas as pd
import numpy as np
from src.datautilityhub.eda import DataLoader, NullAnalyzer, DuplicateHandler
import os
import tempfile

class TestDataLoader(unittest.TestCase):
    def setUp(self):
        # Crear un DataFrame de prueba
        self.df = pd.DataFrame({
            'A': [1, 2, 3, 4, 5],
            'B': ['a', 'b', 'c', 'd', 'e'],
            'C': [1.1, 2.2, 3.3, 4.4, 5.5]
        })
        
        # Crear un directorio temporal para las pruebas
        self.test_dir = tempfile.mkdtemp()
        self.csv_path = os.path.join(self.test_dir, 'test.csv')
        self.df.to_csv(self.csv_path, index=False)

    def test_cargar_csv_de_directorio(self):
        df_loaded = DataLoader.cargar_csv_de_directorio(self.test_dir)
        pd.testing.assert_frame_equal(df_loaded, self.df)

    def tearDown(self):
        # Limpiar archivos temporales
        os.remove(self.csv_path)
        os.rmdir(self.test_dir)

class TestNullAnalyzer(unittest.TestCase):
    def setUp(self):
        # Crear DataFrame con valores nulos
        self.df = pd.DataFrame({
            'A': [1, None, 3, None, 5],
            'B': ['a', 'b', None, 'd', 'e'],
            'C': [1.1, 2.2, 3.3, None, 5.5]
        })

    def test_null_analysis(self):
        null_info, recomendaciones = NullAnalyzer.null_analysis(self.df, show_plot=False)
        
        self.assertEqual(null_info.loc['A', 'Nulos'], 2)
        self.assertEqual(null_info.loc['B', 'Nulos'], 1)
        self.assertEqual(null_info.loc['C', 'Nulos'], 1)
        
        self.assertIsInstance(recomendaciones, dict)

class TestDuplicateHandler(unittest.TestCase):
    def setUp(self):
        # Crear DataFrame con duplicados
        self.df = pd.DataFrame({
            'A': [1, 2, 2, 3, 3],
            'B': ['a', 'b', 'b', 'c', 'c'],
            'C': [1.1, 2.2, 2.2, 3.3, 3.3]
        })

    def test_find_duplicates(self):
        duplicados = DuplicateHandler.find_duplicates(self.df)
        self.assertEqual(len(duplicados), 2)

    def test_remove_duplicates(self):
        df_limpio = DuplicateHandler.remove_duplicates(self.df)
        self.assertEqual(len(df_limpio), 3)

    def test_get_duplicate_stats(self):
        stats = DuplicateHandler.get_duplicate_stats(self.df)
        self.assertEqual(stats['total_rows'], 5)
        self.assertEqual(stats['unique_rows'], 3)
