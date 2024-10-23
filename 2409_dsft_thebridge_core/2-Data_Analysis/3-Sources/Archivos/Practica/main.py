if __name__ == "__main__":
    
    import os
    import shutil
    
    # Importar funciones y variables necesarias
    from funciones import *
    from variables import *

    # Definir la ruta de la carpeta a ordenar
    ruta_descargas = os.path.expanduser("C:\\Users\\mikel\\OneDrive\\Descargas\\Actual\\TB-DS-BIO-23.09.24\\REPOSITORIOS\\Mikel\\dsft2409_mikeltelo\\2409_dsft_thebridge_core\\2-Data_Analysis\\3-Sources\\Archivos\\Practica\\carpeta_ejercicio\\Autocarpeta")

    # Llamar a la función para ordenar los archivos
    ordenar_archivos(ruta_descargas)