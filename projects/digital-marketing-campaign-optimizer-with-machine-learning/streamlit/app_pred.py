#!pip install imbalanced-learn
#!pip install shap

# === Librerías estándar ===
import re  # Trabajo con expresiones regulares
import math  # Funciones matemáticas
import warnings  # Manejo de advertencias

# === Manipulación y análisis de datos ===
import pandas as pd  # Manejo y análisis de datos estructurados
import numpy as np  # Operaciones numéricas y manejo de arrays

# === Visualización ===
import matplotlib.pyplot as plt  # Creación de gráficos básicos
from mpl_toolkits.mplot3d import Axes3D  # Gráficos 3D
import seaborn as sns  # Gráficos estadísticos y estilos
sns.set_style('whitegrid')  # Estilo de gráficos para seaborn

# === Selección de modelos y preprocesamiento ===
from sklearn.model_selection import (
    train_test_split,  # División de datos en conjuntos de entrenamiento y prueba
    GridSearchCV,  # Búsqueda de hiperparámetros con validación cruzada
    StratifiedKFold,  # Validación cruzada estratificada
    RandomizedSearchCV  # Búsqueda de hiperparámetros aleatoria
)
from sklearn.preprocessing import StandardScaler, LabelEncoder  # Preprocesamiento
from sklearn.pipeline import Pipeline  # Construcción de pipelines para preprocesamiento y modelado

# === Manejo de desbalanceo de clases ===
from imblearn.combine import SMOTETomek  # SMOTE + Tomek Links para balanceo de datos
from imblearn.over_sampling import SMOTE  # SMOTE para sobremuestreo

# === Modelos de Machine Learning ===
from sklearn.ensemble import (
    RandomForestClassifier,  # Clasificador Random Forest
    GradientBoostingClassifier,  # Clasificador Gradient Boosting
    StackingClassifier,  # Clasificador basado en apilamiento
    RandomForestRegressor,  # Regresor Random Forest
    GradientBoostingRegressor  # Regresor Gradient Boosting
)
from xgboost import XGBClassifier, XGBRegressor  # Clasificador y regresor XGBoost

# === Métricas y evaluación ===
from sklearn.metrics import (
    classification_report,  # Reporte de métricas para clasificación
    confusion_matrix,  # Matriz de confusión
    ConfusionMatrixDisplay,  # Visualización de matriz de confusión
    roc_auc_score,  # Métrica AUC-ROC
    roc_curve,  # Curva ROC
    f1_score,  # F1-Score
    recall_score,  # Recall (Sensibilidad)
    precision_score,  # Precisión
    mean_absolute_error,  # MAE (Error absoluto medio) para regresión
    mean_squared_error  # MSE (Error cuadrático medio) para regresión
)

# === Clustering ===
from sklearn.cluster import KMeans  # Algoritmo de clustering K-Means
from sklearn.metrics import (
    silhouette_samples,  # Evaluación de silueta para cada punto
    silhouette_score  # Puntuación general de silueta para el modelo
)

# === Reducción de dimensionalidad ===
from sklearn.decomposition import PCA  # Análisis de componentes principales (PCA)

# === Utilidades ===
from sklearn.utils.class_weight import compute_class_weight  # Cálculo de pesos para clases desbalanceadas
import joblib  # Guardar y cargar modelos entrenados

# Cargar los datos
df = pd.read_csv('data/digital_marketing_campaign_dataset.csv')

# Eliminar columnas irrelevantes
df = df.drop(columns=['AdvertisingPlatform', 'AdvertisingTool'])

# Columnas categóricas a codificar
categorical_columns = ['Gender', 'CampaignChannel', 'CampaignType']

# Aplicar One-Hot Encoding
df_encoded = pd.get_dummies(df, columns=categorical_columns, drop_first=False)

# Convertir todos los valores True/False a 1/0 en el DataFrame
df_encoded = df_encoded.applymap(lambda x: 1 if x is True else 0 if x is False else x)

# Determinar el número óptimo de clusters con el método del codo y silhouette score
inertia = []
silhouette_scores = []
max_clusters = 60

for k in range(2, max_clusters + 1):
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(data_scaled)
    inertia.append(kmeans.inertia_)
    silhouette_scores.append(silhouette_score(data_scaled, kmeans.labels_))

