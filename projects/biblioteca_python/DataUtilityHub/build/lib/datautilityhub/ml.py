"""
Módulo de Machine Learning
"""

from sklearn.base import BaseEstimator
from sklearn.metrics import (confusion_matrix, classification_report, recall_score,
                           precision_score, f1_score, roc_auc_score, mean_squared_error,
                           r2_score, mean_absolute_error)
from sklearn.model_selection import (cross_val_score, GridSearchCV, RandomizedSearchCV,
                                   train_test_split, KFold, StratifiedKFold)
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import os
from typing import Union, List, Dict, Optional, Tuple
import joblib
from datetime import datetime

class ModelEvaluator:
    """Clase para evaluar modelos de machine learning"""
    
    def evaluate_model(self, 
                      model: BaseEstimator,
                      X_train: Union[pd.DataFrame, np.ndarray],
                      X_test: Union[pd.DataFrame, np.ndarray],
                      y_train: Union[pd.Series, np.ndarray],
                      y_test: Union[pd.Series, np.ndarray],
                      task_type: str = 'classification',
                      model_name: str = "Modelo ML") -> Dict:
        """
        Evalúa un modelo de machine learning y genera reportes detallados.
        
        Args:
            model: Modelo entrenado
            X_train: Datos de entrenamiento
            X_test: Datos de prueba
            y_train: Etiquetas de entrenamiento
            y_test: Etiquetas de prueba
            task_type: Tipo de tarea ('classification' o 'regression')
            model_name: Nombre del modelo
        
        Returns:
            Diccionario con métricas de evaluación
        """
        # Crear directorio de resultados
        results_dir = 'resultados'
        os.makedirs(results_dir, exist_ok=True)
        
        # Realizar predicciones
        y_pred = model.predict(X_test)
        y_pred_train = model.predict(X_train)
        
        # Calcular métricas según el tipo de tarea
        metrics = {}
        if task_type == 'classification':
            metrics = self._evaluate_classification(y_test, y_pred, y_train, y_pred_train)
            self._plot_confusion_matrix(y_test, y_pred, model_name)
            
            # Probabilidades para ROC curve si el modelo lo soporta
            if hasattr(model, 'predict_proba'):
                self._plot_roc_curve(model, X_test, y_test, model_name)
        else:
            metrics = self._evaluate_regression(y_test, y_pred, y_train, y_pred_train)
            self._plot_regression_results(y_test, y_pred, model_name)
        
        # Generar reporte
        self._generate_report(model, metrics, model_name, task_type)
        
        return metrics
    
    def _evaluate_classification(self, y_test, y_pred, y_train, y_pred_train) -> Dict:
        """Evalúa métricas para clasificación"""
        return {
            'accuracy_train': (y_train == y_pred_train).mean(),
            'accuracy_test': (y_test == y_pred).mean(),
            'precision': precision_score(y_test, y_pred, average='weighted'),
            'recall': recall_score(y_test, y_pred, average='weighted'),
            'f1': f1_score(y_test, y_pred, average='weighted'),
            'classification_report': classification_report(y_test, y_pred)
        }
    
    def _evaluate_regression(self, y_test, y_pred, y_train, y_pred_train) -> Dict:
        """Evalúa métricas para regresión"""
        return {
            'mse_train': mean_squared_error(y_train, y_pred_train),
            'mse_test': mean_squared_error(y_test, y_pred),
            'rmse': np.sqrt(mean_squared_error(y_test, y_pred)),
            'mae': mean_absolute_error(y_test, y_pred),
            'r2': r2_score(y_test, y_pred)
        }
    
    def _plot_confusion_matrix(self, y_test, y_pred, model_name) -> None:
        """Genera y guarda la matriz de confusión"""
        plt.figure(figsize=(10, 8))
        cm = confusion_matrix(y_test, y_pred)
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
        plt.title(f'Matriz de Confusión - {model_name}')
        plt.ylabel('Valor Real')
        plt.xlabel('Valor Predicho')
        plt.savefig(f'resultados/confusion_matrix_{model_name.lower().replace(" ", "_")}.png')
        plt.close()
    
    def _plot_roc_curve(self, model, X_test, y_test, model_name) -> None:
        """Genera y guarda la curva ROC"""
        from sklearn.metrics import roc_curve, auc
        y_pred_proba = model.predict_proba(X_test)[:, 1]
        fpr, tpr, _ = roc_curve(y_test, y_pred_proba)
        roc_auc = auc(fpr, tpr)
        
        plt.figure(figsize=(10, 8))
        plt.plot(fpr, tpr, color='darkorange', lw=2, 
                label=f'ROC curve (AUC = {roc_auc:.2f})')
        plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('Tasa de Falsos Positivos')
        plt.ylabel('Tasa de Verdaderos Positivos')
        plt.title(f'Curva ROC - {model_name}')
        plt.legend(loc="lower right")
        plt.savefig(f'resultados/roc_curve_{model_name.lower().replace(" ", "_")}.png')
        plt.close()
    
    def _plot_regression_results(self, y_test, y_pred, model_name) -> None:
        """Genera y guarda gráficos de resultados de regresión"""
        plt.figure(figsize=(10, 8))
        plt.scatter(y_test, y_pred, alpha=0.5)
        plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
        plt.xlabel('Valores Reales')
        plt.ylabel('Predicciones')
        plt.title(f'Predicciones vs Valores Reales - {model_name}')
        plt.savefig(f'resultados/regression_results_{model_name.lower().replace(" ", "_")}.png')
        plt.close()
    
    def _generate_report(self, model, metrics: Dict, model_name: str, task_type: str) -> None:
        """Genera reporte detallado del modelo"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = f'resultados/reporte_{model_name.lower().replace(" ", "_")}_{timestamp}.txt'
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(f"=== Reporte de Evaluación: {model_name} ===\n")
            f.write(f"Fecha y hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            f.write("1. Información del Modelo\n")
            f.write("-" * 50 + "\n")
            if hasattr(model, 'get_params'):
                f.write("Parámetros del modelo:\n")
                for param, value in model.get_params().items():
                    f.write(f"- {param}: {value}\n")
            
            f.write("\n2. Métricas de Rendimiento\n")
            f.write("-" * 50 + "\n")
            if task_type == 'classification':
                f.write(f"Accuracy (Train): {metrics['accuracy_train']:.4f}\n")
                f.write(f"Accuracy (Test): {metrics['accuracy_test']:.4f}\n")
                f.write(f"Precision: {metrics['precision']:.4f}\n")
                f.write(f"Recall: {metrics['recall']:.4f}\n")
                f.write(f"F1-Score: {metrics['f1']:.4f}\n\n")
                f.write("Reporte de Clasificación Detallado:\n")
                f.write(metrics['classification_report'])
            else:
                f.write(f"MSE (Train): {metrics['mse_train']:.4f}\n")
                f.write(f"MSE (Test): {metrics['mse_test']:.4f}\n")
                f.write(f"RMSE: {metrics['rmse']:.4f}\n")
                f.write(f"MAE: {metrics['mae']:.4f}\n")
                f.write(f"R²: {metrics['r2']:.4f}\n")

class ModelOptimizer:
    """NUEVA CLASE: Para optimización de modelos"""
    
    @staticmethod
    def optimize_hyperparameters(model: BaseEstimator,
                               X: Union[pd.DataFrame, np.ndarray],
                               y: Union[pd.Series, np.ndarray],
                               param_grid: Dict,
                               cv: int = 5,
                               scoring: str = 'accuracy',
                               method: str = 'grid',
                               n_iter: int = 100) -> Tuple[BaseEstimator, Dict]:
        """
        Optimiza hiperparámetros usando Grid Search o Random Search.
        
        Args:
            model: Modelo base a optimizar
            X: Datos de entrenamiento
            y: Etiquetas
            param_grid: Diccionario de parámetros a probar
            cv: Número de folds para validación cruzada
            scoring: Métrica para optimización
            method: Método de búsqueda ('grid' o 'random')
            n_iter: Número de iteraciones para random search
            
        Returns:
            Tuple con el mejor modelo y diccionario de resultados
        """
        if method == 'grid':
            search = GridSearchCV(model, param_grid, cv=cv, scoring=scoring, n_jobs=-1)
        else:
            search = RandomizedSearchCV(model, param_grid, n_iter=n_iter, cv=cv, 
                                      scoring=scoring, n_jobs=-1)
        
        search.fit(X, y)
        
        results = {
            'best_params': search.best_params_,
            'best_score': search.best_score_,
            'cv_results': pd.DataFrame(search.cv_results_)
        }
        
        return search.best_estimator_, results

    @staticmethod
    def cross_validate_model(model: BaseEstimator,
                           X: Union[pd.DataFrame, np.ndarray],
                           y: Union[pd.Series, np.ndarray],
                           cv: int = 5,
                           scoring: Union[str, List[str]] = 'accuracy',
                           task_type: str = 'classification') -> Dict:
        """
        Realiza validación cruzada del modelo con múltiples métricas.
        
        Args:
            model: Modelo a evaluar
            X: Datos
            y: Etiquetas
            cv: Número de folds
            scoring: Métrica(s) de evaluación
            task_type: Tipo de tarea ('classification' o 'regression')
            
        Returns:
            Diccionario con resultados de validación cruzada
        """
        if task_type == 'classification':
            cv_splitter = StratifiedKFold(n_splits=cv, shuffle=True, random_state=42)
        else:
            cv_splitter = KFold(n_splits=cv, shuffle=True, random_state=42)
        
        if isinstance(scoring, str):
            scoring = [scoring]
        
        results = {}
        for metric in scoring:
            scores = cross_val_score(model, X, y, cv=cv_splitter, 
                                   scoring=metric, n_jobs=-1)
            results[metric] = {
                'scores': scores,
                'mean': scores.mean(),
                'std': scores.std()
            }
        
        return results

class ModelPersistence:
    """NUEVA CLASE: Para guardar y cargar modelos"""
    
    @staticmethod
    def save_model(model: BaseEstimator,
                  model_name: str,
                  include_timestamp: bool = True) -> str:
        """
        Guarda el modelo en disco.
        
        Returns:
            Ruta donde se guardó el modelo
        """
        save_dir = 'modelos'
        os.makedirs(save_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S") if include_timestamp else ""
        filename = f"{model_name}_{timestamp}.joblib" if timestamp else f"{model_name}.joblib"
        path = os.path.join(save_dir, filename)
        
        joblib.dump(model, path)
        print(f"Modelo guardado en: {path}")
        return path
    
    @staticmethod
    def load_model(path: str) -> BaseEstimator:
        """Carga un modelo guardado"""
        if not os.path.exists(path):
            raise FileNotFoundError(f"No se encontró el modelo en: {path}")
        
        return joblib.load(path)
