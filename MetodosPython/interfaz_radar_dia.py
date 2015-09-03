#__author__ = 'Arnol'
#__fecha__ = '2015-09-03'
#__version__= '1.0'

import os
from osgeo import ogr,osr
from Tkinter import *
from tkFileDialog import *
import metodosMCP as metMCP
import sys
import time
import datetime as dt


#TODO: dejar los parametros de conexion en un archivo config.txt
#TODO: borrar valores iniciales de configuarcion
GlobalValues = {}
GlobalValues['host'] = "152.231.85.227"
GlobalValues['port'] = "5433"
GlobalValues['dbname'] = "Modelos_CMM"
GlobalValues['user'] = "postgres"
GlobalValues['password'] = "Admin321"
GlobalValues['connString'] = 'PG: host=%s port=%s dbname=%s user=%s password=%s' %(GlobalValues['host'],
                                                                                   GlobalValues['port'],
                                                                                   GlobalValues['dbname'],
                                                                                   GlobalValues['user'],
                                                                                   GlobalValues['password'])
GlobalValues['inputfile'] = ""

initial_file = 'C:/TEMP_SPSS/ibis_20130627_txt/desplazamiento_IBIS_dia.txt'
delim = '\t'
tableoutput = '"radar_ibis"."radar_consolidado_dia"'





#------------------------------------------------
#   Funciones
#------------------------------------------------

def paramConexion():
    # Ventana de conexion a BD
    w2 = Toplevel()
    w2.title("HGI GeoAlert: parametros de conexion")

    dbServer = StringVar()
    dbServer.set(GlobalValues['host'])
    Lserver = Label(w2, width=15,text='DB Server').grid(row=1,column=1)
    Eserver = Entry(w2, textvariable=dbServer).grid(row=1,column=2)

    dbPort = StringVar()
    dbPort.set(GlobalValues['port'])
    Lport = Label(w2, width=15,text='Port').grid(row=2,column=1)
    Eport = Entry(w2, textvariable=dbPort).grid(row=2,column=2)

    dbName = StringVar()
    dbName.set(GlobalValues['dbname'])
    Lname = Label(w2, text='DB Name').grid(row=3,column=1)
    Ename = Entry(w2, textvariable=dbName).grid(row=3,column=2)

    dbUser = StringVar()
    dbUser.set(GlobalValues['user'])
    Luser = Label(w2, text='User').grid(row=4,column=1)
    Euser = Entry(w2, textvariable=dbUser).grid(row=4,column=2)

    dbPW = StringVar()
    dbPW.set(GlobalValues['password'])
    Lpass = Label(w2, text='Password').grid(row=5,column=1)
    Epass = Entry(w2, textvariable=dbPW).grid(row=5,column=2)

    testB = Button(w2, width=8, text='Test',command=lambda: testConn(dbServer.get(),
                                                            dbPort.get(),
                                                            dbName.get(),
                                                            dbUser.get(),
                                                            dbPW.get())).grid(row=6,column=2)

    #TODO: revisar si dejar el check o que el usuario siempre tenga que ingresar los parametros
    #save = IntVar()
    #Csave = Checkbutton(w2, text="Guardar parametros", variable=save).grid(row=5,column=3)
    okB = Button(w2, width=8,text='Aceptar',command=lambda: saveConn(dbServer.get(),
                                                                       dbPort.get(),
                                                                       dbName.get(),
                                                                       dbUser.get(),
                                                                       dbPW.get(),
                                                                       w2)).grid(row=6,column=4)
    w2L53 = Label(w2, text=" ").grid(row=6,column=3)
    w2L55 = Label(w2, text=" ").grid(row=6,column=5)
#   Fin de la funcion


def testConn(dbServer,dbPort,dbName,dbUser,dbPW):
    connString = 'PG: host=%s port=%s dbname=%s user=%s password=%s' %(dbServer,dbPort,dbName,dbUser,dbPW)
    testConnString(connString)
#   Fin funcion

def testConnString(connStr,esTest=1):
    ogr.UseExceptions()
    texto =""
    esError = 0
    try:
        conn = ogr.Open(connStr)
        texto = "Conexion exitosa"
        conn.Destroy()
    except Exception:
        texto= "Error de conexion"
        esError = 1
    if esTest==1:
        EdoConexion(texto)
    if esTest==0 and esError==1:
        EdoConexion(texto)
    return esError
#   Fin de la funcion

def EdoConexion(estado):
    ancho = max(20,len(estado)+2)
    w3=Toplevel()
    w3.title("HGI GeoAlert: Mensaje de la aplicacion")
    w3lab1 = Label(w3, text="").grid(row=1,column=1)
    w3lab2 = Label(w3, width=ancho,text=estado).grid(row=2,column=1)
    w3lab3 = Label(w3, text="").grid(row=3,column=1)
    w3bOK = Button(w3, text='Aceptar',command=w3.destroy).grid(row=4,column=1)
    w3lab5 = Label(w3, text="").grid(row=5,column=1)
#   Fin de la funcion

def saveConn(Server,Port,Name,User,PW,Window=None):
    GlobalValues['host'] = Server
    GlobalValues['port'] = Port
    GlobalValues['dbname'] = Name
    GlobalValues['user'] = User
    GlobalValues['password'] = PW
    GlobalValues['connString'] = 'PG: host=%s port=%s dbname=%s user=%s password=%s' %(GlobalValues['host'],
                                                                                   GlobalValues['port'],
                                                                                   GlobalValues['dbname'],
                                                                                   GlobalValues['user'],
                                                                                   GlobalValues['password'])
    if Window!=None:
        Window.destroy()
#   Fin de la funcion

