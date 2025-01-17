import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from typing import Union, List, Dict, Optional

def plot_numeric_distributions(df: pd.DataFrame, 
                             columns: Optional[List[str]] = None) -> List[go.Figure]:
    """Visualize numeric distributions using histograms."""
    if columns is None:
        columns = df.select_dtypes(include=np.number).columns
    
    figures = []
    for col in columns:
        fig = px.histogram(df, x=col, title=f'Distribution of {col}')
        figures.append(fig)
    return figures

def plot_pie_charts(df: pd.DataFrame, 
                   columns: List[str]) -> List[go.Figure]:
    """Create pie charts for categorical columns."""
    figures = []
    for col in columns:
        value_counts = df[col].value_counts()
        fig = px.pie(values=value_counts.values, 
                    names=value_counts.index, 
                    title=f'Distribution of {col}')
        figures.append(fig)
    return figures

def plot_interactive_line_chart(df: pd.DataFrame,
                              x: str,
                              y: Union[str, List[str]],
                              title: Optional[str] = None) -> go.Figure:
    """Generate interactive line charts."""
    fig = px.line(df, x=x, y=y, title=title)
    return fig

def plot_interactive_pie_chart(df: pd.DataFrame,
                             column: str,
                             title: Optional[str] = None) -> go.Figure:
    """Create interactive pie charts."""
    value_counts = df[column].value_counts()
    fig = px.pie(values=value_counts.values,
                names=value_counts.index,
                title=title or f'Distribution of {column}')
    return fig 