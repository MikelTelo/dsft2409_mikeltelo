# Inicialización de la biblioteca con 3 libros
biblioteca = [
    {"titulo": "Super", "autor": "man", "año": 1800},
    {"titulo": "mega", "autor": "man", "año": 1900},
    {"titulo": "ultra", "autor": "mega", "año": 2000}
]

# Función para mostrar el menú y manejar las opciones
def menu():
    while True:
        print("\n--- Menú de Biblioteca ---")
        print("1. Imprimir biblioteca")
        print("2. Buscar libro por título")
        print("3. Añadir libro")
        print("4. Eliminar libro por autor")
        print("5. Salir")
        
        opcion = input("Selecciona una opción (1-5): ")

        if opcion == '1':
            imprimir_biblioteca()
        elif opcion == '2':
            buscar_libro_por_titulo()
        elif opcion == '3':
            anadir_libro()
        elif opcion == '4':
            eliminar_libro_por_autor()
        elif opcion == '5':
            print('Gracias por usar nuestros servicios. Adiós.')
            break
        else:
            print("Opción no válida. Por favor, selecciona una opción entre 1 y 5.")

# Función para imprimir la biblioteca
def imprimir_biblioteca():
    if len(biblioteca) == 0:
        print("La biblioteca está vacía.")
    else:
        for i, libro in enumerate(biblioteca):
            print(f"{i+1}. Título: {libro['titulo']}, Autor: {libro['autor']}, Año: {libro['año']}")
        print()  # Espacio adicional para claridad

# Función para buscar un libro por título
def buscar_libro_por_titulo():
    titulo = input("Introduce el título del libro a buscar: ")
    encontrado = False
    for libro in biblioteca:
        if libro["titulo"].lower() == titulo.lower():
            print(f"Título: {libro['titulo']}, Autor: {libro['autor']}, Año: {libro['año']}")
            encontrado = True
            break
    if not encontrado:
        print("No se encontró ningún libro con ese título.")

# Función para añadir un libro
def anadir_libro():
    titulo = input("Introduce el título del libro: ")
    autor = input("Introduce el autor del libro: ")
    try:
        año = int(input("Introduce el año de publicación: "))
        nuevo_libro = {"titulo": titulo, "autor": autor, "año": año}
        biblioteca.append(nuevo_libro)
        print(f"Libro '{titulo}' añadido con éxito.")
    except ValueError:
        print("El año debe ser un número. No se añadió el libro.")

# Función para eliminar libros por autor
def eliminar_libro_por_autor():
    autor = input("Introduce el autor del libro a eliminar: ")
    libros_eliminados = [libro for libro in biblioteca if libro["autor"].lower() == autor.lower()]
    
    if libros_eliminados:
        for libro in libros_eliminados:
            biblioteca.remove(libro)
        print(f"Se han eliminado {len(libros_eliminados)} libro(s) del autor '{autor}'.")
    else:
        print(f"No se encontró ningún libro del autor '{autor}'.")

# Ejecutar el menú
menu()