"""
Módulo de Visualización de Datos
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from typing import Optional, Union, List, Tuple, Dict
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

class DataVisualizer:
    """Clase para visualizaciones avanzadas de datos"""
    
    @staticmethod
    def plot_correlation_matrix(df: pd.DataFrame, 
                              figsize: tuple = (10, 8), 
                              method: str = 'pearson',
                              interactive: bool = False) -> None:
        """
        Genera una matriz de correlación con visualización mejorada.
        
        Args:
            df: DataFrame a analizar
            figsize: Tamaño de la figura
            method: Método de correlación ('pearson', 'spearman', 'kendall')
            interactive: Si True, usa plotly para generar un gráfico interactivo
        """
        corr = df.corr(method=method)
        
        if interactive:
            fig = go.Figure(data=go.Heatmap(
                z=corr,
                x=corr.columns,
                y=corr.columns,
                colorscale='RdBu',
                zmin=-1,
                zmax=1
            ))
            fig.update_layout(
                title=f'Matriz de Correlación ({method})',
                width=figsize[0]*100,
                height=figsize[1]*100
            )
            fig.show()
        else:
            plt.figure(figsize=figsize)
            mask = np.triu(np.ones_like(corr, dtype=bool))
            sns.heatmap(corr, mask=mask, annot=True, cmap='coolwarm', center=0)
            plt.title(f'Matriz de Correlación ({method})')
            plt.tight_layout()
            plt.show()

    @staticmethod
    def plot_distribution(df: pd.DataFrame, 
                         columns: Optional[List[str]] = None,
                         interactive: bool = False) -> None:
        """
        Genera gráficos de distribución para las columnas numéricas.
        
        Args:
            df: DataFrame a analizar
            columns: Lista de columnas a visualizar (None para todas numéricas)
            interactive: Si True, usa plotly para gráficos interactivos
        """
        if columns is None:
            columns = df.select_dtypes(include=[np.number]).columns
        
        n_cols = len(columns)
        
        if interactive:
            fig = make_subplots(rows=n_cols, cols=2,
                              subplot_titles=[f'Histograma de {col}' for col in columns] +
                                           [f'Box Plot de {col}' for col in columns])
            
            for i, col in enumerate(columns, 1):
                # Histograma
                fig.add_trace(
                    go.Histogram(x=df[col], name=col),
                    row=i, col=1
                )
                # Box plot
                fig.add_trace(
                    go.Box(y=df[col], name=col),
                    row=i, col=2
                )
            
            fig.update_layout(height=300*n_cols, showlegend=False)
            fig.show()
        else:
            fig, axes = plt.subplots(n_cols, 2, figsize=(12, 4*n_cols))
            
            for i, col in enumerate(columns):
                # Histograma
                sns.histplot(data=df, x=col, ax=axes[i,0])
                axes[i,0].set_title(f'Histograma de {col}')
                
                # Box plot
                sns.boxplot(data=df, y=col, ax=axes[i,1])
                axes[i,1].set_title(f'Box Plot de {col}')
            
            plt.tight_layout()
            plt.show()

    @staticmethod
    def plot_categorical_analysis(df: pd.DataFrame, 
                                cat_column: str,
                                value_column: Optional[str] = None,
                                top_n: int = 10,
                                interactive: bool = False) -> None:
        """
        NUEVA FUNCIÓN: Genera visualizaciones para variables categóricas.
        
        Args:
            df: DataFrame a analizar
            cat_column: Columna categórica a analizar
            value_column: Columna numérica opcional para análisis de valor
            top_n: Número de categorías principales a mostrar
            interactive: Si True, usa plotly para gráficos interactivos
        """
        # Preparar datos
        if value_column:
            data = df.groupby(cat_column)[value_column].agg(['count', 'mean', 'sum'])
            data = data.sort_values('sum', ascending=False).head(top_n)
        else:
            data = df[cat_column].value_counts().head(top_n)
        
        if interactive:
            if value_column:
                fig = make_subplots(rows=2, cols=1,
                                  subplot_titles=[f'Conteo por {cat_column}',
                                                f'Promedio de {value_column} por {cat_column}'])
                
                fig.add_trace(
                    go.Bar(x=data.index, y=data['count'], name='Conteo'),
                    row=1, col=1
                )
                fig.add_trace(
                    go.Bar(x=data.index, y=data['mean'], name='Promedio'),
                    row=2, col=1
                )
            else:
                fig = go.Figure(data=go.Bar(x=data.index, y=data.values))
                fig.update_layout(title=f'Distribución de {cat_column}')
            
            fig.show()
        else:
            if value_column:
                fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
                
                data['count'].plot(kind='bar', ax=ax1)
                ax1.set_title(f'Conteo por {cat_column}')
                ax1.tick_params(axis='x', rotation=45)
                
                data['mean'].plot(kind='bar', ax=ax2)
                ax2.set_title(f'Promedio de {value_column} por {cat_column}')
                ax2.tick_params(axis='x', rotation=45)
            else:
                plt.figure(figsize=(12, 6))
                data.plot(kind='bar')
                plt.title(f'Distribución de {cat_column}')
                plt.xticks(rotation=45)
            
            plt.tight_layout()
            plt.show()

    @staticmethod
    def plot_time_series(df: pd.DataFrame,
                        date_column: str,
                        value_columns: Union[str, List[str]],
                        freq: str = 'D',
                        interactive: bool = False) -> None:
        """
        NUEVA FUNCIÓN: Visualiza series temporales con diferentes agregaciones.
        
        Args:
            df: DataFrame con los datos
            date_column: Nombre de la columna de fecha
            value_columns: Columna(s) de valores a visualizar
            freq: Frecuencia de agregación ('D', 'W', 'M', 'Q', 'Y')
            interactive: Si True, usa plotly para visualización interactiva
        """
        # Asegurar que la columna de fecha es datetime
        df = df.copy()
        df[date_column] = pd.to_datetime(df[date_column])
        
        # Convertir value_columns a lista si es string
        if isinstance(value_columns, str):
            value_columns = [value_columns]
        
        # Agrupar por fecha
        df_grouped = df.groupby(pd.Grouper(key=date_column, freq=freq))[value_columns].mean()
        
        if interactive:
            fig = go.Figure()
            
            for col in value_columns:
                fig.add_trace(
                    go.Scatter(x=df_grouped.index, y=df_grouped[col], name=col)
                )
            
            fig.update_layout(
                title='Análisis de Series Temporales',
                xaxis_title='Fecha',
                yaxis_title='Valor'
            )
            fig.show()
        else:
            plt.figure(figsize=(12, 6))
            for col in value_columns:
                plt.plot(df_grouped.index, df_grouped[col], label=col)
            
            plt.title('Análisis de Series Temporales')
            plt.xlabel('Fecha')
            plt.ylabel('Valor')
            plt.legend()
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.show()
