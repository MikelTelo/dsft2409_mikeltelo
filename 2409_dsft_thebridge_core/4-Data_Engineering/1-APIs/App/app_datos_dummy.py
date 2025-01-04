from flask import Flask, jsonify, request, abort
from datos_dummy import books

app = Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    return "<h1>My API</h1><p>This site is a prototype API for distant reading of science fiction novels.</p>"

# 1.Ruta para obtener todos los libros
@app.route('/v1/all_books', methods=['GET'])
def all_books():
    return books

# 2.Ruta para obtener un libro concreto mediante su id como parámetro en la llamada
@app.route('/v1/book_by_id', methods=['GET'])
def book_by_id():
    book_returned = []
    if 'id' in request.args:
        id = int(request.args.get('id'))
        for book in books:
            if book['id'] == id:
                book_returned.append(book)
        
        if len(book_returned) == 0:
            return abort(404, 'Book not found.')
        
        else:
            return book_returned
    
    else:
        abort(404, 'You must provide an id.')

# 3.Ruta para obtener un libro concreto mediante su título como parámetro en la llamada utilzando al final del endpoint <string:title>@app.route('/v1/book_by_id', methods=['GET'])
@app.route('/v1/book_by_title/<string:title>', methods=['GET'])
def book_by_name(title):
    # titulo = title
    for book in books:
        if book['title'] == title:
            return book

    
# 4.Ruta para obtener un libro concreto mediante su titulo dentro del cuerpo de la llamada
@app.route('/v1/book_by_title_args/', methods=['GET'])
def book_by_title():
    if 'title' in request.args:
        title = request.args.get('title')

        for book in books:
            if book['title'] == title:
                return book
    
    else:
        return 'You must provide a title argument.'
    
# 5.Ruta para añadir un libro mediante un json en la llamada
@app.route('/v1/add_book/', methods=['POST'])
def add_book():
    new_book = request.get_json()
    books.append(new_book)

    return books

# 6.Ruta para añadir un libro mediante parámetros
@app.route('/v1/add_book_params/', methods=['POST'])
def add_book_params():
    id = request.args.get('id')
    title = request.args.get('title')
    author = request.args.get('author')
    first_sentence = request.args.get('first_sentence')
    published = request.args.get('published')

    new_book = {}
    new_book['id'] = id
    new_book['title'] = title
    new_book['auhtor'] = author
    new_book['first_sentence'] = first_sentence
    new_book['published'] = published

    books.append(new_book)

    return books



# 7.Ruta para modificar un libro
@app.route('/v1/modify_book/', methods=['PUT'])
def modify_book():
    id = int(request.args.get('id'))
    published = request.args.get('published')

    for book in books:
        if book['id'] == id:
            book['published'] = published

    return books

# 8.Ruta para eliminar un libro
@app.route('/v1/delete_book/', methods=['DELETE'])
def delete_book():
    id = int(request.args.get('id'))

    for book in books:
        if book['id'] == id:
            books.remove(book)

    return books



app.run()