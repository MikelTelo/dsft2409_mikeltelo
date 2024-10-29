import os
import shutil

def crear_carpetas(carpeta, categorias):
    os.chdir(carpeta)
    for categoria in categorias:
        os.makedirs(categoria, exist_ok = True)
    os.makedirs("Otros", exist_ok = True)

def mover_archivos(carpeta, categorias):
    os.chdir(carpeta)
    for archivo in os.listdir(carpeta):
        if os.path.isdir(os.path.join(carpeta + f"\\{archivo}")):
            # print(archivo, "Es una carpeta")
            pass
        elif archivo.endswith(categorias['Documentos']):
            # print(archivo, "es un documento")
            try:
                shutil.move(carpeta + f"\\{archivo}", carpeta + "\\Documentos")
            except:
                print(archivo, "ya existe, no lo muevo para no sobreescribir")
        elif archivo.endswith(categorias['Imagenes']):
            # print(archivo, "es una imagen")
            try:
                shutil.move(carpeta + f"\\{archivo}", carpeta + "\\Imagenes")
            except:
                print(archivo, "ya existe, no lo muevo para no sobreescribir")
        elif archivo.endswith(categorias['Software']):
            # print(archivo, "es un software")
            try:
                shutil.move(carpeta + f"\\{archivo}", carpeta + "\\Software")
            except:
                print(archivo, "ya existe, no lo muevo para no sobreescribir")
        else:
            # print(archivo, "es otro archivo")
            try:
                shutil.move(carpeta + f"\\{archivo}", carpeta + "\\Otros")
            except:
                print(archivo, "ya existe, no lo muevo para no sobreescribir")
    
def ordenar_carpeta(carpeta, categorias):
    crear_carpetas(carpeta, categorias)
    mover_archivos(carpeta, categorias)