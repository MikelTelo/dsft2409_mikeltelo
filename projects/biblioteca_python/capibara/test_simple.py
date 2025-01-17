import pandas as pd
import capibara as cp

# Crear datos de prueba
df = pd.DataFrame({
    'A': [1, 2, 3, 4, 5],
    'B': ['x', 'y', 'x', 'y', 'x'],
    'C': [10, 20, 30, 40, 50]
})

# Probar análisis básico
print("\nProbando análisis básico:")
analysis = cp.data_analysis.basic_data_analysis(df)
print("Shape:", analysis['shape'])
print("Tipos de datos:", analysis['dtypes'])

# Probar procesamiento
print("\nProbando procesamiento:")
df_dummies = cp.data_processing.create_dummies(df, ['B'])
print("Columnas después de dummies:", df_dummies.columns.tolist())

# Probar visualización
print("\nProbando visualización:")
figures = cp.data_visualization.plot_numeric_distributions(df, ['A', 'C'])
print("Gráficos creados:", len(figures))

print("\nTodas las pruebas completadas con éxito!") 