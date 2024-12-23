
# Hundir la flota en Python

El clásico juego de hundir la flota. Se basa en echar una partida contra la máquina. Nada más iniciar la partida, se le presentará al usuario un menu con 2 opciones: "1" - JUGAR y "2" - SALIR del programa. Si el jugador selecciona la opción "1", aparecerán dos tableros. (El del jugador y el del rival, osea la máquina). Tras ello se le pedirá al jugador que inserte la posición que quiera para realizar el ataque. Si el jugador toca un barco del contrincante este atacará de nuevo y si este falla, continuará atacando la máquina.Así hasta que uno de ellos acabe con todos los barcos del tablero. Quien logre destruir todos los barcos, este conseguirá la victoria, y se volverá a presentar el menú por si quieres volver a jugar o salir.

    def hundir_flota(nombre_jugador):
    #Comenzaremos creando tanto el tablero del jugador como el del rival
    tableroJugador = Tablero.crearTablero()
    tableroRival = Tablero.crearTablero()
    
    #A continuación, vamos a colocar los barcos y a guardar sus posiciones, para ello:
    barcosJugador = colocarBarcos(tableroJugador) #Se colocan los barcos de manera aleatoria tanto en los tableros del jugador como el del rival.
    #También hay que tener en cuenta que "colocarBarcos" también devuelve las posiciones de los barcos, que están dentro de una lista.
    barcosRival = colocarBarcos(tableroRival)

    #Aquí es donde comienzan los turnos tanto el del jugador como el de la máquina. Se ha realizado con un bucle WHILE 
    while len(barcosJugador) > 0 and len(barcosRival) > 0: #El juego acabará cuando uno de los dos se quede sin barcos, pero mientras tanto... mientras que los dos tengan los 10...
        visualizarTableroJugador(tableroJugador,nombre_jugador) #Mostramos el tablero del jugador antes del comienzo del ataque.
        print()
        visualizarTableroRival(tableroRival) #Visualizaremos el tablero del rival antes de que se comienze con el ataque
        print()

        #Turno del jugador
        print(f"Turno de {nombre_jugador}") 
        while True:
            fila_ataque = int(input("Introduce la fila del ataque (entre el 0 y el 9): ")) #Comienza el turno del jugador y se le indica tanto la fila como la columna para atacar al rival.
            columna_ataque = int(input("Introduce la columna del ataque (entre el 0 y el 9): "))
            tocado_barco = ataque_jugador(tableroRival,fila_ataque,columna_ataque)  #Llamamos a la función de "ataque_jugador", es donde el jugador realizará el ataque.

            visualizarTableroRival(tableroRival)

            if tocado_barco==True: #Si acierta (tocado_barco = True) comprobamos si el barco ha sido entero destruido o no.
                if barco_destruido(tableroRival,barcosRival):
                    print("¡Has destruido un barco de tu rival!")
                if len(barcosRival) == 0:
                    print(f"El jugador: {nombre_jugador} ¡HA GANADO LA PARTIDA!")
                    mostrar_imagen('imagenes/win.png')
                    print()
                    return
            else: #En caso contrario, si tocado_barco = False, rompemos el bucle.
                break

        #Turno del rival
        print("Turno del rival")
        fila_ataque_rival = random.randint(0,DIMENSIONES_TABLERO-1)
        columna_ataque_rival = random.randint(0,DIMENSIONES_TABLERO-1)
        if ataque_rival(tableroJugador,fila_ataque_rival,columna_ataque_rival):
            if barco_destruido(tableroJugador, barcosJugador):
                print("¡El rival ha destruido uno de tus barcos!")
            if len(barcosJugador) == 0:
                print("El rival ha destruido todos tus barcos. HAS PERDIDO!")
                mostrar_imagen('imagenes/derrota.png')
                print()
                return
    visualizarTableroJugador(tableroJugador, nombre_jugador) #Después de que nuestro rival ataque, volvemos a imprimir el tablero del jugador pero actualizado.


## Screenshots

![App Screenshot](https://images.playground.com/e1e9fe3d00794e3ba48c3e757fd18c38.jpeg)

