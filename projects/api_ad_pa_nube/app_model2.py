from flask import Flask, jsonify, request, render_template
import os
import pickle
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import Lasso
from sklearn.metrics import mean_squared_error, mean_absolute_percentage_error
import numpy as np

# Obtén la ruta raíz del proyecto
root_path = os.path.dirname(os.path.abspath(__file__))

# Crea la aplicación Flask
app = Flask(__name__, template_folder='templates')
app.config['DEBUG'] = True

# Página principal
@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

# Endpoint para predicción
@app.route("/api/v1/predict", methods=['POST'])
def predict():
    try:
        # Ruta al modelo
        model_path = os.path.join(root_path, 'ad_model.pkl')
        if not os.path.exists(model_path):
            return jsonify({'error': 'El archivo del modelo no se encontró. Por favor, reentrena el modelo primero.'}), 500

        # Carga del modelo
        with open(model_path, 'rb') as file:
            model = pickle.load(file)

        # Obtener parámetros del formulario
        tv = request.form.get('tv', None)
        radio = request.form.get('radio', None)
        newspaper = request.form.get('newspaper', None)

        # Validación de parámetros
        if tv is None or radio is None or newspaper is None:
            return jsonify({'error': 'Faltan argumentos (tv, radio, newspaper) para realizar la predicción.'}), 400

        # Predicción
        prediction = model.predict([[float(tv), float(radio), float(newspaper)]])
        return render_template('index.html', prediction=round(prediction[0], 2))

    except Exception as e:
        return render_template('index.html', error=f'Error durante la predicción: {str(e)}')

# Endpoint para reentrenar el modelo
@app.route('/api/v1/retrain', methods=['POST'])
def retrain():
    try:
        # Ruta a los datos
        data_path = os.path.join(root_path, 'data', 'Advertising_new.csv')
        if not os.path.exists(data_path):
            return jsonify({'error': 'No se encontró el archivo de datos para reentrenar el modelo.'}), 404

        # Carga de datos
        data = pd.read_csv(data_path)

        # Separación de datos
        X_train, X_test, y_train, y_test = train_test_split(
            data.drop(columns=['sales']),
            data['sales'],
            test_size=0.20,
            random_state=42
        )

        # Entrenamiento del modelo
        model = Lasso(alpha=6000)
        model.fit(X_train, y_train)

        # Evaluación del modelo
        rmse = np.sqrt(mean_squared_error(y_test, model.predict(X_test)))
        mape = mean_absolute_percentage_error(y_test, model.predict(X_test))

        # Guardar el modelo entrenado
        model_path = os.path.join(root_path, 'ad_model.pkl')
        with open(model_path, 'wb') as file:
            pickle.dump(model, file)

        return render_template('index.html', message=f'Modelo reentrenado con éxito. RMSE: {round(rmse, 2)}, MAPE: {round(mape, 2)}')

    except Exception as e:
        return render_template('index.html', error=f'Error durante el reentrenamiento: {str(e)}')

# Iniciar la aplicación
if __name__ == "__main__":
    app.run()

# Archivo HTML en la carpeta 'templates' (index.html)

"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>API Advertising</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha3/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <div class="container mt-5">
        <h1 class="text-center">API Advertising</h1>
        <hr>
        <h2>Hacer una predicción</h2>
        <form method="POST" action="/api/v1/predict">
            <div class="mb-3">
                <label for="tv" class="form-label">TV</label>
                <input type="number" step="0.01" class="form-control" id="tv" name="tv" required>
            </div>
            <div class="mb-3">
                <label for="radio" class="form-label">Radio</label>
                <input type="number" step="0.01" class="form-control" id="radio" name="radio" required>
            </div>
            <div class="mb-3">
                <label for="newspaper" class="form-label">Newspaper</label>
                <input type="number" step="0.01" class="form-control" id="newspaper" name="newspaper" required>
            </div>
            <button type="submit" class="btn btn-primary">Predecir</button>
        </form>
        {% if prediction %}
            <div class="alert alert-success mt-3">Predicción: {{ prediction }}</div>
        {% endif %}
        {% if error %}
            <div class="alert alert-danger mt-3">Error: {{ error }}</div>
        {% endif %}
        <hr>
        <h2>Reentrenar el modelo</h2>
        <form method="POST" action="/api/v1/retrain">
            <button type="submit" class="btn btn-warning">Reentrenar</button>
        </form>
        {% if message %}
            <div class="alert alert-success mt-3">{{ message }}</div>
        {% endif %}
    </div>
</body>
</html>
"""