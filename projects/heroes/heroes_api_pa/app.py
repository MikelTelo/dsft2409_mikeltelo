from flask import Flask, request, jsonify, send_from_directory
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import joblib
import re
import pandas as pd
import json
import os
import io

app = Flask(__name__)

# Change working directory to the script's directory
os.chdir(Path(__file__).parent)

# Load model and vectorizer
def load_model():
    try:
        model_path = Path(__file__).parent / 'model' / 'svc_model.pkl'
        vectorizer_path = Path(__file__).parent / 'model' / 'tfidf_vectorizer.pkl'
        
        # Check if model files exist
        if not model_path.exists() or not vectorizer_path.exists():
            print("Model files not found. Training new model...")
            # Load CSV and train model
            data_path = Path(__file__).parent / 'data' / 'superheroes_nlp_dataset.csv'
            if not data_path.exists():
                raise Exception("Dataset file not found at: " + str(data_path))
            
            data = pd.read_csv(data_path)
            accuracy, report = retrain_model(data)
            print(f"Model trained successfully! Accuracy: {accuracy:.2f}")
            print("\nClassification Report:\n", report)
        
        # Load model and vectorizer
        model = joblib.load(str(model_path))
        vectorizer = joblib.load(str(vectorizer_path))
        
        if model is None or vectorizer is None:
            raise Exception("Error loading model or vectorizer")
            
        return model, vectorizer
    except Exception as e:
        print(f"Error loading/training model: {str(e)}")
        return None, None

# Preprocess text
def preprocess_text(text):
    # Handle NaN values
    if pd.isna(text):
        return ""
    
    text = str(text).lower()
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

# Prediction function
def predict_alignment(text, model, vectorizer, threshold=0.5):
    text = preprocess_text(text)
    text_vectorized = vectorizer.transform([text])
    try:
        probs = model.predict_proba(text_vectorized)[0]
    except ValueError:
        text_vectorized = text_vectorized.toarray()
        probs = model.predict_proba(text_vectorized)[0]
    
    prediction = "Hero" if probs[1] > threshold else "Villain"
    return prediction, probs[1], probs[0]

# Retrain model function
def retrain_model(data, test_size=0.2):
    # Clean and prepare data
    print("Cleaning and preparing data...")
    
    # Remove rows with NaN values
    data = data.dropna(subset=['history_text', 'alignment'])
    
    # Ensure text is string and clean
    data['history_text'] = data['history_text'].apply(preprocess_text)
    
    # Remove empty texts
    data = data[data['history_text'].str.len() > 0]
    
    if len(data) == 0:
        raise Exception("No valid data after cleaning")
    
    print(f"Training with {len(data)} valid samples")
    
    # Prepare data
    X = data['history_text']
    y = data['alignment']
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=42
    )
    
    # Initialize and fit vectorizer
    print("Vectorizing text data...")
    vectorizer = TfidfVectorizer(max_features=5000)
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)
    
    # Train model
    print("Training model...")
    model = SVC(probability=True, kernel='linear')
    model.fit(X_train_vec, y_train)
    
    # Evaluate
    print("Evaluating model...")
    y_pred = model.predict(X_test_vec)
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred)
    
    # Save model and vectorizer
    print("Saving model and vectorizer...")
    model_dir = Path(__file__).parent / 'model'
    model_dir.mkdir(exist_ok=True)
    
    joblib.dump(model, model_dir / 'svc_model.pkl')
    joblib.dump(vectorizer, model_dir / 'tfidf_vectorizer.pkl')
    
    return accuracy, report

# Cargar el modelo globalmente
model, vectorizer = load_model()

@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.form
        text = data.get('text', '')
        
        if model is not None and vectorizer is not None:
            prediction, hero_prob, villain_prob = predict_alignment(text, model, vectorizer)
            response = {
                'prediction': prediction,
                'hero_probability': float(hero_prob),
                'villain_probability': float(villain_prob),
                'confidence': float(max(hero_prob, villain_prob))
            }
        else:
            response = {'error': 'Model not loaded properly'}
        
        return jsonify(response)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/retrain', methods=['POST'])
def retrain():
    try:
        retrain_type = request.form.get('type')
        
        # Cargar el dataset original
        original_data_path = Path(__file__).parent / 'data' / 'superheroes_nlp_dataset.csv'
        if not original_data_path.exists():
            return jsonify({'error': 'Original dataset file not found'}), 404
        
        original_data = pd.read_csv(original_data_path)
        
        if retrain_type == 'existing':
            data = original_data
        else:
            if 'file' not in request.files:
                return jsonify({'error': 'No file uploaded'}), 400
            
            file = request.files['file']
            new_data = pd.read_csv(file)
            data = pd.concat([original_data, new_data], ignore_index=True)
        
        accuracy, report = retrain_model(data)
        
        return jsonify({
            'success': True,
            'accuracy': float(accuracy),
            'report': report
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run()