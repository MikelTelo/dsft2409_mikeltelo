# main.py
import os
from eda import *
import numpy as np
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix, classification_report, recall_score

#Creamos el directorio de resultados en caso de que no exista
if not os.path.exists('resultados'):
    os.makedirs('resultados')

class ModelEvaluator:

    def evaluate_model(self, model, X_train, X_test, y_train, y_test, model_name="Modelo ML"):
            print(f"\nEvaluando el modelo {model_name}...")

            #Realizamos las predicciones
            y_pred = model.predict(X_test)
            y_pred_train = model.predict(X_train)
            
            #Calculamos las puntuaciones
            train_score = model.score(X_train, y_train)
            test_score = model.score(X_test, y_test)
            
            #Calculamos y mostramos la matriz de confusión
            cm = confusion_matrix(y_test, y_pred)
            plt.figure(figsize=(10, 8))
            sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
            plt.title(f'Matriz de Confusión - {model_name}')
            plt.ylabel('Valor Real')
            plt.xlabel('Valor Predicho')
            plt.savefig(f'resultados/confusion_matrix_{model_name.lower().replace(" ", "_")}.png')
            plt.close()
            
            #Generamos el reporte de clasificación
            classification_rep = classification_report(y_test, y_pred)
            print("\nInforme de Clasificación:")
            print(classification_rep)
            
            print("\nRecall Score:", recall_score(y_test, y_pred))
            
            # Generamos el reporte completo en un archivo txt
            with open(f'resultados/reporte_{model_name.lower().replace(" ", "_")}.txt', 'w', encoding='utf-8') as f:
                f.write(f"=== Resultados del modelo {model_name} ===\n\n")
                
                #Mejores parámetros (si aplica)
                if hasattr(model, 'get_params'):
                    f.write("Mejores parámetros:\n")
                    f.write(str(model.get_params()) + "\n\n")
                
                #Realizamos el análisis por si hay overfitting
                f.write("Análisis de Overfitting:\n")
                f.write(f"Puntuación en entrenamiento: {train_score:.3f}\n")
                f.write(f"Puntuación en prueba: {test_score:.3f}\n")
                f.write(f"Diferencia (train - test): {train_score - test_score:.3f}\n\n")
                
                #Realizamos el reporte de clasificación
                f.write("Reporte de clasificación en prueba:\n")
                f.write(classification_rep + "\n")
                
                #Nos apoyamos en cualquier métrica que queremos poner por ejemplo: Recall Score
                f.write("\nRecall Score: " + str(recall_score(y_test, y_pred)) + "\n")
                
                #Añadimos información adicional si es necesario
                f.write("\n\nMatriz de Confusión guardada en: resultados/confusion_matrix_{model_name.lower().replace(' ', '_')}.png")

def main():
    # Directorio donde se encuentra el archivo CSV
    directorio = "."
    
    try:
        # Llamamos a la función de eda.py para cargar y analizar el CSV
        df = cargar_csv_de_directorio_y_analisis_basico(directorio)
        
        # Si necesitas trabajar con el DataFrame cargado, puedes hacerlo aquí
        print("\nAnálisis completado con éxito!")
        
        find_duplicates(df)
        
        #import_eda_libraries()
        
        #install_ml_libraries()
        
        #import_ml_libraries()
        
        #Generamos datos sintéticos para la prueba
        X = df.drop(columns=['Label'])
        y = df['Label']
        
        #Dividimos los datos en conjuntos de entrenamiento y prueba
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        evaluator = ModelEvaluator()
        
        #Realizamos el algoritmo de Random Forest con regularización máxima
        print("\n=== Random Forest ===")
        rf_model = RandomForestClassifier(
            n_estimators=100,            #Número de árboles
            max_depth=5,               # Profundidad mínima
            min_samples_split=50,      # Muchísimas muestras para dividir
            min_samples_leaf=25,       # Muchísimas muestras en hojas
            max_features='sqrt',       # Limitamos las features
            bootstrap=True,            # Usamos bootstrap
            max_samples=0.3,          # Usamos solo 30% de las muestras para cada árbol
            class_weight='balanced',   # Balanceamos clases
            random_state=42
        )
        rf_model.fit(X_train, y_train)
        evaluator.evaluate_model(rf_model, X_train, X_test, y_train, y_test, "Random Forest")
        
        #Realizamos el algoritmo de SVM con regularización máxima
        print("\n=== Support Vector Machine ===")
        svm_model = SVC(
            kernel='rbf',          # Kernel
            C=0.1,                 # C bajo
            class_weight='balanced', # Balanceamos clases
            random_state=42
        )
        svm_model.fit(X_train, y_train)
        evaluator.evaluate_model(svm_model, X_train, X_test, y_train, y_test, "SVM")
    
    except Exception as e:
        print(f"Hubo un error: {e}")

# Aseguramos que el código principal solo se ejecute si se ejecuta directamente este script
if __name__ == "__main__":
    main()
