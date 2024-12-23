import random
import string
import tkinter as tk
import pygame
from Barcos import *

#Inicializar Pygame
pygame.init()

#Cargar los sonidos
disparo_sound = pygame.mixer.Sound("HundirLaFlota\Sonidos\cannonFire.wav")
explosionWater = pygame.mixer.Sound("HundirLaFlota\Sonidos\explosionWater.wav")
VictoryEasy = pygame.mixer.Sound("HundirLaFlota\Sonidos\Victory.wav")
gameOverEasy = pygame.mixer.Sound("HundirLaFlota\Sonidos\GameOver.wav")
VictoryNormal = pygame.mixer.Sound("HundirLaFlota\Sonidos\VictoryNormal.wav")
YouLoseNormal = pygame.mixer.Sound("HundirLaFlota\Sonidos\youlose.wav")
FlawlessVictory = pygame.mixer.Sound("HundirLaFlota\Sonidos\FlawlessVictory.wav")
YouDie =pygame.mixer.Sound("HundirLaFlota\Sonidos\YouDied.wav")

# Clase que representa un tablero de juego
class Tablero:
    def __init__(self, filas, columnas):
         # Inicializar las propiedades del tablero
        self.filas = filas
        self.columnas = columnas
        # Crear una matriz vacía para representar el tablero
        self.casillas = [["." for _ in range(columnas)] for _ in range(filas)]
        # Lista para almacenar las coordenadas atacadas
        self.coordenadas_atacadas = []
    
    # Método para generar tableros de juego según la dificultad
    def generar_tableros(self, dificultad):
        if dificultad == 1:
            tablero_jugador = Tablero(10, 10)
            tablero_rival = Tablero(10, 10)
        elif dificultad == 2:
            tablero_jugador = Tablero(15, 15)
            tablero_rival = Tablero(15, 15)
        elif dificultad == 3:
            tablero_jugador = Tablero(20, 20)
            tablero_rival = Tablero(20, 20)

        return tablero_jugador, tablero_rival
    # Método para cargar barcos en el tablero
    def cargar_barcos(self, barcos, mostrar_barcos=False):
        # Recorrer los barcos y marcar sus posiciones en el tablero
        for barco in barcos:
            for fila, columna in barco.posiciones:
                if mostrar_barcos:
                    self.casillas[fila][columna] = "B"
                else:
                    self.casillas[fila][columna] = "."

    # Método para atacar una posición en el tablero
    def atacar(self, fila, columna, barcos_rival, mostrar_barcos=False):
        # Verificar si la posición está dentro del tablero
        if fila < 0 or fila >= self.filas or columna < 0 or columna >= self.columnas:
            print("Coordenada fuera del tablero")
            return False
        # Verificar si la posición ya ha sido atacada
        if (fila, columna) in self.coordenadas_atacadas:
            print("Coordenada ya atacada")
            return False
        # Agregar la posición a la lista de coordenadas atacadas
        self.coordenadas_atacadas.append((fila, columna))
        # Recorrer los barcos rivales y verificar si alguno ha sido atacado
        for barco in barcos_rival:
            if (fila, columna) in barco.posiciones:
                # Marcar la posición como atacada
                self.casillas[fila][columna] = "X"
                if mostrar_barcos:
                    print("¡Barco hundido!")
                     # Verificar si el barco ha sido completamente hundido
                if all((fila, columna) in self.coordenadas_atacadas for fila, columna in barco.posiciones):
                    print("¡Barco completamente hundido!")
                    # Eliminar el barco de la lista de barcos rivales
                    barcos_rival.remove(barco)
                return True
        self.casillas[fila][columna] = "A"
        print("¡Disparo fallido!")
        explosionWater.play()
        return False
    
    def atacar_normal(self, fila, columna, barcos_rival, mostrar_barcos=False):
        if fila < 0 or fila >= self.filas or columna < 0 or columna >= self.columnas:
            print("Coordenada fuera del tablero")
            return False
        if (fila, columna) in self.coordenadas_atacadas:
            print("Coordenada ya atacada")
            return False
        self.coordenadas_atacadas.append((fila, columna))
        for barco in barcos_rival:
            if (fila, columna) in barco.posiciones:
                self.casillas[fila][columna] = "X"
                if mostrar_barcos:
                    print("¡Barco hundido!")
                if all((fila, columna) in self.coordenadas_atacadas for fila, columna in barco.posiciones):
                    print("¡Barco completamente hundido!")
                    barcos_rival.remove(barco)
                return True
        self.casillas[fila][columna] = "A"
        print("¡Disparo fallido!")
        explosionWater.play()
        return False

    def atacar_dificil(self, fila, columna, barcos_rival, mostrar_barcos=False):
        if fila < 0 or fila >= self.filas or columna < 0 or columna >= self.columnas:
            print("Coordenada fuera del tablero")
            return False
        if (fila, columna) in self.coordenadas_atacadas:
            print("Coordenada ya atacada")
            return False
        self.coordenadas_atacadas.append((fila, columna))
        for barco in barcos_rival:
            if (fila, columna) in barco.posiciones:
                self.casillas[fila][columna] = "X"
                if mostrar_barcos:
                    print("¡Barco hundido!")
                if all((fila, columna) in self.coordenadas_atacadas for fila, columna in barco.posiciones):
                    print("¡Barco completamente hundido!")
                    barcos_rival.remove(barco)
                return True
        self.casillas[fila][columna] = "A"
        print("¡Disparo fallido!")
        explosionWater.play()
        return False

    def imprimir_tablero(self):
        print("  ", end="")
        for i in range(self.columnas):
            print(i, end=" ")
        print()
        for i, fila in enumerate(self.casillas):
            print(i, end=" ")
            for casilla in fila:
                print(casilla, end=" ")
            print()

    def imprimir_tablero_con_letras(self):
        print("  ", end="")
        for i in range(self.columnas):
            print(string.ascii_uppercase[i], end=" ")
        print()
        for i, fila in enumerate(self.casillas):
            print(i, end=" ")
            for casilla in fila:
                print(casilla, end=" ")
            print() 

