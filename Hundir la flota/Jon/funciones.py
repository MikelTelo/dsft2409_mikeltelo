import random
from variables import *

#FUNCIONES PARA EL JUEGO DE HUNDIR LA FLOTA
#------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
def colocarBarcos(tablero): #En dicha función, vamos a tener que pasarle como argumento el tablero generado anteriormente ya que en él vamos a colocar los barcos.
    posiciones_barcos = [] #Creamos una lista vacía para almacenar las posiciones de los barcos
    for tamanio, cantidad in BARCOS.items(): #Método diccionario --> devuelve lista tuplas (cada una de ellas contienen clave-valor)
        #Creamos un contador de barcos que van a irse colocando.
        cont_barcos = 0 #En principio, no hemos colocado ninguno, iremos incrementando el número de barcos a poner. Por eso lo inicializaremos a 0.
        while cont_barcos < cantidad: #Creamos un bucle While el cual mientras el contador de barcos que hemos inicializado a 0 debido a que aun no hemos colocado ninguno.
        #Este bucle se hará hasta llegar a 10 que es el máximo número de barcos que hemos puesto para poner en el tablero.
            posicion = random.choice(["Vertical","Horizontal"]) #Hará la elección de la posición de manera random, eligiendo o vertical o horizontal.
            fila = random.randint(0,DIMENSIONES_TABLERO-1) #Se elegirá de manera random una fila al azar.
            columna = random.randint(0,DIMENSIONES_TABLERO-1) #Se elegirá de manera random una columna al azar.
            #Ahora bien, necesitamos saber si el barco puede añadirse en dicha posicion, para ello:
            if puede_colocarse_barco(tablero,fila,columna,tamanio,posicion): #Nos llevará a una función la cual nos dirá si dicho barco podemos colocarlo.
                colocarBarco(tablero,fila,columna,tamanio,posicion) 
                if posicion == "Vertical":
                    posiciones_barcos.append([(fila + i, columna) for i in range(tamanio)])  # Guardamos lo que son las posiciones verticales (lo que quiere decir es que guarda las posiciones de cada barco en el tablero, incluyendo todas las celdas que ocupa el barco, en una lista llamada posiciones_barcos)
                else:
                    posiciones_barcos.append([(fila, columna + j) for j in range(tamanio)])  # Guardamos las posiciones horizontales
                cont_barcos += 1
    return posiciones_barcos  # Devolvemos las posiciones de los barcos colocados
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
def puede_colocarse_barco(tablero,fila,columna,tamanio,posicion): #Esta función se crea para saber si vamos a poder poner el barco en la posición que se quiera.
    if posicion == "Vertical": #Comenzamos probando con la posicion en vertical.
        if fila + tamanio > DIMENSIONES_TABLERO: #En caso de que el barco se salga del tablero. Miramos si cabe el barco de manera vertical
            return False; #Devolvemos false.
        for i in range(tamanio): #Se tendrá que ir observando cada celda en la cual irá el barco.
            if tablero[fila + i][columna] != AGUA: #En caso de haber un barco en esas celdas del tablero, devolveremos False.
                return False #Devolvemos false.
    elif posicion == "Horizontal":
        if columna + tamanio > DIMENSIONES_TABLERO: #Lo mismo que en vertical.
            return False
        for j in range(tamanio):
            if tablero[fila][columna + j] != AGUA:
                return False 
    return True #Se hará un return de True en caso de que haya superado las condiciones.
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
def colocarBarco(tablero,fila,columna,tamanio,posicion): #Esta función es la que se encarga de poner el barco en el tablero.
    if posicion == "Vertical": 
        for i in range(tamanio): #Este for lo que va a hacer es ir recorriendo una a una las celdas colocandose el barco en la posicion vertical.
            tablero[fila + i][columna] = BARCO
    elif posicion == "Horizontal":
        for j in range(tamanio):
            tablero[fila][columna + j] = BARCO
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
def visualizarTableroJugador(tablero,nombre_jugador):
    print(f"Tablero de {nombre_jugador}")
    print("---------------")
    for fila in tablero: #Recorremos todas las filas que hay en el tablero.
        for celda in fila: #Recorremos las celdas que hay en cada fila.
            if celda == TOCADO: #Si le tocamos a un barco, se verá en la celda como X.
                print("X",end="\t")
            elif celda == BARCO: #Si esta el barco puesto en dicha celda lo mostramos para que sepamos que nuestro barco esta ahí, se verá como B (de barco).
                print("B",end="\t")
            elif celda == FALLADO: #Si se ha hecho el ataque y se ha fallado se mostrará como F (de que se ha fallado)
                print("F",end="\t")
            else:
                print("A",end="\t") #Si no hay nada, ningún barco, se mostrará una A de agua.
        print()
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
def visualizarTableroRival(tablero):
    print("Tablero del Rival")
    print("-----------------")
    for fila in tablero: #Recorremos todas las filas que hay en el tablero.
        for celda in fila: #Recorremos las celdas que hay en cada fila.
            if celda == TOCADO: #Si le tocamos a un barco, se verá en la celda como X.
                print("X",end="\t")
            elif celda == BARCO: #Si esta el barco puesto en dicha celda lo mostramos para que sepamos que nuestro barco esta ahí, se verá como B (de barco).
                print("B",end="\t") #-->>> No nos interesa ver los barcos del rival, sino no tendría gracia
            elif celda == FALLADO: #Si se ha hecho el ataque y se ha fallado se mostrará como F (de que se ha fallado)
                print("F",end="\t")
            else:
                print("A",end="\t") #Si no hay nada, ningún barco, se mostrará una A de agua.
        print()
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#Función de ataque del jugador
def ataque_jugador(tablero,fila_ataque,columna_ataque):
    if tablero[fila_ataque][columna_ataque] == BARCO: #Si hay un barco en la posicion que ha dicho el usuario de atacar...
        print("¡TOCADO!")
        tablero[fila_ataque][columna_ataque] = TOCADO #Lo marcamos como tocado.
        return True #El jugador acierta y puede atacar de nuevo
    elif tablero[fila_ataque][columna_ataque] == AGUA: #Es decir, si ahora no hay un barco en esa posición, osea AGUA solamente...
        print("¡AGUA!")
        tablero[fila_ataque][columna_ataque] = FALLADO #Marcamos como que dicho ataque ha fallado.
        return False #Falla ataque y termina el turno del jugador.
    else:
        print("Ya has atacado en esta posición")
        return False #Si ya atacó antes en la posición elegida, se considera como fallo y la partida se termina.
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#Función ataque del rival
def ataque_rival(tablero,fila_ataque_rival,columna_ataque_rival):
    while tablero[fila_ataque_rival][columna_ataque_rival] == TOCADO or tablero[fila_ataque_rival][columna_ataque_rival] == FALLADO: #Lo que hacemos aquí es verificar el ataque del rival
        #Si la máquina ya ha atacado esta posición, este elige otra posición
        fila_ataque_rival = random.randint(0,DIMENSIONES_TABLERO-1)
        columna_ataque_rival = random.randint(0,DIMENSIONES_TABLERO-1)
    if tablero[fila_ataque_rival][columna_ataque_rival] == BARCO: #Si el rival ha acertado debido a que hay un barco en esa posición...
        print(f"¡El rival ataca en {fila_ataque_rival},{columna_ataque_rival} y tu barco ha sido TOCADO!")
        tablero[fila_ataque_rival][columna_ataque_rival] = TOCADO
        return True
    else:
        print(f"El rival ataca en {fila_ataque_rival},{columna_ataque_rival} y has tenido suerte debido a que era AGUA")
        tablero[fila_ataque_rival][columna_ataque_rival] = FALLADO
        return False
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#Función de si el barco ha sido destruido o no
#Esta función lo que va a ir haciendo es ir recorriendo cada barco (pero las posiciones de los barcos de la lista)
def barco_destruido(tablero, barcos_posiciones):
    for barco in barcos_posiciones:
        if all(tablero[fila][columna] == TOCADO for fila, columna in barco):  #Entonces, si todas las partes del barco han sido tocadas = Barco destruido
            barcos_posiciones.remove(barco)  #Por tanto lo eliminamos de la lista
            return True
    return False