import random
import pprint
import time

# A partir de aquí se definen todas las funciones que utiliza el juego Hundir la Flota
def menu_inicio():
    '''
        Muestra el menú de inicio del juego, que permite ir al juego directamente, ver las instrucciones o introducir un nombre para el jugador
    '''
    print('¡Bienvenido al Hundir la flota!')
    opcion = None
    nombre_jugador = 'Jugador'
    while opcion != '1':
        print()
        opcion = input('Selecciona una opción:\n'
                    '1. Jugar\n'
                    '2. Introducir nombre jugador\n'
                    '3. Ver instrucciones\n')
        if opcion == '2':
            nombre_jugador = input('Introduce el nombre del jugador: ')
            print(f'Jugador: {nombre_jugador}')
        elif opcion == '3':
            print("Instrucciones del juego de Hundir la flota:\n"
                "- Tablero: El juego se juega en un tablero de 10x10.\n"
                "- Barcos:\n"
                "  * 4 barcos de 1 casilla\n"
                "  * 3 barcos de 2 casillas\n"
                "  * 2 barcos de 3 casillas\n"
                "  * 1 barco de 4 casillas\n"
                "- Colocación de barcos: Los barcos de la máquina se colocan aleatoriamente en el tablero. El jugador puede elegir colocar sus barcos manualmento o aleatoriamente\n"
                "- Objetivo: Gana el primero que logre hundir todos los barcos del oponente, es decir, el que haga 20 impactos.\n"
                "- Disparo: Para atacar, introduce la fila y columna donde quieres disparar.\n"
                "- Turnos:\n"
                "  * Si aciertas y das en un barco, repetirás tu turno.\n"
                "  * Si fallas, será el turno de la máquina.\n"
                "\n¡Buena suerte!")
        elif opcion == '1':
            break
        else:
            print('No existe esa opción')
    return nombre_jugador


def crea_tablero(casillas = 10):
    '''
        Crea un tablero vacío del número de filas indicado (por defecto 10)
    '''
    fila = ['_' for _ in range(casillas)]
    tablero =[fila.copy() for _ in range(casillas)]  
    return tablero


def espacio_libre(tablero, fila, columna, tamaño, direccion):
    '''
        Verifica si se puede colocar un barco en la posicion determinada, o si esa posición ya está ocupada por otro barco
    '''
    libre = True
    if direccion == 'H':                                # Si la dirección es H, comprueba si el barco se puede colocar desde esa casilla hacia la derecha
        for i in range(tamaño):
            if tablero[fila][columna + i] == 'B':
                libre = False
                break
            else:
                libre = True
    if direccion == 'V':                                # Si la dirección es V, comprueba si el barco se puede colocar desde esa casilla hacia abajo
        for i in range(tamaño):
            if tablero[fila + i][columna] == 'B':
                libre = False
                break
            else:
                libre = True
    return libre


def colocar_barco_aleatorio(tablero, tamaño):
    '''
        Coloca un barco en la posición del tablero indicada, siempre que la funcion espacio_libre() sea True. Elige aleatoriamente unas coordenadas y una dirección.
    '''
    barco_colocado = False
    while barco_colocado == False:
        direccion = random.choice(['H', 'V'])
        if direccion == 'H':
            fila = random.randint(0, len(tablero) - 1)
            columna = random.randint(0, (len(tablero)) - tamaño)
            if espacio_libre(tablero,fila,columna,tamaño, direccion) == True:
                for i in range(tamaño):
                    tablero[fila][columna + i] = 'B'
                barco_colocado = True
        if direccion == 'V':
            fila = random.randint(0, len(tablero) - tamaño)
            columna = random.randint(0, len(tablero) - 1)
            if espacio_libre(tablero,fila,columna,tamaño, direccion) == True:
                for i in range(tamaño):
                    tablero[fila + i][columna] = 'B'
                barco_colocado = True


def colocar_barco_manual(tablero, tamaño):
    '''
        Solicita unas coordenadas y una dirección al usuario y coloca el barco en esa posición si está libre y dentro del tablero
    '''
    barco_colocado = False
    while barco_colocado == False:
        direccion = input('Introduce V para colocar el barco en vertical o H para colocarlo en horizontal: ')
        if direccion.upper() not in ['H', 'V']:
            direccion = 'H'
            print('Entrada incorrecta. Por defecto se pondrá el barco en horizontal')
        fila = solicita_fila(tablero, direccion, tamaño)
        columna = solicita_columna(tablero, direccion, tamaño)

        if direccion.upper() == 'H':
            direccion = direccion.upper()
            if espacio_libre(tablero,fila,columna,tamaño, direccion) == True:
                for i in range(tamaño):
                    tablero[fila][columna + i] = 'B'
                barco_colocado = True
        if direccion.upper() == 'V':
            direccion = direccion.upper()
            if espacio_libre(tablero,fila,columna,tamaño, direccion) == True:
                for i in range(tamaño):
                    tablero[fila + i][columna] = 'B'
                barco_colocado = True

    print(f'Barco colocado en dirección {direccion} en la posición ({fila},{columna})')


