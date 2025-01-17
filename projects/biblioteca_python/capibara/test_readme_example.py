import pandas as pd
import capibara as cp

# Create or load your data
df = pd.DataFrame({
    'age': [25, 30, 35, 40],
    'salary': [30000, 45000, 50000, 60000],
    'category': ['A', 'B', 'A', 'B']
})

print("\nStep 1: Data Analysis")
analysis = cp.data_analysis.basic_data_analysis(df)
print("Basic Analysis:", analysis)

print("\nStep 2: Data Processing")
df_processed = cp.data_processing.create_dummies(df, ['category'])
print("Processed columns:", df_processed.columns.tolist())

print("\nStep 3: Data Visualization")
figures = cp.data_visualization.plot_numeric_distributions(df, ['age', 'salary'])
print("Number of figures created:", len(figures))

print("\nStep 4: Machine Learning")
X = df_processed.drop('salary', axis=1)
y = df_processed['salary']
model, metrics = cp.machine_learning.linear_regression(X, y)
print("Model Metrics:", metrics) 