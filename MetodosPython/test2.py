__author__ = 'Arnol'

import metodosMCP as met
import os

# Parametros
dir = 'C:/Users/Arnol/Desktop/puntos_poligonos_cmm/'
polygon_fn = 'poligono_test.shp'
point_out = 'puntos.shp'
pixel_size = 10

#met.creaMallaInterior(dir,polygon_fn,point_out,pixel_size)
#os.remove(dir + 'temp.tif')


dir2 = 'C:/TEMP_SPSS/ibis_20130627_txt/'
inputfile = 'desplazamiento_IBIS_dia.txt'
delim = '\t'
id_radar = '1'
tableoutput = '"radar_ibis"."radar_consolidado_dia"'

host = "152.231.85.227"
port = "5433"
dbname = "Modelos_CMM"
user = "postgres"
password = "Admin321"
connstr = 'PG: host=%s port=%s dbname=%s user=%s password=%s' %(host,port,dbname,user,password)


met.cargaRadar(dir2,inputfile,delim,id_radar,connstr,tableoutput)