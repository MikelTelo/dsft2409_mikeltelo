"""
DataUtilityHub - Una biblioteca para simplificar el análisis exploratorio de datos y machine learning
"""

# Core functionality
from .core.eda import DataLoader, NullAnalyzer, DuplicateHandler

# Utilities
from .utils.visualization import DataVisualizer
from .utils.preprocessing import DataCleaner, FeatureEngineer

# Models
from .models.ml import ModelEvaluator, ModelOptimizer, ModelPersistence

__version__ = "0.1.0"

__all__ = [
    'DataLoader',
    'NullAnalyzer',
    'DuplicateHandler',
    'DataVisualizer',
    'DataCleaner',
    'FeatureEngineer',
    'ModelEvaluator',
    'ModelOptimizer',
    'ModelPersistence'
]
