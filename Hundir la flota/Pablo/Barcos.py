import random

class Barco:
    def __init__(self, fila, columna, orientacion, tamano):
        self.fila = fila
        self.columna = columna
        self.orientacion = orientacion
        self.tamano = tamano
        self.posiciones = self.generar_posiciones()

    def generar_posiciones(self):
        posiciones = []
        if self.orientacion == "horizontal":
            for i in range(self.tamano):
                posiciones.append((self.fila, self.columna + i))
        elif self.orientacion == "vertical":
            for i in range(self.tamano):
                posiciones.append((self.fila + i, self.columna))
        return posiciones

    @classmethod
    def crear_barcos(cls, cantidad, tamano, orientacion, filas, columnas):
        barcos = []
        for _ in range(cantidad):
            while True:
                fila = random.randint(0, filas - 1)
                columna = random.randint(0, columnas - 1)
                barco = cls(fila, columna, orientacion, tamano)
                if cls.validar_posiciones(barco.posiciones, filas, columnas):
                    barcos.append(barco)
                    break
        return barcos

    @classmethod
    def validar_posiciones(cls, posiciones, filas, columnas):
        for fila, columna in posiciones:
            if fila < 0 or fila >= filas or columna < 0 or columna >= columnas:
                return False
        return True

barcos_creados = []


    



    



        

        