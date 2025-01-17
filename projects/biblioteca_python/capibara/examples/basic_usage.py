import pandas as pd
import numpy as np
import capibara as cp

# Create sample data
df = pd.DataFrame({
    'age': [25, 30, 35, 40, 45, 50, 55, 60],
    'income': [30000, 45000, 50000, 60000, 70000, 80000, 85000, 90000],
    'education': ['High School', 'Bachelor', 'Master', 'PhD', 'Bachelor', 'Master', 'PhD', 'Master'],
    'satisfaction': [7, 8, 8.5, 9, 7.5, 8, 8.5, 9]
})

# Data Analysis
print("\n=== Basic Data Analysis ===")
analysis = cp.data_analysis.basic_data_analysis(df)
print("Data Shape:", analysis['shape'])
print("Missing Values:", analysis['missing_values'])

# Data Processing
print("\n=== Data Processing ===")
# Create dummy variables for education
df_processed = cp.data_processing.create_dummies(df, ['education'])
print("Columns after dummy creation:", df_processed.columns.tolist())

# Data Visualization
print("\n=== Data Visualization ===")
# Create numeric distributions
figures = cp.data_visualization.plot_numeric_distributions(df, ['age', 'income', 'satisfaction'])
for fig in figures:
    fig.show()

# Machine Learning
print("\n=== Machine Learning ===")
# Prepare data for prediction
X = df_processed.drop(['satisfaction'], axis=1)
y = df_processed['satisfaction']

# Train models
linear_model, linear_metrics = cp.machine_learning.linear_regression(X, y)
print("\nLinear Regression Metrics:")
print(f"R2 Score: {linear_metrics['r2']:.3f}")
print(f"RMSE: {linear_metrics['rmse']:.3f}")

# Text Analysis
texts = [
    "Data science is amazing and powerful",
    "Machine learning helps solve complex problems",
    "Python is great for data analysis",
    "Data visualization helps understand patterns"
]

print("\n=== Text Analysis ===")
common_words = cp.machine_learning.most_common_words(texts)
print("Most common words:", common_words) 