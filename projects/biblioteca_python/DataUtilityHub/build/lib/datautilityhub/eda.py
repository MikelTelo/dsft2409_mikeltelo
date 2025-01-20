"""
Módulo de Análisis Exploratorio de Datos (EDA)
"""

import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
from typing import Union, List, Dict, Optional, Tuple
from IPython.display import display

class DataLoader:
    """Clase para cargar y analizar datos"""
    
    @staticmethod
    def cargar_csv_de_directorio(directorio: str) -> pd.DataFrame:
        """
        Carga automáticamente el primer archivo CSV encontrado en el directorio dado
        y genera un análisis básico del mismo.
        """
        if not os.path.isdir(directorio):
            raise ValueError(f"La ruta proporcionada no es un directorio válido: {directorio}")
        
        csv_archivos = [archivo for archivo in os.listdir(directorio) if archivo.endswith('.csv')]
        
        if not csv_archivos:
            raise FileNotFoundError("No se encontraron archivos CSV en el directorio especificado.")
        
        archivo_csv = csv_archivos[0]
        ruta_csv = os.path.join(directorio, archivo_csv)
        
        try:
            df = pd.read_csv(ruta_csv)
            print(f"\n{'#' * 50}")
            print(f"# {'Archivo CSV cargado: ' + ruta_csv.center(40)} #")
            print(f"{'#' * 50}")
            
            DataLoader._mostrar_analisis_basico(df)
            return df
            
        except Exception as e:
            raise Exception(f"Error al cargar el archivo CSV: {str(e)}")

    @staticmethod
    def _mostrar_analisis_basico(df: pd.DataFrame) -> None:
        """Muestra análisis básico del DataFrame"""
        print("\n" + "="*50)
        print("DataFrame completo".center(50))
        print("="*50)
        display(df)
        
        print("\n" + "="*50)
        print("Primeras filas".center(50))
        print("="*50)
        display(df.head())
        
        print("\n" + "="*50)
        print("Información del DataFrame".center(50))
        print("="*50)
        df.info()
        
        print("\n" + "="*50)
        print("Estadísticas descriptivas".center(50))
        print("="*50)
        display(df.describe())
        
        print("\n" + "="*50)
        print("Valores únicos por columna".center(50))
        print("="*50)
        for columna in df.columns:
            print(f"\n{columna} - VALORES ÚNICOS:")
            print(df[columna].value_counts())

    @staticmethod
    def cargar_multiple_csv(directorio: str, pattern: str = "*.csv") -> Dict[str, pd.DataFrame]:
        """
        NUEVA FUNCIÓN: Carga múltiples archivos CSV que coincidan con un patrón.
        
        Args:
            directorio: Directorio donde buscar los archivos
            pattern: Patrón para filtrar archivos (ejemplo: "datos_*.csv")
            
        Returns:
            Dict con nombres de archivo como claves y DataFrames como valores
        """
        import glob
        
        archivos = glob.glob(os.path.join(directorio, pattern))
        dataframes = {}
        
        for archivo in archivos:
            nombre = os.path.basename(archivo)
            try:
                dataframes[nombre] = pd.read_csv(archivo)
                print(f"✅ Cargado: {nombre}")
            except Exception as e:
                print(f"❌ Error al cargar {nombre}: {str(e)}")
        
        return dataframes