# Gráfico combinado: Método del Codo y Silhouette Score
fig, ax1 = plt.subplots(figsize=(10, 6))
ax2 = ax1.twinx()

ax1.plot(range(2, max_clusters + 1), inertia, 'o-b', label='Inercia (Codo)')
ax2.plot(range(2, max_clusters + 1), silhouette_scores, 'o-g', label='Silhouette Score')

ax1.set_xlabel("Número de Clusters")
ax1.set_ylabel("Inercia", color="blue")
ax2.set_ylabel("Silhouette Score", color="green")
plt.title("Método del Codo y Silhouette Score (2-60 Clusters)")
ax1.legend(loc="center left")
ax2.legend(loc="center right")
plt.grid()
plt.show()

# Elegir el número óptimo de clusters
optimal_k = 31
kmeans = KMeans(n_clusters=optimal_k, random_state=42)
data_cluster["Cluster"] = kmeans.fit_predict(data_scaled)

# Crear promedios por cluster
cluster_means_scaled = data_cluster.groupby("Cluster").mean()

# Excluir la columna de 'Cluster' antes de desescalar
cluster_means_scaled = cluster_means_scaled[variables_cluster]

# Desescalar los promedios
cluster_means = pd.DataFrame(
    scaler.inverse_transform(cluster_means_scaled),
    columns=variables_cluster,
    index=cluster_means_scaled.index
)

# Normalizar los valores promedio desescalados
cluster_means_normalized = cluster_means / cluster_means.max()

# Configuración para Spider Plot en filas de 3
categories = cluster_means.columns
num_vars = len(categories)
angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
angles += angles[:1]  # Cerrar el círculo

# Configuración del número de filas y columnas
cols = 3  # Máximo de gráficos por fila
rows = (optimal_k + cols - 1) // cols  # Calcular filas necesarias
fig, axes = plt.subplots(rows, cols, figsize=(20, rows * 6), subplot_kw=dict(polar=True))

# Asegurarse de que los ejes sean unidimensionales para iterar
axes = axes.flatten()

for cluster in range(optimal_k):
    # Seleccionar el eje correspondiente
    ax = axes[cluster]

    # Valores del cluster actual
    values = cluster_means_normalized.iloc[cluster].values.flatten().tolist()
    values += values[:1]  # Cerrar el círculo

    # Añadir datos del cluster
    ax.plot(angles, values, label=f"Cluster {cluster}", linewidth=2, color=f"C{cluster}")
    ax.fill(angles, values, alpha=0.25)

    # Configuración del gráfico
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, fontsize=10)
    ax.set_yticks([])
    ax.set_title(f"Perfil del Cluster {cluster}", size=16, fontweight="bold", y=1.1)

    # Leyenda
    ax.legend(loc="upper right", fontsize=10)

# Eliminar ejes vacíos si los clusters no llenan la última fila
for i in range(optimal_k, len(axes)):
    fig.delaxes(axes[i])

# Ajustar el espaciado para evitar solapamientos
plt.tight_layout()
plt.show()

# --- Asignación manual de CampaignType y CampaignChannel ---
# Diccionario para asignación de CampaignType por cluster
manual_campaign_types = {
    0: "Retention",
    1: "Conversion",
    2: "Retention",
    3: "Conversion",
    4: "Conversion",
    5: "Conversion",
    6: "Retention",
    7: "Retention",
    8: "Consideration",
    9: "Retention",
    10: "Retention",
    11: "Conversion",
    12: "Conversion",
    13: "Conversion",
    14: "Retention",
    15: "Retention",
    16: "Conversion",
    17: "Conversion",
    18: "Conversion",
    19: "Retention",
    20: "Conversion",
    21: "Conversion",
    22: "Conversion",
    23: "Consideration",
    24: "Conversion",
    25: "Retention",
    26: "Conversion",
    27: "Conversion",
    28: "Retention",
    29: "Retention",
    30: "Retention",
}

