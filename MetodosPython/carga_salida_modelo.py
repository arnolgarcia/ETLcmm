__author__ = 'Arnol'

import datetime as dt
import os


def formatoSalidaVectorMovIBIS(inputfile,outputfile,delim,idradar,escritura):
    # Definir campos de salida
    field1 = "id_radar"
    field2 = "id_poligono"
    field3 = "fecha"
    field4 = "id_parametro"
    field5 = "x"
    field6 = "y"
    field7 = "vector_mov"
    field8 = "vector_vel"
    newline = "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n"%(field1,field2,field3,field4,field5,field6,field7,field8)
    try:
        file = open(inputfile)
        print 'Archivo leido exitosamente...'
    except Exception,e:
        print '[ ERROR ]: Error al leer el archivo: '+str(e)
        return
        #sys.exit(1)
    # Crear archivo de salida
    if os.path.isfile(outputfile) and escritura == 'a':
        newline = ""
    output = open(outputfile, escritura)
    output.write(newline)
    line = file.readline()
    line = file.readline()
    datos = []
    field1 = idradar
    field2 = 688
    field4 = 1
    field8 = 0
    while(line != ""):
        Line = line.split(delim)

        fechahora = dt.datetime.strptime(Line[0],"'%Y-%m-%d %H:%M:%S'")
        field3 = fechahora.date()
        field5 = float(Line[1])
        field6 = float(Line[2])
        field7 = float(Line[3])

        newline = "%s\t%s\t'%s'\t%s\t%s\t%s\t%s\t%s\n"%(field1,field2,field3,field4,field5,field6,field7,field8)
        output.write(newline)
        line = file.readline()
#   Fin de la funcion