import pandas as pd
import numpy as np
from typing import Union, List, Dict, Optional, Tuple
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
import xgboost as xgb
from sklearn.cluster import KMeans
from collections import Counter
from sklearn.feature_extraction.text import CountVectorizer

def linear_regression(X: pd.DataFrame, 
                     y: pd.Series) -> Tuple[LinearRegression, Dict]:
    """Perform linear regression and return model and metrics."""
    model = LinearRegression()
    model.fit(X, y)
    
    predictions = model.predict(X)
    metrics = calculate_metrics(y, predictions)
    
    return model, metrics

def calculate_metrics(y_true: np.ndarray, 
                     y_pred: np.ndarray) -> Dict:
    """Calculate model performance metrics."""
    metrics = {
        'mse': mean_squared_error(y_true, y_pred),
        'rmse': np.sqrt(mean_squared_error(y_true, y_pred)),
        'mae': mean_absolute_error(y_true, y_pred),
        'r2': r2_score(y_true, y_pred)
    }
    return metrics

def unSupervisedCluster(data: pd.DataFrame, 
                       n_clusters: int = 3) -> Tuple[KMeans, np.ndarray]:
    """Perform clustering analysis using KMeans."""
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    clusters = kmeans.fit_predict(data)
    return kmeans, clusters

def gradient_boosting_regression(X: pd.DataFrame, 
                               y: pd.Series,
                               params: Optional[Dict] = None) -> Tuple[GradientBoostingRegressor, Dict]:
    """Apply gradient boosting regression."""
    if params is None:
        params = {
            'n_estimators': 100,
            'learning_rate': 0.1,
            'max_depth': 3
        }
    
    model = GradientBoostingRegressor(**params)
    model.fit(X, y)
    
    predictions = model.predict(X)
    metrics = calculate_metrics(y, predictions)
    
    return model, metrics

def xgboost_regression(X: pd.DataFrame, 
                      y: pd.Series,
                      params: Optional[Dict] = None) -> Tuple[xgb.XGBRegressor, Dict]:
    """Implement XGBoost regression."""
    if params is None:
        params = {
            'n_estimators': 100,
            'learning_rate': 0.1,
            'max_depth': 3
        }
    
    model = xgb.XGBRegressor(**params)
    model.fit(X, y)
    
    predictions = model.predict(X)
    metrics = calculate_metrics(y, predictions)
    
    return model, metrics

def random_forest_regression(X: pd.DataFrame, 
                           y: pd.Series,
                           params: Optional[Dict] = None) -> Tuple[RandomForestRegressor, Dict]:
    """Use random forest regression."""
    if params is None:
        params = {
            'n_estimators': 100,
            'max_depth': None,
            'min_samples_split': 2
        }
    
    model = RandomForestRegressor(**params)
    model.fit(X, y)
    
    predictions = model.predict(X)
    metrics = calculate_metrics(y, predictions)
    
    return model, metrics

def most_common_words(texts: List[str], 
                     n_words: int = 10) -> List[Tuple[str, int]]:
    """Analyze text data to find most common words."""
    vectorizer = CountVectorizer(stop_words='english')
    X = vectorizer.fit_transform(texts)
    
    word_freq = {}
    feature_names = vectorizer.get_feature_names_out()
    for i, freq in enumerate(X.sum(axis=0).A1):
        word_freq[feature_names[i]] = freq
    
    return Counter(word_freq).most_common(n_words)

def y_generator(df: pd.DataFrame, 
                target_column: str,
                operation: str = 'mean') -> pd.Series:
    """Generate target variables based on specified operation."""
    if operation == 'mean':
        return df[target_column].mean()
    elif operation == 'median':
        return df[target_column].median()
    elif operation == 'mode':
        return df[target_column].mode()[0]
    else:
        raise ValueError("Operation must be one of: 'mean', 'median', 'mode'") 