# Diccionario para asignación de CampaignChannel por cluster
manual_campaign_channels = {
    0: "Email",
    1: "Email",
    2: "Social Media",
    3: "PPC",
    4: "PPC",
    5: "PPC",
    6: "Social Media",
    7: "PPC",
    8: "Social Media",
    9: "PPC",
    10: "Email",
    11: "Email",
    12: "Email",
    13: "Social Media",
    14: "Email",
    15: "Social Media",
    16: "Social Media",
    17: "Email",
    18: "Social Media",
    19: "PPC",
    20: "Email",
    21: "Social Media",
    22: "Social Media",
    23: "Email",
    24: "Email",
    25: "Email",
    26: "Social Media",
    27: "Social Media",
    28: "Email",
    29: "Email",
    30: "Email",
}

# Copiar df_encoded a df_encoded_mod
df_encoded_mod = df_encoded.copy()

# Inicializar todas las columnas CampaignChannel_xxx y CampaignType_xxx en False en df_encoded_mod
campaign_channels = ["Email", "PPC", "Referral", "SEO", "Social Media"]
for channel in campaign_channels:
    df_encoded_mod[f"CampaignChannel_{channel}"] = False

campaign_types = ["Awareness", "Consideration", "Conversion", "Retention"]
for campaign in campaign_types:
    df_encoded_mod[f"CampaignType_{campaign}"] = False

# Iterar sobre cada cluster y asignar True a las columnas correspondientes en df_encoded_mod
for cluster, campaign_type in manual_campaign_types.items():
    # Obtener CustomerIDs del cluster actual
    cluster_customers = data_cluster[data_cluster["Cluster"] == cluster]["CustomerID"]

    # Asignar CampaignType
    df_encoded_mod.loc[
        df_encoded_mod["CustomerID"].isin(cluster_customers),
        f"CampaignType_{campaign_type}"
    ] = True

for cluster, campaign_channel in manual_campaign_channels.items():
    # Obtener CustomerIDs del cluster actual
    cluster_customers = data_cluster[data_cluster["Cluster"] == cluster]["CustomerID"]

    # Asignar CampaignChannel
    df_encoded_mod.loc[
        df_encoded_mod["CustomerID"].isin(cluster_customers),
        f"CampaignChannel_{campaign_channel}"
    ] = True

# --- Validación ---
print("Validación de asignaciones:")
print("Ejemplo de asignaciones en data_cluster:")
print(data_cluster[["CustomerID", "Cluster"]].head())

print("\nDistribución de CampaignType en df_encoded_mod:")
print(df_encoded_mod[[f"CampaignType_{campaign}" for campaign in campaign_types]].sum())

print("\nDistribución de CampaignChannel en df_encoded_mod:")
print(df_encoded_mod[[f"CampaignChannel_{channel}" for channel in campaign_channels]].sum())

# --- Número de clientes asignados a cada cluster ---
cluster_counts = data_cluster["Cluster"].value_counts().sort_index()

print("\nNúmero de clientes asignados a cada cluster:")
print(cluster_counts)

# Visualización de la distribución por cluster
import matplotlib.pyplot as plt

plt.figure(figsize=(12, 6))
cluster_counts.plot(kind="bar", color="skyblue", edgecolor="black")
plt.title("Número de Clientes por Cluster")
plt.xlabel("Cluster")
plt.ylabel("Número de Clientes")
plt.xticks(rotation=0)
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.show()

df_encoded_mod = df_encoded_mod.drop(columns=['Conversion'])

# --- Predicción de AdSpend con GridSearch ---

# Datos de entrenamiento: campaña anterior
X_adspend = df_encoded.drop(columns=["AdSpend", "CustomerID", "Conversion"], errors="ignore")
y_adspend = df_encoded["AdSpend"]

# División en entrenamiento y prueba
X_train_adspend, X_test_adspend, y_train_adspend, y_test_adspend = train_test_split(
    X_adspend, y_adspend, test_size=0.2, random_state=42
)

# Escalar los datos de entrenamiento
scaler_adspend = StandardScaler()
X_train_adspend_scaled = scaler_adspend.fit_transform(X_train_adspend)
X_test_adspend_scaled = scaler_adspend.transform(X_test_adspend)

# Modelos de regresión
regressors = {
    "RandomForest": RandomForestRegressor(random_state=42),
    "GradientBoosting": GradientBoostingRegressor(random_state=42),
    "XGBoost": XGBRegressor(random_state=42, objective='reg:squarederror')
}

