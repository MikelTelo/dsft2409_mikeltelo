import pandas as pd
import sys
import os
from pathlib import Path

# Obtener la ruta absoluta del directorio actual
current_dir = Path(__file__).parent.absolute()

# Agregar el directorio src al path
src_path = os.path.join(current_dir, 'src')
if src_path not in sys.path:
    sys.path.insert(0, src_path)

try:
    from datautilityhub.core.eda import DataLoader, NullAnalyzer, DuplicateHandler
    from datautilityhub.utils.visualization import DataVisualizer
    from datautilityhub.utils.preprocessing import DataCleaner, FeatureEngineer
    from datautilityhub.models.ml import ModelEvaluator, ModelOptimizer
except ImportError as e:
    print(f"Error al importar: {e}")
    print(f"Python Path actual: {sys.path}")
    print(f"Directorio actual: {current_dir}")
    print(f"Buscando en: {src_path}")
    sys.exit(1)

def main():
    print("\n=== Ejemplo de uso de DataUtilityHub ===")
    
    # 1. Crear un DataFrame de ejemplo
    data = {
        'edad': [25, 30, None, 40, 45, 28, 32, 38, 42, 47],
        'salario': [30000, 45000, 50000, None, 70000, 35000, 48000, 55000, 65000, 75000],
        'experiencia': [1, 5, 7, 10, None, 2, 6, 8, 12, 17],
        'satisfaccion': [7, None, 6, 8, 9, 7, 8, 7, None, 9],
        'departamento': ['IT', 'HR', 'IT', 'Finance', 'IT', None, 'Finance', 'IT', 'HR', 'Finance']
    }
    df = pd.DataFrame(data)
    
    # 2. Análisis Exploratorio
    print("\n=== Análisis de Valores Nulos ===")
    null_info, recomendaciones = NullAnalyzer.null_analysis(df, show_plot=True)
    print("\nRecomendaciones para manejo de nulos:")
    for col, rec in recomendaciones.items():
        print(f"{col}: {rec}")
    
    # 3. Visualizaciones
    print("\n=== Generando Visualizaciones ===")
    print("Generando matriz de correlación...")
    # Seleccionar solo columnas numéricas para la correlación
    numeric_columns = ['edad', 'salario', 'experiencia', 'satisfaccion']
    DataVisualizer.plot_correlation_matrix(df[numeric_columns], interactive=True)
    
    print("Generando distribuciones...")
    DataVisualizer.plot_distribution(df, columns=['edad', 'salario', 'experiencia'])
    
    # 4. Preprocesamiento
    print("\n=== Preprocesamiento de Datos ===")
    
    # Limpieza de datos
    print("Removiendo outliers...")
    df_clean = DataCleaner.remove_outliers(
        df, 
        columns=['salario', 'experiencia'], 
        method='zscore'
    )
    
    # Feature Engineering
    print("Codificando variables categóricas...")
    df_encoded = FeatureEngineer.encode_categorical(
        df_clean,
        columns=['departamento'],
        method='onehot'
    )
    
    # 5. Machine Learning (ejemplo con datos simulados)
    print("\n=== Ejemplo de Machine Learning ===")
    from sklearn.model_selection import train_test_split
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.metrics import mean_squared_error, r2_score
    
    # Preparar datos
    X = df_encoded.drop(['salario'], axis=1)
    y = df_encoded['salario']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Crear y entrenar modelo
    model = RandomForestRegressor(random_state=42)
    model.fit(X_train, y_train)
    
    # Evaluar modelo
    print("Evaluando modelo...")
    evaluator = ModelEvaluator()
    metrics = evaluator.evaluate_model(
        model, X_train, X_test, y_train, y_test,
        task_type='regression',
        model_name="Random Forest"
    )
    
    # Optimizar hiperparámetros
    print("\nOptimizando hiperparámetros...")
    param_grid = {
        'n_estimators': [50, 100],
        'max_depth': [None, 10],
        'min_samples_split': [2, 5]
    }
    
    best_model, results = ModelOptimizer.optimize_hyperparameters(
        RandomForestRegressor(),
        X, y,
        param_grid=param_grid,
        method='grid',
        scoring='neg_mean_squared_error'
    )
    
    print("\nMejores parámetros encontrados:")
    print(results['best_params'])
    
    print("\nAnálisis completado. Revisa las visualizaciones generadas.")

if __name__ == "__main__":
    main()