def mostrar_ventana_ganador_easy():
        ventana = tk.Tk()
        ventana.title("Felicidadees,¡Has ganadoooo!")
        imagen_ganador = tk.PhotoImage(file="HundirLaFlota\Imagenes\Winner.png")
        label_imagen = tk.Label(ventana,image=imagen_ganador)
        label_imagen.pack()
        ventana.mainloop()
        
        
def mostrar_ventana_perdedor_easy():
        ventana = tk.Tk()
        ventana.title("¡Has perdido!")
        imagen_perdedor = tk.PhotoImage(file="HundirLaFlota\Imagenes\Loser.png")
        label_imagen = tk.Label(ventana, image=imagen_perdedor)
        label_imagen.pack()
        ventana.mainloop()
        

def mostrar_ventana_ganador_normal():
        ventana = tk.Tk()
        ventana.title("Enhorabuenaaa ¡Has ganadoooo!")
        imagen_ganador = tk.PhotoImage(file="HundirLaFlota\Imagenes\WinNormal.png")
        label_imagen = tk.Label(ventana,image=imagen_ganador)
        label_imagen.pack()
        ventana.mainloop()

def mostrar_ventana_perdedor_normal():
        ventana = tk.Tk()
        ventana.title("¡Has perdido!")
        imagen_perdedor = tk.PhotoImage(file="HundirLaFlota\Imagenes\Losser.png")
        label_imagen = tk.Label(ventana, image=imagen_perdedor)
        label_imagen.pack()
        ventana.mainloop()  

def mostrar_ventana_ganador_dificil():
        ventana = tk.Tk()
        ventana.title("Enhorabuenaaa ¡Has conseguidoo ganarrr!")
        imagen_ganador = tk.PhotoImage(file="HundirLaFlota\Imagenes\YouWin.jpeg")
        label_imagen = tk.Label(ventana,image=imagen_ganador)
        label_imagen.pack()
        ventana.mainloop()