param_grid = {
    "RandomForest": {
        "n_estimators": [50, 100, 150],
        "max_depth": [3, 4, 5],
        "min_samples_split": [3, 5, 10]
    },
    "GradientBoosting": {
        "n_estimators": [50, 100, 150],
        "learning_rate": [0.01, 0.1, 0.2],
        "max_depth": [3, 5, 7]
    },
    "XGBoost": {
        "n_estimators": [50, 100, 150],
        "learning_rate": [0.01, 0.1, 0.2],
        "max_depth": [3, 5, 7]
    }
}

best_regressor = None
best_score = float('inf')

for name, model in regressors.items():
    grid_search = GridSearchCV(
        model, param_grid[name], cv=3, scoring="neg_mean_squared_error", n_jobs=-1
    )
    grid_search.fit(X_train_adspend_scaled, y_train_adspend)
    
    if -grid_search.best_score_ < best_score:
        best_score = -grid_search.best_score_
        best_regressor = grid_search.best_estimator_
        best_model_name = name

print(f"Mejor modelo para AdSpend: {best_model_name}")
print(f"Mejor MSE: {best_score:.2f}")
print(f"Mejores hiperparámetros: {grid_search.best_params_}")

# Datos de predicción: nueva campaña
X_mod = df_encoded_mod.drop(columns=["AdSpend", "CustomerID", "Conversion"], errors="ignore")

# Escalar los datos de la nueva campaña con el mismo scaler
X_mod_scaled = scaler_adspend.transform(X_mod)

# Predicción de AdSpend para la nueva campaña
df_encoded_mod["AdSpend"] = best_regressor.predict(X_mod_scaled)

# Ajustar el gasto total para mantener proporciones similares
original_total = y_adspend.sum()  # Total original conocido
modified_total = df_encoded_mod["AdSpend"].sum()  # Total predicho
scaling_factor = original_total / modified_total
df_encoded_mod["AdSpend"] *= scaling_factor

# Evaluación del modelo en datos de entrenamiento y prueba
train_mse = mean_squared_error(y_train_adspend, best_regressor.predict(X_train_adspend_scaled))
test_mse = mean_squared_error(y_test_adspend, best_regressor.predict(X_test_adspend_scaled))
print(f"\nMSE en Train: {train_mse:.2f}")
print(f"MSE en Test: {test_mse:.2f}")

# --- Resumen de gasto de AdSpend ---
original_adspend = df_encoded["AdSpend"].sum()
modified_adspend = df_encoded_mod["AdSpend"].sum()

print("\nGasto total en campañas:")
print(f"Original: {original_adspend:.2f}")
print(f"Modificado: {modified_adspend:.2f}")

# Gasto desglosado por CampaignType
print("\nGasto por CampaignType:")
for campaign in ["Awareness", "Consideration", "Conversion", "Retention"]:
    original_spend = df_encoded.loc[df_encoded[f'CampaignType_{campaign}'] == 1, 'AdSpend'].sum()
    modified_spend = df_encoded_mod.loc[df_encoded_mod[f'CampaignType_{campaign}'] == 1, 'AdSpend'].sum()
    print(f"{campaign}:")
    print(f"  Original: {original_spend:.2f}")
    print(f"  Modificado: {modified_spend:.2f}")

# Gasto desglosado por CampaignChannel
print("\nGasto por CampaignChannel:")
for channel in ["Email", "PPC", "Referral", "SEO", "Social Media"]:
    original_spend = df_encoded.loc[df_encoded[f'CampaignChannel_{channel}'] == 1, 'AdSpend'].sum()
    modified_spend = df_encoded_mod.loc[df_encoded_mod[f'CampaignChannel_{channel}'] == 1, 'AdSpend'].sum()
    print(f"{channel}:")
    print(f"  Original: {original_spend:.2f}")
    print(f"  Modificado: {modified_spend:.2f}")

    # Inicializar listas para almacenar los datos de gasto
campaign_types = ["Awareness", "Consideration", "Conversion", "Retention"]
campaign_channels = ["Email", "PPC", "Referral", "SEO", "Social Media"]

