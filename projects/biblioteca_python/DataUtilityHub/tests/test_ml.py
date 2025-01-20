"""
Pruebas unitarias para el módulo de Machine Learning
"""

import unittest
import pandas as pd
import numpy as np
from sklearn.datasets import make_classification, make_regression
from sklearn.linear_model import LogisticRegression, LinearRegression
from src.datautilityhub.ml import ModelEvaluator, ModelOptimizer, ModelPersistence
import os
import tempfile

class TestModelEvaluator(unittest.TestCase):
    def setUp(self):
        # Crear datos de clasificación
        X_class, y_class = make_classification(
            n_samples=100, n_features=4, random_state=42)
        self.X_train_class = X_class[:80]
        self.X_test_class = X_class[80:]
        self.y_train_class = y_class[:80]
        self.y_test_class = y_class[80:]
        
        # Crear datos de regresión
        X_reg, y_reg = make_regression(
            n_samples=100, n_features=4, random_state=42)
        self.X_train_reg = X_reg[:80]
        self.X_test_reg = X_reg[80:]
        self.y_train_reg = y_reg[:80]
        self.y_test_reg = y_reg[80:]
        
        self.evaluator = ModelEvaluator()

    def test_evaluate_classification_model(self):
        model = LogisticRegression()
        model.fit(self.X_train_class, self.y_train_class)
        
        metrics = self.evaluator.evaluate_model(
            model,
            self.X_train_class,
            self.X_test_class,
            self.y_train_class,
            self.y_test_class,
            task_type='classification'
        )
        
        self.assertIn('accuracy_test', metrics)
        self.assertIn('precision', metrics)
        self.assertIn('recall', metrics)

    def test_evaluate_regression_model(self):
        model = LinearRegression()
        model.fit(self.X_train_reg, self.y_train_reg)
        
        metrics = self.evaluator.evaluate_model(
            model,
            self.X_train_reg,
            self.X_test_reg,
            self.y_train_reg,
            self.y_test_reg,
            task_type='regression'
        )
        
        self.assertIn('mse_test', metrics)
        self.assertIn('r2', metrics)

class TestModelOptimizer(unittest.TestCase):
    def setUp(self):
        # Crear datos de prueba
        X, y = make_classification(n_samples=100, n_features=4, random_state=42)
        self.X = X
        self.y = y
        
        self.param_grid = {
            'C': [0.1, 1, 10],
            'max_iter': [100, 200]
        }

    def test_optimize_hyperparameters(self):
        model = LogisticRegression()
        best_model, results = ModelOptimizer.optimize_hyperparameters(
            model, self.X, self.y, self.param_grid)
        
        self.assertIsInstance(best_model, LogisticRegression)
        self.assertIn('best_params', results)
        self.assertIn('best_score', results)

    def test_cross_validate_model(self):
        model = LogisticRegression()
        results = ModelOptimizer.cross_validate_model(
            model, self.X, self.y, scoring=['accuracy', 'precision'])
        
        self.assertIn('accuracy', results)
        self.assertIn('precision', results)

class TestModelPersistence(unittest.TestCase):
    def setUp(self):
        self.model = LogisticRegression()
        X, y = make_classification(n_samples=100, n_features=4, random_state=42)
        self.model.fit(X, y)
        self.temp_dir = tempfile.mkdtemp()

    def test_save_and_load_model(self):
        # Guardar modelo
        save_path = ModelPersistence.save_model(
            self.model, 'test_model', include_timestamp=False)
        
        # Cargar modelo
        loaded_model = ModelPersistence.load_model(save_path)
        
        # Verificar que es el mismo tipo de modelo
        self.assertIsInstance(loaded_model, LogisticRegression)
        
        # Verificar que los parámetros son iguales
        self.assertEqual(
            self.model.get_params(),
            loaded_model.get_params()
        )

    def tearDown(self):
        # Limpiar archivos temporales
        for file in os.listdir(self.temp_dir):
            os.remove(os.path.join(self.temp_dir, file))
        os.rmdir(self.temp_dir)

if __name__ == '__main__':
    unittest.main()
