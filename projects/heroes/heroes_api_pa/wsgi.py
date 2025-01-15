import sys
import os

# Ajusta esta ruta al path correcto en tu cuenta de PythonAnywhere
# Por ejemplo: '/home/tuusuario/mysite' o '/home/tuusuario/tu_proyecto'
path = '/home/TU_USERNAME/TU_PROJECT_NAME'
if path not in sys.path:
    sys.path.append(path)

from app import app as application 