original_campaign_spend = []
modified_campaign_spend = []

original_channel_spend = []
modified_channel_spend = []

# Gasto por CampaignType (en miles de dólares)
for campaign in campaign_types:
    original_spend = df_encoded.loc[df_encoded[f'CampaignType_{campaign}'] == 1, 'AdSpend'].sum() / 1000  # en miles de dólares
    modified_spend = df_encoded_mod.loc[df_encoded_mod[f'CampaignType_{campaign}'] == 1, 'AdSpend'].sum() / 1000  # en miles de dólares
    original_campaign_spend.append(original_spend)
    modified_campaign_spend.append(modified_spend)

# Gasto por CampaignChannel (en miles de dólares)
for channel in campaign_channels:
    original_spend = df_encoded.loc[df_encoded[f'CampaignChannel_{channel}'] == 1, 'AdSpend'].sum() / 1000  # en miles de dólares
    modified_spend = df_encoded_mod.loc[df_encoded_mod[f'CampaignChannel_{channel}'] == 1, 'AdSpend'].sum() / 1000  # en miles de dólares
    original_channel_spend.append(original_spend)
    modified_channel_spend.append(modified_spend)

# Configurar la posición de las barras
x_campaigns = np.arange(len(campaign_types))
x_channels = np.arange(len(campaign_channels))

# Crear el gráfico de barras
fig, ax = plt.subplots(figsize=(14, 8))

bar_width = 0.35  # Ancho de las barras

# Colores sobrios
color_original = '#6fa3f7'  # Azul suave
color_modified = '#f1a7a6'  # Rojo suave

# Barras para CampaignType
bar1 = ax.bar(x_campaigns - bar_width/2, original_campaign_spend, bar_width, label='Original', color=color_original)
bar2 = ax.bar(x_campaigns + bar_width/2, modified_campaign_spend, bar_width, label='Modificado', color=color_modified)

# Barras para CampaignChannel
bar3 = ax.bar(x_channels - bar_width/2 + len(campaign_types), original_channel_spend, bar_width, label='Original', color=color_original)
bar4 = ax.bar(x_channels + bar_width/2 + len(campaign_types), modified_channel_spend, bar_width, label='Modificado', color=color_modified)

# Etiquetas y título
ax.set_xlabel('Tipo de Campaña y Canal', fontsize=12)
ax.set_ylabel('Gasto en AdSpend (Miles de dólares)', fontsize=12)
ax.set_title('Desglose de Gasto en AdSpend por Tipo de Campaña y Canal', fontsize=14, fontweight='bold')

# Configuración de las leyendas
ax.legend()

# Ajuste de etiquetas y posiciones
ax.set_xticks(np.concatenate([x_campaigns, x_channels + len(campaign_types)]))
ax.set_xticklabels(campaign_types + campaign_channels, rotation=45, ha='right', fontsize=10)

# Mejoras visuales
plt.tight_layout()
plt.show()


# Cargar pipeline completo
best_pipeline = joblib.load("RandomForest_best_pipeline.pkl")
print("\nPipeline cargado: RandomForest_best_pipeline.pkl")

# Predicción en la nueva campaña
X_mod = df_encoded_mod.drop(columns=["CustomerID"], errors="ignore")
y_mod_proba = best_pipeline.predict_proba(X_mod)[:, 1]

# Ajuste de probabilidades según el umbral
optimal_threshold = 0.5  # Usar el umbral óptimo o manual
y_mod_pred = (y_mod_proba >= optimal_threshold).astype(int)

# Añadir predicciones al dataset
df_encoded_mod["Conversion"] = y_mod_pred

