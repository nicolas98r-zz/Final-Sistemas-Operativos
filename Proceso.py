import matplotlib.pyplot as plt
import numpy as np

class Proceso:
    def __init__(self, nombre, tiempo_ini, tiempo_eje, bloqueo_ini, bloqueo_dur):
        self.nombre = nombre
        self.tiempo_ini = tiempo_ini
        self.tiempo_eje = tiempo_eje
        self.bloqueo_ini = bloqueo_ini
        self.bloqueo_dur = bloqueo_dur
        
class RoundRobin:
    def __init__(self, quantum):
        self.__procesos = []
        self.grafico = Grafica()
        self.quantum = quantum

    def añadir_proceso(self, proceso):
        self.__procesos.append(proceso)

    def calcular(self):
        i = 0
        obj_pro = self.__procesos[i]
        self.grafico.agregar_barras(obj_pro.tiempo_ini, obj_pro.tiempo_eje, obj_pro.nombre, "g")
        self.grafico.mostrar()
        print (obj_pro)
        


class Grafica:
    def __init__(self):
        self.__horizonte = 6
        self.__ticks = 10
        self.__altura_bar = 2
        self.__nombre_pro = ["Windows"]
        self.__numero_pro = len(self.__nombre_pro)

        self.__fig, self.__diagrama = plt.subplots() 

        self.__diagrama.set_xlabel("Tiempo")
        self.__diagrama.set_ylabel("Procesos")
        
        self.__diagrama.set_xlim(0, self.__horizonte)
        self.__diagrama.set_ylim(0, self.__numero_pro*self.__altura_bar)

        self.__diagrama.set_xticks(range(0, self.__horizonte, 1), minor=True)
        self.__diagrama.grid(True, axis='x', which='both')

        self.__diagrama.set_yticks(range(self.__altura_bar, self.__numero_pro*self.__altura_bar, self.__altura_bar), minor=True)
        self.__diagrama.grid(True, axis='y', which='minor')

        self.__diagrama.set_yticks(np.arange(self.__altura_bar/2, self.__altura_bar*self.__numero_pro - self.__altura_bar/2 + self.__altura_bar, self.__altura_bar))
        self.__diagrama.set_yticklabels(self.__nombre_pro)
    
    def mostrar(self):
        # plt.savefig("figura.jpg")  
        plt.show()

    # Función para generar barras:
    def agregar_barras(self, tiempo_ini, duracion, proceso, color):
        obj_pro = self.__nombre_pro.index(proceso)
        # Posición de la barra:
        self.__diagrama.broken_barh([(tiempo_ini, duracion)], (self.__altura_bar*obj_pro, self.__altura_bar), facecolors=(color))

p = Proceso("Windows", 0, 6, 3, 1)
pp = RoundRobin(25)
pp.añadir_proceso(p)
pp.calcular()