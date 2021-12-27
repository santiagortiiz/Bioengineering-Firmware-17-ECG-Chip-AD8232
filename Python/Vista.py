# -*- coding: utf-8 -*-
"""
Created on Wed Sep 30 11:51:28 2020

@author: SANTIAGO
"""
#%% Librerias para el diseño de la interfaz de Usuario

from PyQt5.QtWidgets import QMainWindow, QVBoxLayout                                        # Librerias necesarias para crear ventanas
from PyQt5.uic import loadUi                                                                # Libreria para cargar diseños en QtDesigner

import serial
from pyqtgraph.Qt import QtCore

from matplotlib.figure import Figure;
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

#%%

class FiguraCanvas_1(FigureCanvas):                                                           # Clase Figura creada para graficar 
    def __init__(self, parent= None, ancho = 741, alto = 600, dpi = 100):                   # la densidad espectral de potencia de
        self.Figura_1 = Figure(figsize = (ancho, alto), dpi = dpi)                               # 3 dimensiones (t,f,PSD)
        self.ECG = self.Figura_1.add_subplot(111)
        FigureCanvas.__init__(self, self.Figura_1)

    def graficar_ECG(self,dato):
        
        self.ECG.clear();
        self.ECG.set_ylim(0,5000)
        line, = self.ECG.plot(dato)
        line.set_ydata(dato)
         
        self.ECG.figure.canvas.draw()
        self.ECG.figure.canvas.flush_events()

#%%

class InterfazGrafica(QMainWindow):
    def __init__(self, ppal = None):
        super(InterfazGrafica, self).__init__()                                              # Carga la venta de QtDesigner
        loadUi('InterfazGrafica.ui', self)  
        
        self.estructura()                                                                   # Llama la estructura de la ventana
                
    def asignarControlador(self, controlador):                                              # Se asigna el controlador a la ventana de inicio
        self.__controlador = controlador   
        
    def estructura(self):                                                                   # Se conectan los botones de la ventana con sus
                                                                                            # respectivas funciones
        self.Psoc = serial.Serial("COM3", 9600) # Objeto de la clase PySerial
        
        layout_1 = QVBoxLayout()
        self.espacio_grafico_1.setLayout(layout_1)                                          # Se inserta un QVBox en el espacio_grafico_1,
        self.figura_1 = FiguraCanvas_1(self.espacio_grafico_1)                              # se Instancia el objeto FiguraCanvas en figura_1
        layout_1.addWidget(self.figura_1)                                                   # y se añade al espacio_grafico_1 que esta en layout_1

#%%
    def start(self):
        #self.figura_1.show()
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.recibir_datos_del_Psoc)
        self.timer.start(5)
    
    def stop(self):
        self.campoGrafico.hide()
        self.timer.stop()
        self.Psoc.close()
        
    def recibir_datos_del_Psoc(self):
        dato = self.Psoc.read()
        print(dato)
        #self.figura_1.graficar_ECG(dato)
        
    def enviar_dato_al_Psoc(self):
        self.Psoc.write(b'1')
        self.start()