# --- Visualizaciones ---
def create_visualizations(df, title_prefix):
    sns.set(style="whitegrid")
    fig, axes = plt.subplots(1, 4, figsize=(24, 6))  # Una fila con 4 gráficos

    # Gráfico 1: Relación entre CampaignChannel y Conversion
    sns.countplot(data=df, x=df[["CampaignChannel_Email", "CampaignChannel_PPC",
                                 "CampaignChannel_Referral", "CampaignChannel_SEO",
                                 "CampaignChannel_Social Media"]].idxmax(axis=1),
                  hue="Conversion", ax=axes[0])
    axes[0].set_title(f"{title_prefix}: Relación CampaignChannel y Conversion")
    axes[0].set_xlabel("CampaignChannel")
    axes[0].set_ylabel("Frecuencia")
    axes[0].tick_params(axis="x", rotation=30)

    # Gráfico 2: Relación entre CampaignType y Conversion
    sns.countplot(data=df, x=df[["CampaignType_Awareness", "CampaignType_Consideration",
                                 "CampaignType_Conversion", "CampaignType_Retention"]].idxmax(axis=1),
                  hue="Conversion", ax=axes[1])
    axes[1].set_title(f"{title_prefix}: Relación CampaignType y Conversion")
    axes[1].set_xlabel("CampaignType")
    axes[1].set_ylabel("Frecuencia")
    axes[1].tick_params(axis="x", rotation=30)

    # Gráfico 3: Relación entre CampaignChannel y AdSpend
    sns.boxplot(data=df, x=df[["CampaignChannel_Email", "CampaignChannel_PPC",
                               "CampaignChannel_Referral", "CampaignChannel_SEO",
                               "CampaignChannel_Social Media"]].idxmax(axis=1),
                y="AdSpend", ax=axes[2])
    axes[2].set_title(f"{title_prefix}: Relación CampaignChannel y AdSpend")
    axes[2].set_xlabel("CampaignChannel")
    axes[2].set_ylabel("AdSpend")
    axes[2].tick_params(axis="x", rotation=30)

    # Gráfico 4: Relación entre CampaignType y AdSpend
    sns.boxplot(data=df, x=df[["CampaignType_Awareness", "CampaignType_Consideration",
                               "CampaignType_Conversion", "CampaignType_Retention"]].idxmax(axis=1),
                y="AdSpend", ax=axes[3])
    axes[3].set_title(f"{title_prefix}: Relación CampaignType y AdSpend")
    axes[3].set_xlabel("CampaignType")
    axes[3].set_ylabel("AdSpend")
    axes[3].tick_params(axis="x", rotation=30)

    plt.tight_layout()
    plt.show()

# Visualizaciones para datos originales y modificados
create_visualizations(df_encoded, "Original")
create_visualizations(df_encoded_mod, "Modificado")

# Crear un desglose de conversiones positivas por canal de campaña y tipo de campaña
def conversion_desglose(df):
    # Identificar el canal de campaña predominante
    df['CampaignChannel'] = df[[
        "CampaignChannel_Email", "CampaignChannel_PPC",
        "CampaignChannel_Referral", "CampaignChannel_SEO",
        "CampaignChannel_Social Media"
    ]].idxmax(axis=1)

    # Identificar el tipo de campaña predominante
    df['CampaignType'] = df[[
        "CampaignType_Awareness", "CampaignType_Consideration",
        "CampaignType_Conversion", "CampaignType_Retention"
    ]].idxmax(axis=1)

    # Filtrar las conversiones positivas
    conversions_positive = df[df['Conversion'] == 1]

    # Calcular la cantidad de conversiones por canal
    channel_conversion = conversions_positive.groupby('CampaignChannel').size().reset_index(name='PositiveConversionsByChannel')

    # Calcular la cantidad de conversiones por tipo de campaña
    type_conversion = conversions_positive.groupby('CampaignType').size().reset_index(name='PositiveConversionsByType')

    # Calcular los totales generales
    total_channel_conversions = channel_conversion['PositiveConversionsByChannel'].sum()
    total_type_conversions = type_conversion['PositiveConversionsByType'].sum()

    return channel_conversion, type_conversion, total_channel_conversions, total_type_conversions

# Aplicar la función a los datos
channel_conversion_encoded, type_conversion_encoded, total_channel_conversions_encoded, total_type_conversions_encoded = conversion_desglose(df_encoded)
channel_conversion_encoded_mod, type_conversion_encoded_mod, total_channel_conversions_encoded_mod, total_type_conversions_encoded_mod = conversion_desglose(df_encoded_mod)

# Mostrar los resultados para df_encoded
print("Desglose de Conversiones Positivas por Canal de Campaña (df_encoded):")
print(channel_conversion_encoded)

print("\nDesglose de Conversiones Positivas por Tipo de Campaña (df_encoded):")
print(type_conversion_encoded)

