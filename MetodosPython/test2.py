__author__ = 'Arnol'

import metodosMCP as met
import os

# Parametros
dir = 'C:/Users/Arnol/Desktop/puntos_poligonos_cmm/'
polygon_fn = 'poligono_test.shp'
point_out = 'puntos.shp'
pixel_size = 10

met.creaMallaInterior(dir,polygon_fn,point_out,pixel_size)
#os.remove(dir + 'temp.tif')