def mostrar_ventana_perdedor_dificil():
        ventana = tk.Tk()
        ventana.title("¡Has perdido!")
        imagen_perdedor = tk.PhotoImage(file="HundirLaFlota\Imagenes\GameOver.png")
        label_imagen = tk.Label(ventana, image=imagen_perdedor)
        label_imagen.pack()
        ventana.mainloop()

    


def jugar(dificultad,nombreId):
        tablero_jugador, tablero_rival = Tablero(0, 0).generar_tableros(dificultad)
        barcos_jugador = Barco.crear_barcos(5, 2, "horizontal", tablero_jugador.filas, tablero_jugador.columnas)
        barcos_rival = Barco.crear_barcos(1, 2, "horizontal", tablero_rival.filas, tablero_rival.columnas)
        tablero_jugador.cargar_barcos(barcos_jugador)
        tablero_rival.cargar_barcos(barcos_rival, mostrar_barcos=True)
        while True:
            print(f"Tablero del jugador: {nombreId}")
            tablero_jugador.imprimir_tablero_con_letras()
            print("Tablero del rival:")
            tablero_rival.imprimir_tablero_con_letras()
            while True:
                fila = int(input("Ingrese la fila: "))
                columna = int(input("Ingrese la columna: "))
                if tablero_rival.atacar(fila, columna, barcos_rival):
                    print("¡Disparo acertado!")
                    disparo_sound.play()
                    if not barcos_rival:
                        print("¡Has ganado!")
                        pygame.time.delay(2000)
                        VictoryEasy.play()
                        mostrar_ventana_ganador_easy()
                        
                        return
                else:
                    print("¡Disparo fallido!")
                    break
            # Turno de la máquina
            while True:
                fila_maquina = random.randint(0, tablero_jugador.filas - 1)
                columna_maquina = random.randint(0, tablero_jugador.columnas - 1)
                if tablero_jugador.atacar(fila_maquina, columna_maquina, barcos_jugador):
                    print("¡La máquina ha acertado!")
                    if not barcos_jugador:
                        print("¡Has perdido!")
                        pygame.time.delay(2000)
                        mostrar_ventana_perdedor_easy()
                        gameOverEasy.play()
                        return
                else:
                    print("¡La máquina ha fallado!")
                    break

def jugar_normal(dificultad, nombreId):
        tablero_jugador, tablero_rival = Tablero(0, 0).generar_tableros(dificultad)
        barcos_jugador = Barco.crear_barcos(5, 3, "horizontal", tablero_jugador.filas, tablero_jugador.columnas)
        barcos_rival = Barco.crear_barcos(5, 3, "horizontal", tablero_rival.filas, tablero_rival.columnas)
        tablero_jugador.cargar_barcos(barcos_jugador)
        tablero_rival.cargar_barcos(barcos_rival, mostrar_barcos=True)
        while True:
            print(f"Tablero del jugador: {nombreId}")
            tablero_jugador.imprimir_tablero_con_letras()
            print("Tablero del rival:")
            tablero_rival.imprimir_tablero_con_letras()
            while True:
                fila = int(input("Ingrese la fila: "))
                columna = int(input("Ingrese la columna: "))
                if tablero_rival.atacar_normal(fila, columna, barcos_rival):
                    print("¡Disparo acertado!")
                    if not barcos_rival:
                        print("¡Has ganado!")
                        pygame.time.delay(2000)
                        mostrar_ventana_ganador_normal()
                        VictoryNormal.play()
                        return
                else:
                    print("¡Disparo fallido!")

                    break
            # Turno de la máquina
            while True:
                fila_maquina = random.randint(0, tablero_jugador.filas - 1)
                columna_maquina = random.randint(0, tablero_jugador.columnas - 1)
                if tablero_jugador.atacar_normal(fila_maquina, columna_maquina, barcos_jugador):
                    print("¡La máquina ha acertado!")
                else:
                    print("¡La máquina ha fallado!")
                # Segundo ataque
                fila_maquina_segundo = None
                columna_maquina_segundo = None
                if fila_maquina - 1 >= 0:
                    fila_maquina_segundo = fila_maquina - 1
                else:
                    fila_maquina_segundo = fila_maquina + 1
                columna_maquina_segundo = columna_maquina
                if (fila_maquina_segundo, columna_maquina_segundo) not in tablero_jugador.coordenadas_atacadas:
                    if tablero_jugador.atacar_normal(fila_maquina_segundo, columna_maquina_segundo, barcos_jugador):
                        print("¡La máquina ha acertado de nuevo!")
                        if not barcos_jugador:
                            print("¡Has perdido!")
                            pygame.time.delay(2000)
                            YouLoseNormal.play()
                            mostrar_ventana_perdedor_normal()
                            return
                    else:
                        print("¡La máquina ha fallado de nuevo!")
                        break
                else:
                    print("¡La máquina ha repetido coordenadas!")
                    break

                    


