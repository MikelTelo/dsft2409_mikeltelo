from flask import Flask, request, jsonify
import os
import pickle
from sklearn.model_selection import cross_val_score
import pandas as pd
import sqlite3


os.chdir(os.path.dirname(__file__))

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route("/", methods=['GET'])
def hello():
    return "Bienvenido a mi API del modelo advertising"

#1

@app.route('/v2/predict', methods=['GET'])
def predict():
    model = pickle.load(open('data/advertising_model','rb'))

    tv = request.args.get('tv', None)
    radio = request.args.get('radio', None)
    newspaper = request.args.get('newspaper', None)

    if tv is None or radio is None or newspaper is None:
        return "Missing args, the input values are needed to predict"
    else:
        prediction = model.predict([[int(tv),int(radio), int(newspaper)]])
        return "The prediction of sales investing that amount of money in TV, radio and newspaper is: " + str(round(prediction[0],2)) + 'k €'    
    
#2
@app.route('/v2/ingest_data', methods=['POST'])
def ingest_data():
    connection = sqlite3.connect('data/advertising.db')
    cursor = connection.cursor()

    tv = request.args.get('tv', None)
    radio = request.args.get('radio', None)
    newspaper = request.args.get('newspaper', None)
    sales = request.args.get('sales', None)

    query = '''INSERT INTO campañas VALUES (?, ?, ?, ?)'''
    query_2 = "SELECT * FROM campañas"

    cursor.execute(query, (tv, radio, newspaper, sales))
    result = cursor.execute(query_2).fetchall()

    connection.commit()
    connection.close()

    return result

#3
@app.route('/v2/retrain', methods=['PUT'])
def retrain():
    connection = sqlite3.connect('data/advertising.db')
    cursor = connection.cursor()

    query = '''SELECT * FROM campañas'''
    result = cursor.execute(query).fetchall()

    columns = [columns[0] for columns in cursor.description]

    df = pd.DataFrame(data= result, columns= columns)
    df.dropna(inplace= True)

    X = df.drop(columns= ('sales'))
    Y = df['sales']

    model = pickle.load(open('data/advertising_model', 'rb'))
    mae_1 = - (cross_val_score(model, X, Y, cv = 5, scoring= 'neg_mean_absolute_error')).mean()

    model.fit(X, Y)
    mae_2 = - (cross_val_score(model, X, Y, cv = 5, scoring= 'neg_mean_absolute_error')).mean()

    if mae_2 < mae_1:
        pickle.dump(model, open('data/advertising_model', 'wb'))
        return f'Your new model is better, mae = {mae_2}'
    
    else:
        return f'Your old model is better, mae = {mae_1}'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)