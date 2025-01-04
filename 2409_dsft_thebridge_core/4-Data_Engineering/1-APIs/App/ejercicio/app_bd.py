import json
from flask import Flask, request, jsonify
import sqlite3
import os

os.chdir(os.path.dirname(__file__))

app = Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def welcome():
    return "Welcome to mi API conected to my books database"

@app.route('/api/v1/resources/books/all', methods=['GET'])
def get_all():
    connection = sqlite3.connect('books.db')
    cursor = connection.cursor()
    select_books = "SELECT * FROM books"
    result = cursor.execute(select_books).fetchall()
    connection.close()
    return result

# 1.Ruta para obtener el conteo de libros por autor ordenados de forma descendente
@app.route('/api/v1/resources/books/count', methods=['GET'])
def count_books():
    connection = sqlite3.connect('books.db')
    cursor = connection.cursor()
    select_books = '''SELECT author, COUNT(title) AS Conteo FROM books
                        GROUP BY author
                        ORDER BY Conteo
                        DESC'''
    result = cursor.execute(select_books).fetchall()
    connection.close()
    return result

# 2.Ruta para obtener los libros de un autor como argumento en la llamada
@app.route('/api/v1/resources/books/by_author', methods=['GET'])
def books_by_author():
    connection = sqlite3.connect('books.db')
    cursor = connection.cursor()

    author = request.args.get('author')

    select_books = '''SELECT title FROM books
                     WHERE author = ?'''
    
    result = cursor.execute(select_books, (author,)).fetchall()
    connection.close()
    return result

# 3.Ruta para obtener los libros filtrados por título, publicación y autor
@app.route('/api/v1/resources/books/filtered', methods=['GET'])
def books_filtered():
    connection = sqlite3.connect('books.db')
    cursor = connection.cursor()

    author = "%" + request.args.get('author') + "%"
    title = request.args.get('title')
    published = request.args.get('published')

    select_books = '''SELECT * FROM books
                        WHERE author LIKE ?
                        AND title = ?
                        AND published = ?'''
    
    result = cursor.execute(select_books, (author,title, published)).fetchall()
    connection.close()
    return result
app.run()