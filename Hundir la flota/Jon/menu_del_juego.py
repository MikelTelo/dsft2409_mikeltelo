from opcion_jugar import *

def menu_juego():

    while(True):
        try:
            print("|JUEGO DE HUNDIR LA FLOTA|")
            print("|------------------------|")
            print("|1.Jugar                 |")
            print("|2.Salir                 |")
            opcion = int(input("Introduce una de las opciones: "))
            print()

            if opcion == 1:
                nombre_jugador = input("Introduce el nombre del jugador: ") #Hacemos que el jugador ponga su nombre para que comience a jugar.
                print() 
                hundir_flota(nombre_jugador) #Si el usuario le da a la opción jugar, comenzará a ejecutarse el juego.
            elif opcion == 2:
                print("Saliendo del menu de juego.")
                exit() #Función que se dedica a cerrar el programa.
        except ValueError:
            print("Lo siento, la opción no es válida. Inserta como opciones o 1 o 2.")
            print()