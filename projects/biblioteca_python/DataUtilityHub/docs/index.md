# DataUtilityHub Documentation

![DataUtilityHub Logo](../resources/img/pangolin_logo.jpeg)

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](https://opensource.org/licenses/MIT)

## Estructura del Proyecto

```
DataUtilityHub/
├── src/
│   └── datautilityhub/
│       ├── core/          # Funcionalidades principales
│       ├── utils/         # Utilidades y helpers
│       └── models/        # Modelos y algoritmos
├── tests/
│   ├── unit/             # Tests unitarios
│   └── integration/      # Tests de integración
├── docs/
│   ├── api/              # Documentación de la API
│   └── examples/         # Ejemplos de uso
└── resources/            # Recursos (imágenes, etc.)
```

## Installation

```bash
# Instalación local
pip install .

# O en modo desarrollo
pip install -e .
```

## Quick Start

```python
from datautilityhub.core import DataLoader, NullAnalyzer
from datautilityhub.utils import DataVisualizer
from datautilityhub.models import ModelEvaluator

# Cargar datos
df = DataLoader.load_csv_from_directory('data/')

# Analizar nulos
null_stats, metrics = NullAnalyzer.analyze_nulls(df)

# Crear visualizaciones
DataVisualizer.plot_correlation_matrix(df)

# Evaluar modelo
metrics = ModelEvaluator.evaluate_model(model, X_test, y_test)
```

## Módulos Principales

### Core
- `DataLoader`: Carga y gestión de datos
- `NullAnalyzer`: Análisis de valores nulos
- `DuplicateHandler`: Gestión de duplicados

### Utils
- `DataVisualizer`: Visualizaciones
- `DataCleaner`: Limpieza de datos
- `FeatureEngineer`: Ingeniería de características

### Models
- `ModelEvaluator`: Evaluación de modelos
- `ModelOptimizer`: Optimización de hiperparámetros
- `ModelPersistence`: Gestión de modelos

## Documentación Detallada

- [API Reference](api/index.md)
- [Ejemplos](examples/index.md)
- [Guía de Contribución](../CONTRIBUTING.md)

## Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](../LICENSE) para más detalles.

## Support

- Documentation: [https://datautilityhub.readthedocs.io](https://datautilityhub.readthedocs.io)
- Issue Tracker: [GitHub Issues](https://github.com/yourusername/DataUtilityHub/issues)
- Source Code: [GitHub Repository](https://github.com/yourusername/DataUtilityHub) 