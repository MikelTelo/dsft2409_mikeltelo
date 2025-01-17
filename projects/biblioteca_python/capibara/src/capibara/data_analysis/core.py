import pandas as pd
import numpy as np
from typing import Union, List, Dict, Optional

def filter_rows(df: pd.DataFrame, conditions: Dict) -> pd.DataFrame:
    """Filter DataFrame rows based on conditions."""
    for column, condition in conditions.items():
        if isinstance(condition, (list, tuple)):
            df = df[df[column].isin(condition)]
        else:
            df = df[df[column] == condition]
    return df

def remove_outliers(df: pd.DataFrame, columns: List[str], n_std: float = 3) -> pd.DataFrame:
    """Remove outliers from specified columns using standard deviation method."""
    for column in columns:
        if pd.api.types.is_numeric_dtype(df[column]):
            mean = df[column].mean()
            std = df[column].std()
            df = df[abs(df[column] - mean) <= (n_std * std)]
    return df

def basic_data_analysis(df: pd.DataFrame) -> Dict:
    """Perform comprehensive data analysis."""
    analysis = {
        'shape': df.shape,
        'dtypes': df.dtypes.to_dict(),
        'missing_values': df.isnull().sum().to_dict(),
        'numeric_summary': df.describe().to_dict(),
        'categorical_summary': {col: df[col].value_counts().to_dict() 
                              for col in df.select_dtypes(include=['object']).columns}
    }
    return analysis

def outlier_meanSd(df: pd.DataFrame, column: str, n_std: float = 3) -> pd.Series:
    """Detect outliers using mean and standard deviation."""
    mean = df[column].mean()
    std = df[column].std()
    is_outlier = abs(df[column] - mean) > (n_std * std)
    return is_outlier

def data_report(df: pd.DataFrame) -> Dict:
    """Generate detailed data report."""
    report = {
        'basic_info': {
            'rows': len(df),
            'columns': len(df.columns),
            'duplicates': df.duplicated().sum(),
            'memory_usage': df.memory_usage(deep=True).sum()
        },
        'column_info': {
            col: {
                'dtype': str(df[col].dtype),
                'missing': df[col].isnull().sum(),
                'unique_values': df[col].nunique()
            } for col in df.columns
        }
    }
    return report

def missing_values_summary(df: pd.DataFrame) -> Dict:
    """Analyze missing values."""
    total = df.isnull().sum().sort_values(ascending=False)
    percent = (df.isnull().sum() / len(df) * 100).sort_values(ascending=False)
    
    summary = pd.concat([total, percent], axis=1, 
                       keys=['Total', 'Percent']).reset_index()
    return summary.to_dict('records') 