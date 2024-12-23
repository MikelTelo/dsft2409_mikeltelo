#CONSTANTES DEL PROGRAMA
#-----------------------------------------------------
AGUA = 0 #Se trata de una casilla que no tiene barco.
BARCO = 1 #Se trata de una casilla en la que hay un barco.
TOCADO = 2 #Se trata de una casilla la cual la hemos dado en un barco.
FALLADO = 3 #Se trata de una casilla en la cual nosotros hemos atacado pero hemos fallado (No había objetivo).

#Dimensiones para poder crear el tablero.
DIMENSIONES_TABLERO = 10

BARCOS = { #Creamos un diccionario de Barcos en donde crearemos 1 barco de 4 posiciones, otro de...
    1: 4,
    2: 3,
    3: 2,
    4: 1
}