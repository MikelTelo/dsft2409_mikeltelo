"""
Módulo de Preprocesamiento de Datos
"""

import pandas as pd
import numpy as np
from typing import Union, List, Optional, Tuple, Dict
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler
from sklearn.impute import SimpleImputer, KNNImputer
from category_encoders import TargetEncoder, WOEEncoder
import category_encoders as ce

class DataCleaner:
    """Clase para limpieza de datos"""
    
    @staticmethod
    def remove_outliers(df: pd.DataFrame, 
                       columns: List[str], 
                       method: str = 'zscore', 
                       threshold: float = 3) -> pd.DataFrame:
        """
        Elimina outliers usando diferentes métodos.
        
        Args:
            df: DataFrame a limpiar
            columns: Columnas a analizar
            method: Método ('zscore' o 'iqr')
            threshold: Umbral para considerar outlier
        """
        df = df.copy()
        
        if method == 'zscore':
            for col in columns:
                z_scores = np.abs((df[col] - df[col].mean()) / df[col].std())
                df = df[z_scores < threshold]
        
        elif method == 'iqr':
            for col in columns:
                Q1 = df[col].quantile(0.25)
                Q3 = df[col].quantile(0.75)
                IQR = Q3 - Q1
                df = df[~((df[col] < (Q1 - threshold * IQR)) | 
                         (df[col] > (Q3 + threshold * IQR)))]
        
        return df
    
    @staticmethod
    def handle_missing_values(df: pd.DataFrame, 
                            strategy: Union[str, Dict] = 'mean',
                            method: str = 'simple') -> pd.DataFrame:
        """
        Maneja valores faltantes con diferentes estrategias.
        
        Args:
            df: DataFrame a procesar
            strategy: Estrategia de imputación o diccionario de estrategias por columna
            method: Método de imputación ('simple' o 'knn')
        """
        df = df.copy()
        
        if isinstance(strategy, str):
            if method == 'simple':
                imputer = SimpleImputer(strategy=strategy)
                df_imputed = pd.DataFrame(imputer.fit_transform(df), columns=df.columns)
            elif method == 'knn':
                imputer = KNNImputer(n_neighbors=5)
                df_imputed = pd.DataFrame(imputer.fit_transform(df), columns=df.columns)
        else:
            df_imputed = df.copy()
            for col, strat in strategy.items():
                if col in df.columns:
                    imputer = SimpleImputer(strategy=strat)
                    df_imputed[col] = imputer.fit_transform(df[[col]])
        
        return df_imputed

    @staticmethod
    def handle_infinite_values(df: pd.DataFrame, 
                             replacement: Union[str, float] = 'mean') -> pd.DataFrame:
        """
        NUEVA FUNCIÓN: Maneja valores infinitos en el DataFrame.
        
        Args:
            df: DataFrame a procesar
            replacement: Valor de reemplazo o estrategia ('mean', 'median', 'max', 'min')
        """
        df = df.copy()
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        
        for col in numeric_cols:
            mask = np.isinf(df[col])
            if mask.any():
                if isinstance(replacement, str):
                    if replacement == 'mean':
                        val = df[col][~np.isinf(df[col])].mean()
                    elif replacement == 'median':
                        val = df[col][~np.isinf(df[col])].median()
                    elif replacement == 'max':
                        val = df[col][~np.isinf(df[col])].max()
                    elif replacement == 'min':
                        val = df[col][~np.isinf(df[col])].min()
                else:
                    val = replacement
                df.loc[mask, col] = val
        
        return df

class FeatureEngineer:
    """Clase para ingeniería de características"""
    
    @staticmethod
    def create_date_features(df: pd.DataFrame, 
                           date_column: str) -> pd.DataFrame:
        """
        Crea características a partir de una columna de fecha.
        """
        df = df.copy()
        df[date_column] = pd.to_datetime(df[date_column])
        
        # Extraemos características de fecha
        df[f'{date_column}_year'] = df[date_column].dt.year
        df[f'{date_column}_month'] = df[date_column].dt.month
        df[f'{date_column}_day'] = df[date_column].dt.day
        df[f'{date_column}_dayofweek'] = df[date_column].dt.dayofweek
        df[f'{date_column}_quarter'] = df[date_column].dt.quarter
        df[f'{date_column}_is_weekend'] = df[date_column].dt.dayofweek.isin([5, 6]).astype(int)
        df[f'{date_column}_is_month_end'] = df[date_column].dt.is_month_end.astype(int)
        df[f'{date_column}_is_month_start'] = df[date_column].dt.is_month_start.astype(int)
        
        return df
    
    @staticmethod
    def create_interaction_features(df: pd.DataFrame, 
                                  columns: List[tuple], 
                                  operation: str = 'multiply') -> pd.DataFrame:
        """
        Crea características de interacción entre columnas.
        """
        df = df.copy()
        operations = {
            'multiply': lambda x, y: x * y,
            'divide': lambda x, y: x / y,
            'add': lambda x, y: x + y,
            'subtract': lambda x, y: x - y,
            'mean': lambda x, y: (x + y) / 2,
            'max': lambda x, y: np.maximum(x, y),
            'min': lambda x, y: np.minimum(x, y)
        }
        
        for col1, col2 in columns:
            new_col = f'{col1}_{operation}_{col2}'
            df[new_col] = operations[operation](df[col1], df[col2])
        
        return df

    @staticmethod
    def encode_categorical(df: pd.DataFrame,
                         columns: Optional[List[str]] = None,
                         method: str = 'onehot',
                         target_column: Optional[str] = None) -> pd.DataFrame:
        """
        NUEVA FUNCIÓN: Codifica variables categóricas usando diferentes métodos.
        
        Args:
            df: DataFrame a procesar
            columns: Lista de columnas a codificar (None para todas las categóricas)
            method: Método de codificación ('onehot', 'label', 'target', 'woe', 'binary')
            target_column: Columna objetivo para codificación supervisada
        """
        df = df.copy()
        
        if columns is None:
            columns = df.select_dtypes(include=['object', 'category']).columns
        
        if method == 'onehot':
            df = pd.get_dummies(df, columns=columns, prefix_sep='_')
        elif method == 'label':
            for col in columns:
                df[col] = df[col].astype('category').cat.codes
        elif method == 'target' and target_column:
            encoder = TargetEncoder()
            df[columns] = encoder.fit_transform(df[columns], df[target_column])
        elif method == 'woe' and target_column:
            encoder = WOEEncoder()
            df[columns] = encoder.fit_transform(df[columns], df[target_column])
        elif method == 'binary':
            for col in columns:
                if df[col].nunique() == 2:
                    df[col] = (df[col] == df[col].value_counts().index[0]).astype(int)
        
        return df

    @staticmethod
    def scale_features(df: pd.DataFrame,
                      columns: Optional[List[str]] = None,
                      method: str = 'standard') -> Tuple[pd.DataFrame, object]:
        """
        NUEVA FUNCIÓN: Escala características numéricas.
        
        Args:
            df: DataFrame a procesar
            columns: Lista de columnas a escalar (None para todas las numéricas)
            method: Método de escalado ('standard', 'minmax', 'robust')
            
        Returns:
            Tuple con DataFrame escalado y objeto scaler
        """
        df = df.copy()
        
        if columns is None:
            columns = df.select_dtypes(include=[np.number]).columns
        
        if method == 'standard':
            scaler = StandardScaler()
        elif method == 'minmax':
            scaler = MinMaxScaler()
        elif method == 'robust':
            scaler = RobustScaler()
        
        df[columns] = scaler.fit_transform(df[columns])
        
        return df, scaler
