import json
from flask import Flask, request, jsonify
import sqlite3
import os

# Define la ruta absoluta al archivo de la base de datos
BASE_DIR = os.path.dirname(__file__)
DB_PATH = os.path.join(BASE_DIR, "books.db")

app = Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def welcome():
    return "Welcome to my API connected to my books database"

# Ruta para obtener todos los libros
@app.route('/api/v1/resources/books/all', methods=['GET'])
def get_all():
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    select_books = "SELECT * FROM books"
    result = cursor.execute(select_books).fetchall()
    connection.close()
    return jsonify([dict(zip(["id", "title", "author", "first_sentence", "published"], row)) for row in result])

# 1. Ruta para obtener el conteo de libros por autor ordenados de forma descendente
@app.route('/api/v1/resources/books/count', methods=['GET'])
def count_books():
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    select_books = '''
        SELECT author, COUNT(title) AS count FROM books
        GROUP BY author
        ORDER BY count DESC
    '''
    result = cursor.execute(select_books).fetchall()
    connection.close()
    return jsonify([{"author": row[0], "count": row[1]} for row in result])

# 2. Ruta para obtener los libros de un autor como argumento en la llamada
@app.route('/api/v1/resources/books/by_author', methods=['GET'])
def books_by_author():
    author = request.args.get('author')
    if not author:
        return jsonify({"error": "You must provide an author"}), 400

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    select_books = '''SELECT title FROM books WHERE author = ?'''
    result = cursor.execute(select_books, (author,)).fetchall()
    connection.close()
    return jsonify([{"title": row[0]} for row in result])

# 3. Ruta para obtener los libros filtrados por título, publicación y autor
@app.route('/api/v1/resources/books/filtered', methods=['GET'])
def books_filtered():
    author = request.args.get('author', "")
    title = request.args.get('title', "")
    published = request.args.get('published', "")

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    select_books = '''
        SELECT * FROM books
        WHERE author LIKE ? AND title LIKE ? AND published LIKE ?
    '''
    result = cursor.execute(select_books, (f"%{author}%", f"%{title}%", f"%{published}%")).fetchall()
    connection.close()
    return jsonify([dict(zip(["id", "title", "author", "first_sentence", "published"], row)) for row in result])

if __name__ == "__main__":
    app.run()
