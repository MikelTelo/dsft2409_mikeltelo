

@app.route('/', methods=['GET'])
def welcome():


@app.route('/api/v1/resources/books/all', methods=['GET'])


# 1.Ruta para obtener el conteo de libros por autor ordenados de forma descendente
@app.route('/api/v1/resources/books/count', methods=['GET'])
def count_books():


# 2.Ruta para obtener los libros de un autor como argumento en la llamada
@app.route('/api/v1/resources/books/by_author', methods=['GET'])
def books_by_author():


# 3.Ruta para obtener los libros filtrados por título, publicación y autor
@app.route('/api/v1/resources/books/filtered', methods=['GET'])
def books_filtered():

app.run()