class NullAnalyzer:
    """Clase para análisis de valores nulos"""
    
    @staticmethod
    def null_analysis(df: pd.DataFrame, show_plot: bool = True) -> Tuple[pd.DataFrame, Dict]:
        """
        Analiza valores nulos en un DataFrame.
        
        Returns:
            Tuple con DataFrame de análisis y diccionario de recomendaciones
        """
        # Análisis básico de nulos
        null_info = pd.DataFrame({
            'Columna': df.columns,
            'Nulos': df.isnull().sum(),
            'Porcentaje': (df.isnull().sum() / len(df)) * 100
        }).set_index('Columna').sort_values(by='Nulos', ascending=False)

        # Generar recomendaciones
        recomendaciones = {}
        for col in df.columns:
            pct_nulos = (df[col].isnull().sum() / len(df)) * 100
            if pct_nulos == 0:
                continue
            elif pct_nulos < 5:
                recomendaciones[col] = "Considerar imputación por media/mediana"
            elif pct_nulos < 30:
                recomendaciones[col] = "Evaluar importancia de la variable y considerar técnicas avanzadas de imputación"
            else:
                recomendaciones[col] = "Considerar eliminar la columna"

        # Visualización
        if show_plot:
            plt.figure(figsize=(12, 6))
            plt.bar(null_info.index, null_info['Nulos'], color='skyblue')
            plt.title('Valores Nulos por Columna')
            plt.xlabel('Columnas')
            plt.ylabel('Cantidad de Nulos')
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            plt.show()

        return null_info, recomendaciones

    @staticmethod
    def analizar_patrones_nulos(df: pd.DataFrame) -> pd.DataFrame:
        """
        NUEVA FUNCIÓN: Analiza patrones de valores nulos entre columnas.
        
        Returns:
            DataFrame con matriz de correlación de valores nulos
        """
        # Crear matriz de nulos (1 si es nulo, 0 si no)
        null_matrix = df.isnull().astype(int)
        
        # Calcular correlación entre patrones de nulos
        null_corr = null_matrix.corr()
        
        # Visualizar correlaciones significativas
        significant_corr = null_corr[abs(null_corr) > 0.5]
        
        print("Patrones de valores nulos correlacionados:")
        for col1 in significant_corr.columns:
            for col2 in significant_corr.index:
                if col1 < col2 and abs(significant_corr.loc[col2, col1]) > 0.5:
                    print(f"{col1} - {col2}: {significant_corr.loc[col2, col1]:.2f}")
        
        return null_corr

class DuplicateHandler:
    """Clase para manejar duplicados en DataFrames"""
    
    @staticmethod
    def find_duplicates(df: pd.DataFrame, subset: Optional[List[str]] = None) -> pd.DataFrame:
        """
        Encuentra filas duplicadas en un DataFrame.
        
        Args:
            df: DataFrame a analizar
            subset: Lista de columnas para considerar en la búsqueda de duplicados
        """
        duplicados = df[df.duplicated(subset=subset, keep='first')]
        print(f"Se encontraron {len(duplicados)} filas duplicadas")
        return duplicados

    @staticmethod
    def remove_duplicates(df: pd.DataFrame, subset: Optional[List[str]] = None, 
                         keep: str = 'first') -> pd.DataFrame:
        """
        Elimina filas duplicadas de un DataFrame.
        
        Args:
            df: DataFrame a limpiar
            subset: Lista de columnas para considerar
            keep: 'first', 'last' o False
        """
        len_original = len(df)
        df_limpio = df.drop_duplicates(subset=subset, keep=keep)
        eliminados = len_original - len(df_limpio)
        print(f"Se eliminaron {eliminados} filas duplicadas")
        return df_limpio

    @staticmethod
    def get_duplicate_stats(df: pd.DataFrame, subset: Optional[List[str]] = None) -> Dict:
        """
        NUEVA FUNCIÓN: Obtiene estadísticas detalladas sobre duplicados.
        
        Returns:
            Diccionario con estadísticas de duplicados
        """
        stats = {
            'total_rows': len(df),
            'duplicate_rows': len(df[df.duplicated(subset=subset, keep=False)]),
            'unique_rows': len(df.drop_duplicates(subset=subset)),
            'duplicate_groups': len(df[df.duplicated(subset=subset, keep=False)].groupby(subset if subset else df.columns).size()),
            'max_duplicates': df[df.duplicated(subset=subset, keep=False)].groupby(subset if subset else df.columns).size().max()
        }
        
        stats['duplicate_percentage'] = (stats['duplicate_rows'] / stats['total_rows']) * 100
        
        return stats
