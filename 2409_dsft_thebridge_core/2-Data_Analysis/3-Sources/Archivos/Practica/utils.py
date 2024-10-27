import os
import shutil
    
class Fichero:

    def __init__(self, categoria, extensions, ruta):
        self.categoria = categoria
        self.extensions = extensions
        self.ruta = ruta
        self.select_dir()
        self.create_categories()
        self.move_files()

    def select_dir(self):
        os.chdir(self.ruta)

    def create_categories(self):
        os.makedirs(self.categoria, exist_ok=True)

    def move_files(self):
        for archivo in os.listdir():
            if os.path.isdir(archivo):
                print(archivo, "Es una carpeta")
            elif archivo.endswith(self.extensions) or self.extensions==():
                try:
                    shutil.move(archivo, self.categoria)
                except Exception as e:
                    print(e)