def rutaDir(entry):
    rutadeldirectorio=askopenfilename(initialfile=initial_file)
    entry.set(rutadeldirectorio)
    GlobalValues['inputfile'] = rutadeldirectorio
#   Fin funcion

def cargaArchivo(tableout,id_radar):
    # Revisar validez de los inputs
    if testConnString(GlobalValues['connString'],0)==1:
        return
    if GlobalValues['inputfile']=='':
        EdoConexion('Seleccionar un archivo valido')
        return

    # Crear ventana para el log
    textlog,logwin = LogWindow()
    stdout_old = sys.stdout
    sys.stdout = Std_redirector(textlog)
    time_ini = dt.datetime.now()
    print "Carga de archivos iniciada: " + time_ini.strftime("%d-%m-%Y %H:%M:%S")
    textlog.update()

    # Ejecutar metodo para cargar los datos
    try:
        metMCP.cargaRadar(GlobalValues['inputfile'],delim,id_radar,GlobalValues['connString'],tableout)
        # TODO: eliminar testing antes de empaquetar
        #testing(GlobalValues['inputfile'],delim,id_radar,GlobalValues['connString'],tableout)
        time_fin = dt.datetime.now()
        print "Carga de archivos finalizada: " + time_fin.strftime("%d-%m-%Y %H:%M:%S")
        print "Tiempo de ejecucion: " + str(time_fin-time_ini)
    except Exception,e:
        print "Error de ejecucion:\n" + str(e)
    sys.stdout = stdout_old
    logwin.title("Log: Finalizado")
#   Fin de la funcion

def LogWindow():
    logg = Toplevel()
    #time.sleep(2)
    logg.title("Log: Ejecutandose...")
    S = Scrollbar(logg)
    T = Text(logg, height=20, width=70)
    S.pack(side=RIGHT, fill=Y)
    T.pack(side=LEFT, fill=Y)
    S.config(command=T.yview)
    T.config(yscrollcommand=S.set)
    exitB = Button(logg,width=10,text="Salir",command=salir).pack(side=BOTTOM)
    aceptaB = Button(logg,width=10,text="Aceptar",command=logg.destroy).pack(side=BOTTOM)
    cancelaB = Button(logg,width=10,text="Cancelar",command=logg.destroy).pack(side=BOTTOM)
    return T,logg
#   Fin de la funcion

# TODO: definir forma para cancelar la carga
#def cancelaCarga(self):
#    self.destroy()
#    print "ERROR: Carga de archivos cancelada"

class Std_redirector(object):
    def __init__(self,widget):
        self.widget = widget

    # TODO: Ver si se puede sobreescribir el texto
    def write(self,string,rew=0):
        if rew==0:
            self.widget.insert(END,string)
            self.widget.see(END)
            self.widget.update()
        if rew==1:
            ind = self.widget.index(END)
            self.widget.insert(END,ind)
            self.widget.insert(END,string)
            self.widget.see(END)
            self.widget.update()
# Fin de la clase para redireccionar el 'print'

def salir():
    os._exit(0)
#   Fin de la funcion



#------------------------------------------------
#   Funciones para testing
#------------------------------------------------

def testing(entrada,delimitador,id,connStr,salida):
    print 'inputfile: '+ str(entrada)
    print 'delim: ' + str(delimitador)
    print 'id: ' + str(id)
    print 'connstring: '+ str(connStr)
    print 'tableoutput: '+ str(salida)
#   Fin




#------------------------------------------------
#   Ventana principal
#------------------------------------------------

# Inicializar ventana y titulo
w1 = Tk()
w1.title('HGI GeoAlert: Cargador datos radar Ibis')

# 1ra fila (en blanco
l1 = Label(w1, text="").grid(row=1,column=2)

# 2da fila (boton conexion)
conexB = Button(w1, width=15,
            text='Detalles conexion',
            command=paramConexion).grid(row=2,column=4)

# 3era fila (Ingresar archivo a subir)
l3 = Label(w1, width=10,text='Archivo:').grid(row=3,column=1)
inputfile = StringVar()
e3 = Entry(w1, width=70,textvariable=inputfile).grid(row=3,column=2)
l33 = Label(w1,width=1,text='').grid(row=3,column=3)
seleccB = Button(w1, width=15,text='Seleccionar archivo',command=lambda: rutaDir(inputfile)).grid(row=3,column=4)
l35 = Label(w1,width=1,text='').grid(row=3,column=5)

# 4ta fila (tableoutput)
l4 = Label(w1, width=10,text='Tabla:').grid(row=4,column=1)
table = StringVar()
#TODO: Setear valor de 'inputfile' solo para testing, eliminar despues
table.set('"radar_ibis".radar_test')
e4 = Entry(w1, width=70,textvariable=table).grid(row=4,column=2)

# 5ta fila (id_radar)
l5 = Label(w1, width=10,text='ID radar:').grid(row=5,column=1)
id_rad = StringVar()
#TODO: Setear valor de 'inputfile' solo para testing, eliminar despues
id_rad.set('1')
e5 = Entry(w1, width=70,textvariable=id_rad).grid(row=5,column=2)

# 5ta fila (en blanco)
l5 = Label(w1,width=1,text='').grid(row=6,column=3)

# 7ta fila (botones "carga" y "exit")
cargaB = Button(w1, text='Cargar archivos',command=lambda: cargaArchivo(table.get(),id_rad.get())).grid(row=7,column=2)
exitB = Button(w1, text='Salir', command=salir).grid(row=7,column=4)

# 8ta fila (en blanco)
l8 = Label(w1, text=" ").grid(row=8,column=2)

# Iniciar ventana
w1.mainloop()
