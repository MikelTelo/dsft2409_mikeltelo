from variables import *

class Tablero: #Tablero se ha realizado como un objeto tablero

    def __init__(self,dimensiones=DIMENSIONES_TABLERO):
        self.dimensiones = dimensiones
        self.tablero = self.crear_tablero() #Lo que hacemos aquí es crear el tablero al inicializar dicho objeto

        #Comenzaremos con la función crear tablero del juego, para ello:
    def crearTablero():
        tablero = [] #Crearemos una variable de lista vacía la cual se usará para guardar el tablero entero.
        for i in range(DIMENSIONES_TABLERO): #Creamos un bucle el cual, se va a ir repitiendo para cada fila del tablero diez veces.
            filas = [AGUA] * DIMENSIONES_TABLERO #Dentro de la variable filas vamos a almacenarle diez celdas de agua (para cada fila).
            tablero.append(filas) #Añadimos dicha variable filas al tablero.
        return tablero #Hacemos un return del tablero entero hecho.