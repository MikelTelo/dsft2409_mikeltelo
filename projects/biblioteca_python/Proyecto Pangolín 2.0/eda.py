import os
import pandas as pd
from IPython.display import display
import folium
import subprocess
import sys

def cargar_csv_de_directorio_y_analisis_basico(directorio):
    """
    Esta función carga automáticamente el primer archivo CSV encontrado en el directorio dado,
    muestra el DataFrame cargado, y luego genera un análisis del mismo paso a paso.
    
    :param directorio: Ruta del directorio donde buscar los archivos CSV.
    :return: Un DataFrame de Pandas con los datos del primer archivo CSV encontrado.
    """
    # Verificamos si la ruta proporcionada es un directorio válido
    if not os.path.isdir(directorio):
        raise ValueError(f"La ruta proporcionada no es un directorio válido: {directorio}")
    
    # Listamos todos los archivos en el directorio
    archivos = os.listdir(directorio)
    
    # Filtramos los archivos CSV
    csv_archivos = [archivo for archivo in archivos if archivo.endswith('.csv')]
    
    if not csv_archivos:
        raise FileNotFoundError("No se encontraron archivos CSV en el directorio especificado.")
    
    # Tomamos el primer archivo CSV encontrado (Solo el primero)
    archivo_csv = csv_archivos[0]
    
    # Realizamos la ruta completa del archivo CSV
    ruta_csv = os.path.join(directorio, archivo_csv)
    
    # Cargamos el archivo CSV con Pandas
    try:
        df = pd.read_csv(ruta_csv)
        print(f"\n{'#' * 50}")
        print(f"# {'Archivo CSV cargado: ' + ruta_csv.center(40)} #")
        print(f"{'#' * 50}")
        
        # Mostrar el DataFrame completo (esto puede ser grande, ten en cuenta)
        print("\n" + "="*50)
        print(f"  {'DataFrame cargado'.center(50)}  ")
        print("="*50)
        display(df)  # Imprime todo el DataFrame (esto puede ser muy grande, por lo que podrías usar df.head())
        
        print("\n" + "="*50)
        print(f"  {'Primeras filas del DataFrame'.center(50)}  ")
        print("="*50)
        display(df.head())  # Ahora imprimimos explícitamente el .head()
        
        print("\n" + "="*50)
        print(f"  {'Información del DataFrame'.center(50)}  ")
        print("="*50)
        df.info()  # Esto ya imprime el resumen de la estructura del DataFrame
        
        print("\n" + "="*50)
        print(f"  {'Descripción estadística del DataFrame'.center(50)}  ")
        print("="*50)
        display(df.describe())  # Asegúrate de imprimir explícitamente el resultado de describe
        
        print("\n" + "="*50)
        print(f"  {'Conteo de valores únicos por columna'.center(50)}  ")
        print("="*50)
        for columna in df.columns:
            print(f"\n{columna} - {'Valores únicos:'.upper()}")
            print(df[columna].value_counts())  # Imprimir conteo de valores únicos
        
        return df
    except Exception as e:
        raise Exception(f"Hubo un error al cargar el archivo CSV: {str(e)}")
    
def find_duplicates(df):
    """
    Finds duplicate rows in a DataFrame.
    Parameters:
    df (pd.DataFrame): The DataFrame to check for duplicates.
    Returns:
    pd.DataFrame: A DataFrame containing duplicate rows.
    """
    return df[df.duplicated()]

def import_eda_libraries():
    """
    Imports the most common libraries for Exploratory Data Analysis (EDA)
    and configures them for optimal use.
    """
    global pd, np, plt, sns, missingno, statsmodels, sp, go, profile, ce, phik, yellowbrick
    try:
        # :gráfico_de_barras: Data Manipulation and Processing
        import pandas as pd       # Tabular data manipulation
        import numpy as np        # Numerical operations
        import scipy as sp        # Mathematical and statistical calculations
        # :gráfico_con_tendencia_ascendente: Visualization
        import matplotlib.pyplot as plt  # Basic plots
        import seaborn as sns     # Advanced statistical plots
        import plotly.graph_objects as go  # Interactive plots
        import missingno          # Visualization of missing data patterns
        # :gráfico_de_barras: Statistical Analysis
        import statsmodels.api as sm  # Statistical models
        # :pestañas_de_marcadores: Data Profiling
        from ydata_profiling import ProfileReport as profile  # Automatic data profiling reports
        # :etiqueta: Categorical Variable Encoding
        import category_encoders as ce  # Advanced encoding methods for categorical variables
        # :eslabón: Correlation Analysis
        import phik  # Correlation analysis between categorical and numerical variables
        # :gráfico_de_barras: Multivariate Analysis
        import yellowbrick  # Visualization of ML metrics and data patterns
        # :engranaje: Basic Configurations
        sns.set(style="whitegrid")
        plt.style.use('ggplot')
        pd.options.display.float_format = '{:.2f}'.format  # Display floats with two decimals
        print(":marca_de_verificación_blanca: All libraries for EDA have been successfully imported.")
    except ImportError as e:
        print(f":x: Error importing libraries: {e}")
        print(":flechas_en_sentido_antihorario: Make sure you have executed the library installation function first.")