print(f"\nTotal de Conversiones Positivas por Canal (df_encoded): {total_channel_conversions_encoded}")
print(f"Total de Conversiones Positivas por Tipo (df_encoded): {total_type_conversions_encoded}")

# Mostrar los resultados para df_encoded_mod
print("\nDesglose de Conversiones Positivas por Canal de Campaña (df_encoded_mod):")
print(channel_conversion_encoded_mod)

print("\nDesglose de Conversiones Positivas por Tipo de Campaña (df_encoded_mod):")
print(type_conversion_encoded_mod)

print(f"\nTotal de Conversiones Positivas por Canal (df_encoded_mod): {total_channel_conversions_encoded_mod}")
print(f"Total de Conversiones Positivas por Tipo (df_encoded_mod): {total_type_conversions_encoded_mod}")

# Gráfica comparativa de tipos de campaña (incluyendo todas las campañas)
def plot_campaign_type_comparison(type_conversion_encoded, type_conversion_encoded_mod):
    sns.set(style="whitegrid")

    # Fusionar los DataFrames para comparación, asegurando que se incluyan todas las campañas
    comparison_df = pd.merge(
        type_conversion_encoded.rename(columns={'PositiveConversionsByType': 'Encoded'}),
        type_conversion_encoded_mod.rename(columns={'PositiveConversionsByType': 'Encoded_Mod'}),
        on='CampaignType', how='outer'
    ).fillna(0)

    # Calcular totales y agregar una fila para "Total"
    total_encoded = comparison_df['Encoded'].sum()
    total_encoded_mod = comparison_df['Encoded_Mod'].sum()
    comparison_df = pd.concat([
        comparison_df,
        pd.DataFrame({
            'CampaignType': ['Total'],
            'Encoded': [total_encoded],
            'Encoded_Mod': [total_encoded_mod]
        })
    ])

    # Configuración de la gráfica
    comparison_df.set_index('CampaignType').plot(kind='bar', figsize=(12, 7))
    plt.title("Comparativa de Conversiones Positivas por Tipo de Campaña (Todas las Campañas)")
    plt.ylabel("Cantidad de Conversiones Positivas")
    plt.xlabel("Tipo de Campaña")
    plt.xticks(rotation=45)
    plt.legend(title="Dataset", labels=["Encoded", "Encoded Mod"])
    plt.tight_layout()
    plt.show()

# Gráfica comparativa de canales de campaña (incluyendo todos los canales)
def plot_campaign_channel_comparison(channel_conversion_encoded, channel_conversion_encoded_mod):
    sns.set(style="whitegrid")

    # Fusionar los DataFrames para comparación, asegurando que se incluyan todos los canales
    comparison_df = pd.merge(
        channel_conversion_encoded.rename(columns={'PositiveConversionsByChannel': 'Encoded'}),
        channel_conversion_encoded_mod.rename(columns={'PositiveConversionsByChannel': 'Encoded_Mod'}),
        on='CampaignChannel', how='outer'
    ).fillna(0)

    # Calcular totales y agregar una fila para "Total"
    total_encoded = comparison_df['Encoded'].sum()
    total_encoded_mod = comparison_df['Encoded_Mod'].sum()
    comparison_df = pd.concat([
        comparison_df,
        pd.DataFrame({
            'CampaignChannel': ['Total'],
            'Encoded': [total_encoded],
            'Encoded_Mod': [total_encoded_mod]
        })
    ])

    # Configuración de la gráfica
    comparison_df.set_index('CampaignChannel').plot(kind='bar', figsize=(12, 7))
    plt.title("Comparativa de Conversiones Positivas por Canal de Campaña (Todos los Canales)")
    plt.ylabel("Cantidad de Conversiones Positivas")
    plt.xlabel("Canal de Campaña")
    plt.xticks(rotation=45)
    plt.legend(title="Dataset", labels=["Encoded", "Encoded Mod"])
    plt.tight_layout()
    plt.show()

# Generar gráficas comparativas
plot_campaign_type_comparison(type_conversion_encoded, type_conversion_encoded_mod)
plot_campaign_channel_comparison(channel_conversion_encoded, channel_conversion_encoded_mod)

