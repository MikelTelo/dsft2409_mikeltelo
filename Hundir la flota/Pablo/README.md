
# Hundir La Flota

Este programa es el juego de Hundir la flota solo que con algunas nuevas mecanicas:

1 Se implementa un menu donde se puede escoger las distintas dificultades, Facil, Normal y Dificil.

2 En funcion de la dificultad elegida las dimensiones del tablero se modifican y la maquina obtiene mas disparos. En la dificultad facil es el juego de Hundir la flota, en normal el tablero es un 15x15 y la maquina dispara 2 veces en su turno y en dificil el tablero es un 20 x20 y la maquina dispara 4 veces por turno y de manera inteligente



    from Tablero import *
    from Barcos import *
    from Variables import *
    #Clase para definir todas las Funciones del HundirLaFlota

    def HundirLaFlota(nombreId):
        while(True):
            try:
            print("Selecciona una dificultad")
            print("1. Easy")
            print("2. Normal")
            print("3. Hard")
            dificultad = int(input("Dificultad: "))
       
            if dificultad == 1:
                jugar(dificultad,nombreId)               
                break
            elif dificultad == 2:
                jugar_normal(dificultad,nombreId)  
                break
                
            elif dificultad == 3:
                jugar_dificil(dificultad,nombreId)
                break
                
            else:
                print("Elige una opcion valida")

        except ValueError:
            print("Introduce una opcion valida")            



