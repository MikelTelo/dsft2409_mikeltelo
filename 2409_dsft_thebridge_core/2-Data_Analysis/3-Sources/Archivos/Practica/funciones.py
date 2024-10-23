from variables import * 

import os
import shutil

def ordenar_archivos(ruta_origen):
    # Definir las extensiones para cada categoría
    extensiones = {
        'Imagenes': ['.jpg', '.jpeg', '.png', '.svg', '.gif'],
        'Documentos': ['.doc', '.docx', '.txt', '.pdf', '.xls', '.ppt', '.xlsx', '.pptx'],
        'Software': ['.exe', '.py','.ipynb'],
        'Otros': ['.md']
    }

    # Crear las carpetas si no existen
    for categoria in extensiones.keys():
        carpeta = os.path.join(ruta_origen, categoria)
        if not os.path.exists(carpeta):
            os.makedirs(carpeta)

    # Recorrer todos los archivos en la carpeta de origen
    for archivo in os.listdir(ruta_origen):
        ruta_archivo = os.path.join(ruta_origen, archivo)
        
        # Ignorar directorios
        if os.path.isfile(ruta_archivo):
            extension = os.path.splitext(archivo)[1].lower()
            
            # Determinar la categoría del archivo
            categoria_destino = 'Otros'
            for categoria, exts in extensiones.items():
                if extension in exts:
                    categoria_destino = categoria
                    break
            
            # Mover el archivo a la carpeta correspondiente
            ruta_destino = os.path.join(ruta_origen, categoria_destino, archivo)
            shutil.move(ruta_archivo, ruta_destino)
            print(f"Movido: {archivo} -> {categoria_destino}")