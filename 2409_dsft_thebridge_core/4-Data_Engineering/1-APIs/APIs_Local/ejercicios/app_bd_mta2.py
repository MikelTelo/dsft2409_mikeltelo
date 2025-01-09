from flask import Flask, jsonify, request, abort
import sqlite3
import os

os.chdir(os.path.dirname(os.path.dirname(__file__)))

app = Flask(__name__)
app.config["DEBUG"] = True

# Helper function to interact with the database
def query_db(query, args=(), one=False):
    with sqlite3.connect("books.db") as conn:
        conn.row_factory = sqlite3.Row  # Enables dict-like access to rows
        cur = conn.cursor()
        cur.execute(query, args)
        rv = cur.fetchall()
        conn.commit()
        return (rv[0] if rv else None) if one else rv


@app.route('/', methods=['GET'])
def welcome():
    return "<h1>Books API</h1><p>Welcome to the Books API. Use the endpoints to interact with the database.</p>"


@app.route('/api/v1/resources/books/all', methods=['GET'])
def all_books():
    books = query_db("SELECT * FROM books")
    return jsonify([dict(book) for book in books])


# 1. Ruta para obtener el conteo de libros por autor ordenados de forma descendente
@app.route('/api/v1/resources/books/count', methods=['GET'])
def count_books():
    books_count = query_db(
        "SELECT author, COUNT(*) as count FROM books GROUP BY author ORDER BY count DESC"
    )
    return jsonify([dict(row) for row in books_count])


# 2. Ruta para obtener los libros de un autor como argumento en la llamada
@app.route('/api/v1/resources/books/by_author', methods=['GET'])
def books_by_author():
    if 'author' in request.args:
        author = request.args.get('author')
        books = query_db("SELECT * FROM books WHERE author = ?", (author,))
        if books:
            return jsonify([dict(book) for book in books])
        else:
            return jsonify({'message': 'No books found for this author.'})
    else:
        abort(400, 'You must provide an author argument.')


# 3. Ruta para obtener los libros filtrados por título, publicación y autor
@app.route('/api/v1/resources/books/filtered', methods=['GET'])
def books_filtered():
    filters = []
    values = []

    if 'title' in request.args:
        filters.append("title LIKE ?")
        values.append(f"%{request.args.get('title')}%")

    if 'author' in request.args:
        filters.append("author LIKE ?")
        values.append(f"%{request.args.get('author')}%")

    if 'published' in request.args:
        filters.append("published LIKE ?")
        values.append(f"%{request.args.get('published')}%")

    if filters:
        query = "SELECT * FROM books WHERE " + " AND ".join(filters)
        books = query_db(query, values)
        if books:
            return jsonify([dict(book) for book in books])
        else:
            return jsonify({'message': 'No books found matching the filters.'})
    else:
        abort(400, 'You must provide at least one filter (title, author, published).')


if __name__ == "__main__":
    app.run()
