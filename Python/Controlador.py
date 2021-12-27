# -*- coding: utf-8 -*-
"""
Created on Wed Sep 30 11:51:27 2020

@author: SANTIAGO
"""

#%% Librerias e Importación de Objetos de la Vista y el Modelo

import sys

from Vista import InterfazGrafica
from Modelo import Procesador
from PyQt5.QtWidgets import QApplication

class Controlador(object):                                                                  # Se crea la clase contenedora de
    def __init__(self, vista, procesador):                                                  # la ventana que enlazara la
        self.__mi_vista = vista                                                             # interfaz y el modelo del sistema
        self.__mi_modelo = procesador 

#%% Canal de comunicación/peticiones que realiza la vista al modelo
        


#%% Generador de la aplicación
        
class Aplicacion(object):                                                                   # Se crea la clase que pone en marcha
    def __init__(self):                                                                     # la aplicacion
        self.__app = QApplication(sys.argv)                                                 
        
        self.__mi_vista = InterfazGrafica()                                                 # Se crean los objetos de la aplicacion  
        self.__mi_modelo = Procesador() 
        
        self.__mi_controlador = Controlador(self.__mi_vista, self.__mi_modelo)              # Al controlador se le asignan los objetos 
                                                                                            # vista y modelo, y de forma análoga, a los 
        self.__mi_vista.asignarControlador(self.__mi_controlador)                           # objetos se les asigna el controlador  
        self.__mi_modelo.asignarControlador(self.__mi_controlador)                          # para que esten entrelazados
        
    def main(self):
        self.__mi_vista.show();
        sys.exit(self.__app.exec_()) 
   
     
#%%
aplicacion = Aplicacion() 
aplicacion.main() 






