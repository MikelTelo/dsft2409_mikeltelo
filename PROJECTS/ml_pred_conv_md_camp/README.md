# **Predicción de Conversión en Campañas de Marketing Digital**

## **Descripción del Proyecto**

Este proyecto utiliza técnicas de Machine Learning para predecir conversiones en campañas de marketing digital. A través del análisis de datos, balanceo de clases y modelado, se optimizan estrategias de marketing dirigidas a maximizar el ROI (retorno de inversión). 

Se aplicaron modelos de clasificación binaria para predecir la probabilidad de conversión y, mediante técnicas de clusterización, se personalizaron estrategias de asignación de campañas y canales para diferentes segmentos de clientes.

---

## **Objetivos**

- Desarrollar un modelo de clasificación para predecir conversiones en campañas digitales.
- Optimizar la asignación de recursos publicitarios hacia los canales y campañas más efectivos.
- Proporcionar recomendaciones basadas en datos para mejorar la toma de decisiones comerciales.

---

## **Estructura del Proyecto**

El proyecto está organizado de la siguiente manera:

- **`main`**: Contiene 5 notebooks **pred_conv_md_camp_ml_General** el principal sobre el cual se basan el resto de los notebooks, al final del mismo hay links a los demas notebooks derivados de este (pred_conv_md_camp_ml_Awareness, pred_conv_md_camp_ml_Consideration, pred_conv_md_camp_ml_Conversion, pred_conv_md_camp_ml_Retention). **memoria** que contiene un resumen y explicación del proyecto. Este readme.
- **`utils/`**: Contiene otros documentos de utilidad
- **`data/`**: Contiene los datos utilizados en el análisis (descargables desde [Predict Conversion in Digital Marketing](https://www.kaggle.com/datasets/rabieelkharoua/predict-conversion-in-digital-marketing-dataset/data)).
- **`notebooks/`**: Jupyter Notebooks de prueba y desarrollo.
- **`model/`**: Archivos .pkl con modelos de machine learning entrenados.
- **`resources/`**: Contiene imágenes y gráficos relevantes para el análisis, como distribuciones, matrices de correlación y feature importance.

---

## **Datos Utilizados**

- **Registros:** 8000 observaciones.
- **Variables:** 20 (sin valores nulos).
- **Descripción:**
  - **Demográficas:** `Age`, `Gender`, `Income`.
  - **Interacciones digitales:** `ClickThroughRate`, `WebsiteVisits`, `PagesPerVisit`, `TimeOnSite`, `EmailOpens`, `EmailClicks`.
  - **Campañas publicitarias:** `CampaignChannel`, `CampaignType`, `AdSpend`.
  - **Variable objetivo:** `Conversion` (1 si el cliente realizó una conversión, 0 en caso contrario).

---

## **Metodología**

### **1. Exploración y Limpieza de Datos**
- **Eliminación de columnas irrelevantes:** Variables como `AdvertisingPlatform` y `AdvertisingTool` se descartaron por ser redundantes.
- **Análisis de correlación:** Se identificaron relaciones débiles entre variables predictoras y el objetivo.
- **Balanceo de clases:** Aplicación de **SMOTE + Tomek Links** para abordar el desbalance (90% conversiones positivas y 10% negativas).

### **2. Transformaciones**
- **Codificación de variables categóricas:** Uso de **One-Hot Encoding**.
- **Clusterización:** Aplicación de **KMeans** para segmentar clientes en 36 grupos según su comportamiento.
- **Eliminación de variables sesgadas:** Variables como `LoyaltyPoints` y `ConversionRate` fueron descartadas.

### **3. Modelado**
- **Modelos probados:** Random Forest, Gradient Boosting, XGBoost.
- **Modelo seleccionado:** Gradient Boosting.
  - **Métricas:** 
    - Recall (Test): 0.92
    - Precision (Test): 0.88
    - ROC-AUC: 0.93
- **Optimización de hiperparámetros:** Uso de **GridSearchCV**.

### **4. Simulaciones**
- Personalización de canales y campañas para cada cluster utilizando los patrones de comportamiento identificados.

---

## **Resultados Clave**

- **Canales más efectivos:** `Email`, `PPC`, `Social Media`.
- **Campañas más efectivas:** 
  - **Conversion:** Enfocadas en ventas directas.
  - **Retention:** Dirigidas a clientes recurrentes.
- **Impacto:** Aumento en la efectividad del gasto publicitario, reducción de no conversiones y mayor retorno.

---

## **Requisitos**

### **Tecnologías y Librerías**
- Python 3.8+
- Jupyter Notebook
- Librerías principales:
  - `pandas`
  - `numpy`
  - `scikit-learn`
  - `matplotlib`
  - `seaborn`

---

## **Cómo Ejecutar el Proyecto**

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/MikelTelo/digital-marketing-campaign-optimizer-with-machine-learning.git
   cd digital-marketing-campaign-optimizer-with-machine-learning
