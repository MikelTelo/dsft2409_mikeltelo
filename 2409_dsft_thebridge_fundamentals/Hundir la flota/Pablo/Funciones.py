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

