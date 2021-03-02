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
        self.grafico = None
        self.quantum = quantum

    def añadir_proceso(self, proceso):
        self.__procesos.append(proceso)
        
    
    def dibujar_grafico(self):
        lista_com = []
        pos = self.__procesos[0].tiempo_ini
        self.grafico = Grafico(self.__generar_etiquetas())

        #Para 1 parte: Los bloqueos
        for i in range(len(self.__procesos)):
            obj_pro = self.__procesos[i]
            self.grafico.agregar_barras(obj_pro.tiempo_ini, pos, obj_pro.nombre, "lightgray")
            if (self.quantum < obj_pro.tiempo_eje): #Si el quantum NO cubre el proceso
                self.grafico.agregar_barras(pos, self.quantum, obj_pro.nombre, "g")
                if (obj_pro.bloqueo_ini <= self.quantum): #Inicia Bloqueo
                    pos = pos + obj_pro.bloqueo_ini
                    self.grafico.agregar_barras(pos, obj_pro.bloqueo_dur, obj_pro.nombre, "r")
                else: pos = self.quantum + pos
                lista_com.append(obj_pro)
            else:   #Si el quantum cubre el proceso
                self.grafico.agregar_barras(pos, obj_pro.tiempo_eje, obj_pro.nombre, "g") 
                if (obj_pro.bloqueo_ini <= self.quantum): #Inicia Bloqueo
                    pos = pos + obj_pro.bloqueo_ini
                    self.grafico.agregar_barras(pos, obj_pro.bloqueo_dur, obj_pro.nombre, "r")
                    lista_com.append(obj_pro)
                else: pos = obj_pro.tiempo_eje + pos
        
        #Para 2 parte: Algoritmo
        """ while lista_com:
            print("Elemento") """
            
        self.grafico.mostrar()

    #Agrega los nombres de los procesos a las etiquetas de la grafica
    def __generar_etiquetas(self):
        nombre_pro = []
        for i in range(len(self.__procesos)):   
            obj_nom = self.__procesos[i].nombre
            nombre_pro.append(obj_nom)
        return nombre_pro

class Grafico:
    def __init__(self, nombre_pro):
        self.__horizonte = 60
        self.__ticks = 10
        self.__altura_bar = 2
        self.__nombre_pro = nombre_pro
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

p = RoundRobin(3)
l1 = Proceso("Windows", 0, 9, 1, 2)
l2 = Proceso("Power point", 1, 2, 2, 2)
l3 = Proceso("Calculadora", 1, 5, 6, 1)
p.añadir_proceso(l1)
p.añadir_proceso(l2)
p.añadir_proceso(l3)
p.dibujar_grafico()
 