def jugar_dificil(dificultad, nombreId):
        tablero_jugador, tablero_rival = Tablero(0, 0).generar_tableros(dificultad)
        barcos_jugador = Barco.crear_barcos(5, 3, "horizontal", tablero_jugador.filas, tablero_jugador.columnas)
        barcos_rival = Barco.crear_barcos(5, 3, "horizontal", tablero_rival.filas, tablero_rival.columnas)
        tablero_jugador.cargar_barcos(barcos_jugador)
        tablero_rival.cargar_barcos(barcos_rival, mostrar_barcos=True)
        while True:
            print(f"Tablero del jugador: {nombreId}")
            tablero_jugador.imprimir_tablero_con_letras()
            print("Tablero del rival:")
            tablero_rival.imprimir_tablero_con_letras()
            while True:
                fila = int(input("Ingrese la fila: "))
                columna = int(input("Ingrese la columna: "))
                if tablero_rival.atacar_dificil(fila, columna, barcos_rival):
                    print("¡Disparo acertado!")
                    if not barcos_rival:
                        print("¡Has ganado!")
                        pygame.time.delay(2000)
                        FlawlessVictory.play()
                        mostrar_ventana_ganador_dificil()
                        
                        return
                else:
                    print("¡Disparo fallido!")
                    break
            # Turno de la máquina
            while True:
                fila_maquina = random.randint(0, tablero_jugador.filas - 1)
                columna_maquina = random.randint(0, tablero_jugador.columnas - 1)
                if (fila_maquina, columna_maquina) not in tablero_jugador.coordenadas_atacadas:
                    break
            if tablero_jugador.atacar_dificil(fila_maquina, columna_maquina, barcos_jugador):
                print("¡La máquina ha acertado!")
                # Disparos inteligentes
                fila_maquina_base = fila_maquina
                columna_maquina_base = columna_maquina
                for _ in range(3):
                    direcciones = [(0, 1), (0, -1), (1, 0), (-1, 0)]
                    random.shuffle(direcciones)
                    for direccion in direcciones:
                        fila_maquina_nueva = fila_maquina_base + direccion[0]
                        columna_maquina_nueva = columna_maquina_base + direccion[1]
                        if (fila_maquina_nueva, columna_maquina_nueva) not in tablero_jugador.coordenadas_atacadas and 0 <= fila_maquina_nueva < tablero_jugador.filas and 0 <= columna_maquina_nueva < tablero_jugador.columnas:
                            if tablero_jugador.atacar_dificil(fila_maquina_nueva, columna_maquina_nueva, barcos_jugador):
                                print("¡La máquina ha acertado de nuevo!")
                                fila_maquina_base = fila_maquina_nueva
                                columna_maquina_base = columna_maquina_nueva
                                break
                            if not barcos_jugador:
                                print("¡Has perdido!")
                                pygame.time.delay(2000)
                                YouDie.play()
                                mostrar_ventana_perdedor_dificil()
                                return
                            else:
                                print("¡La máquina ha fallado de nuevo!")
                                break
            else:
                print("¡La máquina ha fallado!")