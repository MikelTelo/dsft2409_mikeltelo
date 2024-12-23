from Funciones import *
def MenuHundirFlota():
    while True:
        try:
            print("--------------------------")
            print("Bienvenidos al juego de estrategia \n ----------- Hundir La Flota  --------------")
            print("--------------------------")
            print("1. Iniciar juego")
            print("2. Salir")
            print("--------------------------")
            opcion = int(input("Ingrese la opcion que desee: "))
            if opcion == 1 :
                nombreId = input("Introduce tu nombre \n")
                print(f"Has seleccionado la opcion {opcion}")
                HundirLaFlota(nombreId)# carga el juego
            elif opcion == 2:
                print(f"Has seleccionado la opcion {opcion} Salir")
                print("Has salido  del juego")
                exit()
            else:
                print(f"La opcion {opcion} que has elegido no es valida")
                print("Pofavor introduce otra opcion")
        except ValueError: 
            print("Porfavor Intruduce una opcion correcta")     


