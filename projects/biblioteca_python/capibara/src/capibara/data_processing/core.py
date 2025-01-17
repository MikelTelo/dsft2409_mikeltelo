import pandas as pd
import numpy as np
from typing import Union, List, Dict, Optional
from sklearn.preprocessing import LabelEncoder

def create_dummies(df: pd.DataFrame, 
                  columns: List[str], 
                  drop_first: bool = True) -> pd.DataFrame:
    """Create dummy variables for specified categorical columns."""
    return pd.get_dummies(df, columns=columns, drop_first=drop_first)

def fill_zeros_with_mean(df: pd.DataFrame, 
                        columns: Optional[List[str]] = None) -> pd.DataFrame:
    """Replace zeros with mean values in specified columns."""
    if columns is None:
        columns = df.select_dtypes(include=np.number).columns
    
    df = df.copy()
    for col in columns:
        if pd.api.types.is_numeric_dtype(df[col]):
            mean_value = df[df[col] != 0][col].mean()
            df[col] = df[col].replace(0, mean_value)
    return df

def fill_nans_with_mean(df: pd.DataFrame, 
                       columns: Optional[List[str]] = None) -> pd.DataFrame:
    """Handle missing values by replacing them with mean values."""
    if columns is None:
        columns = df.select_dtypes(include=np.number).columns
    
    df = df.copy()
    for col in columns:
        if pd.api.types.is_numeric_dtype(df[col]):
            df[col] = df[col].fillna(df[col].mean())
    return df

def convert_to_numeric(df: pd.DataFrame, 
                      columns: List[str], 
                      method: str = 'label') -> pd.DataFrame:
    """Convert categorical columns to numeric using specified method."""
    df = df.copy()
    
    if method == 'label':
        le = LabelEncoder()
        for col in columns:
            if df[col].dtype == 'object':
                df[col] = le.fit_transform(df[col].astype(str))
    elif method == 'ordinal':
        for col in columns:
            if df[col].dtype == 'object':
                categories = df[col].unique()
                mapping = {cat: i for i, cat in enumerate(categories)}
                df[col] = df[col].map(mapping)
    
    return df 