def install_ml_libraries():
    """
    Installs the most common libraries for Machine Learning, excluding less frequently used ones.
    """
    libraries = [
        # :gráfico_de_barras: Data Manipulation and Processing
        'numpy',              # Numerical operations
        'pandas',             # Tabular data manipulation
        'scipy',              # Mathematical and statistical calculations
        # :gráfico_con_tendencia_ascendente: Visualization
        'matplotlib',         # Static plots
        'seaborn',            # Advanced visualization
        'plotly',             # Interactive plots
        # :cara_de_robot: General Machine Learning
        'scikit-learn',       # Classic Machine Learning algorithms
        'xgboost',            # Gradient Boosting for tabular data
        'lightgbm',           # Efficient Gradient Boosting
        'catboost',           # Optimized Gradient Boosting
        # :cerebro: Deep Learning
        'tensorflow',         # Neural networks and Deep Learning
        'keras',              # High-level API for TensorFlow
        'torch',              # Deep Learning framework (PyTorch)
        'transformers',       # Advanced NLP models (BERT, GPT, etc.)
        # :lupa: Model Optimization
        'optuna',             # Hyperparameter optimization
        'hyperopt',           # Alternative for hyperparameter optimization
        # :paquete: Model Tracking and Management
        'mlflow',             # ML experiment tracking
        'dvc',               # Data version control
        # :gráfico_de_barras: Statistical Analysis
        'statsmodels',        # Statistical models
        # :engranaje: Text and NLP Processing
        'nltk',              # Natural Language Processing
        'spacy',             # Efficient NLP processing
        # :edificio_en_construcción: Data Processing
        'imblearn',           # Handling imbalanced data
        'joblib',            # Model serialization
        # :gráfico_de_barras: Visualization and Analysis
        'yellowbrick',        # ML metrics visualization
        # :escudo: Model Validation
        'shap',              # Model interpretability
        'lime',              # Local interpretation of predictions
        # :eslabón: Neural Network Graphs
        'networkx',           # Graph modeling and analysis
        # :alto_voltaje: Parallel Computing
        'dask',              # Parallel data processing
        'ray',               # Distributed ML tasks and models
        # :pestañas_de_marcadores: Feature Engineering
        'feature-engine',    # Advanced feature transformations
    ]
    for library in libraries:
        try:
            __import__(library)
            print(f":marca_de_verificación_blanca: The library '{library}' is already installed.")
        except ImportError:
            print(f":advertencia: Installing '{library}'...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", library])
    print("\n:cohete: All necessary libraries for Machine Learning are installed and ready to use.")
    
    
def import_ml_libraries():
    """
    Imports the most common libraries for Machine Learning and sets up basic configurations.
    """
    global pd, np, plt, sns, go
    global tf, keras, xgb, lgb, cb, sm, sp, torch, transformers
    global train_test_split, GridSearchCV, RandomizedSearchCV
    global accuracy_score, confusion_matrix, classification_report
    global optuna, shap, lime, dask, ray, imblearn
    global feature_engine
    try:
        # :gráfico_de_barras: Data Manipulation
        import pandas as pd       # Tabular data manipulation
        import numpy as np        # Numerical operations
        import scipy as sp        # Mathematical and statistical calculations
        # :gráfico_con_tendencia_ascendente: Visualization
        import matplotlib.pyplot as plt  # Basic plots
        import seaborn as sns     # Advanced statistical plots
        import plotly.graph_objects as go  # Interactive plots
        # :cara_de_robot: Machine Learning
        import sklearn
        from sklearn.model_selection import train_test_split, GridSearchCV, RandomizedSearchCV
        from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
        import xgboost as xgb     # Gradient Boosting
        import lightgbm as lgb    # Efficient Gradient Boosting
        import catboost as cb     # Optimized Gradient Boosting
        # :cerebro: Deep Learning
        import tensorflow as tf   # Neural networks
        from tensorflow import keras
        import torch              # Deep Learning framework
        from transformers import pipeline  # NLP models (GPT, BERT)
        # :lupa: Model Optimization
        import optuna             # Hyperparameter optimization
        # :escudo: Model Interpretability
        import shap              # Global interpretability
        import lime              # Local interpretability
        # :alto_voltaje: Parallel Computing
        import dask              # Parallel data processing
        import ray               # Distributed ML models and tasks
        # :edificio_en_construcción: Data Processing
        import imblearn          # Handling imbalanced data (SMOTE, ADASYN)
        import feature_engine    # Advanced feature transformations
        # :gráfico_de_barras: Statistical Analysis
        import statsmodels.api as sm  # Statistical models
        # :engranaje: Basic Configurations
        sns.set(style="whitegrid")
        plt.style.use('ggplot')
        pd.options.display.float_format = '{:.2f}'.format  # Display floats with two decimal places
        print(":marca_de_verificación_blanca: All libraries for Machine Learning have been successfully imported.")
    except ImportError as e:
        print(f":x: Error importing libraries: {e}")
        print(":flechas_en_sentido_antihorario: Make sure you have executed the library installation function first.")
        


    