def solicita_fila(tablero, direccion, tamaño):
    '''
        Solicita al usuario que introduzca una fila y asegura que esté dentro del tablero y que el barco quepa en esa posición
    '''
    entrada_fila = False                                                            
    while not entrada_fila:
        entrada_num = False
        while not entrada_num:
            fila = input('Introduce la fila en la que quieres colocar el barco: ')
            fila, entrada_num = entrada_numero(fila, entrada_num)
        if direccion.upper() == 'H':
            if fila in range(len(tablero)):
                entrada_fila = True
            else:
                print('El barco se sale de los límites del tablero. Prueba otra vez')
        else:
            if fila in range(len(tablero) - tamaño + 1):
                entrada_fila = True
            else:
                print('El barco se sale de los límites del tablero. Prueba otra vez')
    return fila


def solicita_columna(tablero, direccion, tamaño):
    '''
        Solicita al usuario que introduzca una columna y asegura que esté dentro del tablero y que el barco quepa en esa posición
    '''
    entrada_col = False                                                            
    while not entrada_col:
        entrada_num = False
        while not entrada_num:
            columna = input('Introduce la columna en la que quieres colocar el barco: ')
            columna, entrada_num = entrada_numero(columna, entrada_num)
        if direccion.upper() == 'H':
            if columna in range(len(tablero) - tamaño + 1):
                entrada_col = True
            else:
                print('El barco se sale de los límites del tablero. Prueba otra vez')
        else:
            if columna in range(len(tablero)):
                entrada_col = True
            else:
                print('El barco se sale de los límites del tablero. Prueba otra vez')
    return columna
                    

def entrada_numero(num_text, entrada_correcta):
    '''
    Asegura que se introduce un número
    '''
    num = None
    try:
        num = int(num_text)
        entrada_correcta = True
    except Exception as e:
        print('Entrada incorrecta. El valor debe ser un número. Prueba otra vez')
        entrada_correcta = False
    return num, entrada_correcta


def disparo_jugador(tablero, disparos, puntos):
    '''
        Realiza el diparo en la posición que el jugador indique, y actualiza los tableros y marcadores
    '''
    cambio_turno = False
    while not cambio_turno:
        pprint.pprint(disparos)

        x_valida = False                                                      # Solicita coordenadas del disparo y asegura que sean números. Si no, vuelve a solicitarlas
        while not x_valida:
            x_text = input('Introduce la fila del disparo: ')
            x, x_valida = entrada_numero(x_text,x_valida)
        y_valida = False
        while not y_valida:
            y_text = input('Introduce la columna del disparo: ')
            y, y_valida = entrada_numero(y_text, y_valida)

        if x not in range(len(tablero)) or y not in range(len(tablero)):      # Comprueba si el disparo está dentro del tablero. Si está fuera, pierdes el turno
            print('Disparo fuera del tablero. Pierdes el turno')
            cambio_turno = True
        elif disparos[x][y] in ['X', 'O']:                                    # Comprueba si has disparado en un sitio repetido. Si es así, se repite tu turno
            print('Ya has disparado ahí. Prueba otra vez')
        elif tablero[x][y] == '_':                                            # Comprueba si el disparo ha dado en el agua
            disparos[x][y] = 'O'
            print('Disparo fallado')
            cambio_turno = True
        elif tablero[x][y] == 'B':                                            # Comprueba si el disparo ha dado en un barco. Si es true, repite turno
            disparos[x][y] = 'X'
            print('¡Buen disparo! Has acertado en un barco')
            puntos = puntos + 1
            cambio_turno = False
            if puntos == 20:                                                  # Si el jugador lleva 20 aciertos, ya no se repite su turno porque se acaba el juego
                cambio_turno = True
    return puntos


def disparo_maquina(tablero, puntos):
    '''
        Realiza el diparo en la posición que la máquina elija aleatoriamente, y actualiza los tableros y marcadores
    '''
    cambio_turno = False
    while not cambio_turno:
        time.sleep(1)
        x = random.randint(0, len(tablero) - 1)    # Asegura que el disparo de la máquina esté dentro de los límites del tablero
        y = random.randint(0, len(tablero) - 1)
        if tablero[x][y] == '_':
            tablero[x][y] = 'O'
            print('Disparo fallado')
            pprint.pprint(tablero)
            cambio_turno = True
        elif tablero[x][y] == 'B':
            tablero[x][y] = 'X'
            print('¡Buen disparo! La máquina ha acertado en un barco')
            pprint.pprint(tablero)
            puntos = puntos + 1
            cambio_turno = False
            if puntos == 20:
                cambio_turno = True
        else:
            continue     # Si la máquina dispara en un punto en el que ya disparó anteriormente, se repite su turno
    return puntos


def mostrar_marcador(puntos_jugador, puntos_maquina, nombre_jugador):
    ''' 
        Muestra el marcador del juego
    '''
    print(f'Puntos {nombre_jugador}: {puntos_jugador}')
    print(f'Puntos Computer: {puntos_maquina}')

            
