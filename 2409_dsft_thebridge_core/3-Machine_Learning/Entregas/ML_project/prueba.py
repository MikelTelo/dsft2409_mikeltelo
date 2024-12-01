import pandas as pd
import pickle
import datetime
dia_de_hoy = datetime.datetime.now().date()

# df = pd.read_csv('../data/train.csv')
# model = 'Hola'
# pickle.dump(model, open('hola', 'wb'))
model = pickle.load(open('C:/Users/misla/Documents/Bootcamp/DS_TheBridgeBBK_SBIL2023/3-Machine_Learning/Entregas/ML_project/hola', 'rb'))
print(model)

predictions = model.predict(X_train)
pd.DataFrame(predictions, columns= 'Predicciones').to_csv(f'../data/predicciones_{dia_de_hoy}.csv')

# hola_mundo_2 = pickle.load(open('data/ejemplo.pkl', 'rb'))