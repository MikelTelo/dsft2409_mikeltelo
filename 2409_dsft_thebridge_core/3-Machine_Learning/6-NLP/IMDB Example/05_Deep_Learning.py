import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
#from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report,confusion_matrix
import pickle
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
import joblib
import warnings
warnings.filterwarnings("ignore")
from tensorflow.keras.callbacks import EarlyStopping


import sys

import sys
#sys.path.append('/Users/34632/TheBridge/htools/')
#from Toolbox_ML import *


suffix = 73 #sys.argv[1]


print()
# Load dataset
df = pd.read_csv('data/IMDB Dataset.csv')
print(df.head(10))
print(df.info())

# Preprocessing
df['review'] = df['review'].str.lower()

# Splitting data
X_train, X_test, y_train, y_test = train_test_split(df['review'], df['sentiment'], test_size=0.2, random_state=42)

# Vectorization
vectorizer = TfidfVectorizer(stop_words='english', max_df=0.7)
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

print('The sentiment data for training is organized in a matrix.')
print('Num. reviews (rows): ',X_train_vec.shape[0])
print('Num. tokens: (columns)',X_train_vec.shape[1])
print()

# Definición del modelo
model = Sequential()

# Capa de entrada
model.add(Dense(512, input_shape=(X_train_vec.shape[1],), activation='relu'))
model.add(Dropout(0.5))

# Primera capa oculta
model.add(Dense(256, activation='relu'))
model.add(Dropout(0.5))

# Segunda capa oculta
model.add(Dense(128, activation='relu'))
model.add(Dropout(0.5))

# Tercera capa oculta
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))

# Capa de salida
model.add(Dense(1, activation='sigmoid'))

# Compilación del modelo
model.compile(optimizer='adam',
              loss='binary_crossentropy',
              metrics=['accuracy'])


print(model.summary())

print('Converting output to number...')
y_train = y_train == 'positive'
y_test  = y_test  == 'positive'

early_stopping = EarlyStopping(
    monitor='val_loss',  # The metric to monitor
    patience=3,          # Number of epochs with no improvement after which training will be stopped
    verbose=1,           # Verbosity mode (0 or 1)
    mode='min',          # Mode should be 'min' for 'val_loss' as we want to minimize the loss
    restore_best_weights=True # Whether to restore model weights from the epoch with the best value of the monitored quantity
)

print('Shapes')
print(X_train_vec.shape)
print(y_train.values.shape)
print('Training...')
model.fit(X_train_vec, y_train, epochs= 50, callbacks=[early_stopping])

# Model evaluation
print('Evaluating the model...')
print()
print('The following depicts the ability, the goodness, to tell the correct sentiment of a critic, \
      positive vs negative, for all the test critics, which the Model will now see for the first time. Overall accuracy:')
predictions = model.predict(X_test_vec) >= 0.5
print("Accuracy:", accuracy_score(y_test, predictions))
print()
print('The Classification Report')
print()
print("Classification Report:\n", classification_report(y_test, predictions))
print()
confusion_m = confusion_matrix(y_test,predictions)
print('The Confussion Matrix:')
print('x-axis is predicted while y-axis is true label.')
print()
print(confusion_m)
print()



#with open('review1.txt') as f0:
#    # Read the contents of the file
#    new_review = f0.read()
#    new_review_list = [new_review]

#print('Review 1 is:', new_review)
#new_review_vec = vectorizer.transform(new_review_list)
#print('Shape of review1.txt',new_review_vec.shape)
#prediction = model.predict(new_review_vec)
#print(f'Prediction is {'positive' if prediction > 0.5 else 'negative'}')

#with open('review2.txt') as f0: 
#    # Read the contents of the file
#    new_review = f0.read()
#    new_review_list = [new_review]

#print('Review 2 is:', new_review)
#new_review_vec = vectorizer.transform(new_review_list)
#print('Shape of review2.txt',new_review_vec.shape)
#prediction = model.predict(new_review_vec)
#print(f'Prediction is {'positive' if prediction > 0.5 else 'negative'}')