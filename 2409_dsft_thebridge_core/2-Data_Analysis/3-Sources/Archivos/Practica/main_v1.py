import utils as u
import variables as v
import os

for categoria in v.categorias:
    u.Fichero(categoria, v.categorias[categoria], v.carpeta)