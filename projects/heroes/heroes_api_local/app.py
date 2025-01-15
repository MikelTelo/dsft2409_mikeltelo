from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import joblib
import re
import pandas as pd
import http.server
import socketserver
import json
from urllib.parse import parse_qs, urlparse
import os
import io

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

# Load model globally
model, vectorizer = load_model()

class PredictorHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        
        # Parse URL path
        path = urlparse(self.path).path
        
        if path == '/predict':
            # Handle prediction request
            data = parse_qs(post_data)
            text = data.get('text', [''])[0]
            
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
                
        elif path == '/retrain':
            try:
                # Get Content-Type header
                content_type = self.headers.get('Content-Type', '')
                retrain_type = None
                file_content = None
                
                # Cargar el dataset original primero
                original_data_path = Path(__file__).parent / 'data' / 'superheroes_nlp_dataset.csv'
                if not original_data_path.exists():
                    raise Exception("Original dataset file not found")
                original_data = pd.read_csv(original_data_path)
                print(f"Original dataset loaded with {len(original_data)} rows")

                if 'multipart/form-data' in content_type:
                    # Parse boundary
                    boundary = content_type.split('boundary=')[1].encode()
                    parts = post_data.split(boundary.decode())
                    
                    # Parse multipart form data
                    for part in parts:
                        if 'name="type"' in part:
                            retrain_type = part.split('\r\n\r\n')[1].split('\r\n')[0]
                        elif 'name="file"' in part and 'filename=' in part:
                            # Extract file content
                            file_content = part.split('\r\n\r\n')[1].rsplit('\r\n', 1)[0]
                else:
                    # Handle regular form data
                    data = parse_qs(post_data)
                    retrain_type = data.get('type', [''])[0]

                if not retrain_type:
                    raise Exception("Retrain type not specified")

                if retrain_type == 'existing':
                    # Usar solo el dataset original
                    data = original_data
                    print("Using existing dataset")
                else:
                    # Verificar que se haya subido un archivo
                    if not file_content:
                        raise Exception("No file uploaded")
                    
                    # Cargar el nuevo dataset
                    new_data = pd.read_csv(io.StringIO(file_content))
                    print(f"New dataset loaded with {len(new_data)} rows")
                    
                    # Combinar ambos datasets
                    data = pd.concat([original_data, new_data], ignore_index=True)
                    print(f"Combined dataset has {len(data)} rows")

                # Verify required columns
                required_columns = ['history_text', 'alignment']
                missing_columns = [col for col in required_columns if col not in data.columns]
                if missing_columns:
                    raise Exception(f"Missing required columns: {', '.join(missing_columns)}")

                print("Starting model retraining...")
                accuracy, report = retrain_model(data)
                print("Model retrained successfully")
                
                response = {
                    'success': True,
                    'accuracy': float(accuracy),
                    'report': report
                }
            except Exception as e:
                print(f"Error in retraining: {str(e)}")
                response = {'error': str(e)}
        else:
            response = {'error': 'Invalid endpoint'}

        # Send response
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())

    def do_GET(self):
        if self.path == '/':
            self.path = '/index.html'
        try:
            # First try to send the file
            return http.server.SimpleHTTPRequestHandler.do_GET(self)
        except Exception as e:
            # If there's an error, print it and send 404
            print(f"Error serving file: {str(e)}")
            self.send_error(404, "File not found")

def run_server(port=8000):
    handler = PredictorHandler
    
    print(f"Current directory: {os.getcwd()}")
    print(f"Files in directory: {os.listdir('.')}")
    
    with socketserver.TCPServer(("", port), handler) as httpd:
        print(f"Serving at http://localhost:{port}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server...")
            httpd.shutdown()

if __name__ == '__main__':
    run_server()