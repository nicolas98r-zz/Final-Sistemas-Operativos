import matplotlib.pyplot as plt
import numpy as np

class Proceso:
    def __init__(self, nombre, tiempo_ini, tiempo_eje, bloqueo_ini, bloqueo_dur):
        self.nombre = nombre
        self.tiempo_ini = tiempo_ini
        self.tiempo_eje = tiempo_eje
        self.bloqueo_ini = bloqueo_ini
        self.bloqueo_dur = bloqueo_dur
        self.tiempo_res = self.tiempo_eje
        
class RoundRobin:
    def __init__(self, quantum):
        self.__procesos = []
        self.grafico = None
        self.quantum = quantum

    def añadir_proceso(self, proceso):
        self.__procesos.append(proceso)
        
    
    def dibujar_grafico(self):
        lista_com = []
        lista_fin = []
        pos = self.__procesos[0].tiempo_ini
        self.grafico = Grafico(self.__generar_etiquetas())

        #Para 1 parte: Los bloqueos
        for i in range(len(self.__procesos)):
            obj_pro = self.__procesos[i]
            self.grafico.agregar_barras(obj_pro.tiempo_ini, pos, obj_pro.nombre, "lightgray")
            if (self.quantum < obj_pro.tiempo_eje): #Si el quantum NO cubre el proceso
                self.grafico.agregar_barras(pos, self.quantum, obj_pro.nombre, "g")
                if (obj_pro.bloqueo_ini <= self.quantum and obj_pro.bloqueo_ini > 0): #Inicia Bloqueo
                    self.__procesos[i].tiempo_res = obj_pro.tiempo_res - obj_pro.bloqueo_ini
                    pos = pos + obj_pro.bloqueo_ini
                    self.grafico.agregar_barras(pos, obj_pro.bloqueo_dur, obj_pro.nombre, "r")
                    lista_fin.append(pos + obj_pro.bloqueo_dur)
                else: 
                    self.__procesos[i].tiempo_res = obj_pro.tiempo_res - self.quantum
                    pos = self.quantum + pos
                    lista_fin.append(pos)
                lista_com.append(obj_pro)
            else:   #Si el quantum cubre el proceso
                self.grafico.agregar_barras(pos, obj_pro.tiempo_eje, obj_pro.nombre, "g") 
                if (obj_pro.bloqueo_ini <= obj_pro.tiempo_eje and obj_pro.bloqueo_ini > 0): #Inicia Bloqueo
                    pos = pos + obj_pro.bloqueo_ini
                    self.grafico.agregar_barras(pos, obj_pro.bloqueo_dur, obj_pro.nombre, "r")
                else: 
                    pos = obj_pro.tiempo_eje + pos
        
        #Para 2 parte: Algoritmo
        i = 0
        
        while lista_com:
            obj_pro = lista_com[0] 
            self.grafico.agregar_barras(lista_fin[0], pos - lista_fin[0], obj_pro.nombre, "lightgray")
            if (obj_pro.tiempo_res <= self.quantum): #Completo la ejecucion
                self.grafico.agregar_barras(pos, obj_pro.tiempo_res, obj_pro.nombre, "g")
                pos = pos + obj_pro.tiempo_res
                lista_com[0].tiempo_res = 0
                lista_com.pop(0)
                lista_fin.pop(0)
                
            else: #No completo la ejecucion
                self.grafico.agregar_barras(pos, self.quantum, obj_pro.nombre, "g")
                pos = pos + self.quantum
                lista_com[0].tiempo_res = lista_com[0].tiempo_res - self.quantum
                lista_com.append(lista_com[0])
                lista_com.pop(0)
                lista_fin.append(pos)
                lista_fin.pop(0)

        self.grafico.ajustar_limite_hor(pos)
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
        self.__ticks = 10
        self.__altura_bar = 2
        self.__nombre_pro = nombre_pro
        self.__numero_pro = len(self.__nombre_pro)

        self.__fig, self.__diagrama = plt.subplots() 

        self.__diagrama.set_xlabel("Tiempo")
        self.__diagrama.set_ylabel("Procesos")
        
        self.__diagrama.set_ylim(0, self.__numero_pro*self.__altura_bar)

        self.__diagrama.set_yticks(range(self.__altura_bar, self.__numero_pro*self.__altura_bar, self.__altura_bar), minor=True)
        self.__diagrama.grid(True, axis='y', which='minor')

        self.__diagrama.set_yticks(np.arange(self.__altura_bar/2, self.__altura_bar*self.__numero_pro - self.__altura_bar/2 + self.__altura_bar, self.__altura_bar))
        self.__diagrama.set_yticklabels(self.__nombre_pro)
    
    def mostrar(self):
        plt.savefig("graficoProcesos.jpg")  

    # Función para generar barras:
    def agregar_barras(self, tiempo_ini, duracion, proceso, color):
        obj_pro = self.__nombre_pro.index(proceso)
        # Posición de la barra:
        self.__diagrama.broken_barh([(tiempo_ini, duracion)], (self.__altura_bar*obj_pro, self.__altura_bar), facecolors=(color))

    def ajustar_limite_hor(self, horizonte):
        self.__diagrama.set_xticks(range(0, horizonte + 1, 1), minor=True)
        self.__diagrama.grid(True, axis='x', which='both')

p = RoundRobin(5)
l1 = Proceso("A", 0, 9, 1, 5)
l2 = Proceso("B", 1, 7, 3, 3)
l3 = Proceso("C", 1, 3, 0, 0)
l4 = Proceso("D", 2, 13, 6, 2)
l5 = Proceso("E", 3, 3, 4, 1)
l6 = Proceso("F", 4, 7, 3, 2)
p.añadir_proceso(l1)
p.añadir_proceso(l2)
p.añadir_proceso(l3)
p.añadir_proceso(l4)
p.añadir_proceso(l5)
p.añadir_proceso(l6)
p.dibujar_grafico() 

 