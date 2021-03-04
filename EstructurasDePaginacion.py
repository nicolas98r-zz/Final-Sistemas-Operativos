import matplotlib.pyplot as graficador

"""
ESTRUCTURAS
"""



class Proceso:
	def __init__(self, nombre, ocupacion=1):
		self.nombre=nombre
		self.ocupacion=ocupacion

	def getOcupacion(self):
		return self.ocupacion

	def getNombre(self):
		return self.nombre

class Pagina:
	def __init__(self, nombre, ocupacion, proceso):
		self.nombre=nombre
		self.ocupacion=ocupacion
		self.proceso=proceso

	def getNombre(self):
		return self.nombre
	def getOcupacion(self):
		return self.ocupacion
	def getProceso(self):
		return self.proceso

class Marco:
	def __init__(self, nombre, pagina):
		self.nombre=nombre
		self.pagina=pagina

	def setPagina(self,pagina):
		self.pagina=pagina

	def getPagina(self):
		return self.pagina

	def getNombre(self):
		return self.nombre

#Administrador de memoria

class Memoria:
	def __init__(self, tamMemoria, tamMarcos):
		self.marcos=[]
		for i in range(2**(tamMemoria-tamMarcos)):
			self.marcos.append(Marco(i,None))

	def getMarcos(self):
		return self.marcos

	def setMarco(self,direccion,pagina):
		self.marcos[direccion].setPagina(pagina)

	def getMarco(self,direccion):
		return self.marcos[direccion]

	def getMarcosOcupados(self):
		ocupacion=0
		for marco in self.marcos:
			if marco.getPagina()!=None:
				ocupacion+=1
		return ocupacion

class CeldaDeTabla:
	def __init__(self, pagina, presente=True, modificada=False, direccion=""):
		self.pagina=pagina
		self.presente=presente
		self.modificada=modificada

"""
FUNCIONES DE LA MEMORIA
"""

def paginarProceso(paginas,cantMaxPaginas,tamPaginas,proceso):
	"""
	Distribuye el proceso en paginas de un tamaño especifico.

	Evalua si el proceso cabe según la cantidad de paginas (memoria virtual)
	posteriormente lo divide en paginas de un tamaño especifico con escepción de la ultima donde puede haber fragmentación interna
	Para la creación de paginas, toma cada pagina y la va rellenando con:
		-Nombre del proceso - numero diferenciador
		-Tamaño que ocupará el proceso en la página
		-Proceso mismo para ser identificado
	Retorna un arreglo que contiene todas las paginas creadas
	"""
	listaPaginas=[]																							#Lista que contendrá las paginas del proceso
	if (len(paginas)<=cantMaxPaginas ) and ( proceso.getOcupacion() <= ((int(cantMaxPaginas)-int(len(paginas)))*int(tamPaginas))): 	#Si la cantidad de paginas existente es menor a la maxima y el espacio ocupado por un proceso no llena la memoria
		tamRestanteProceso=proceso.getOcupacion()

		#Calculo de paginas a usar
		paginasUsar=0
		if (proceso.getOcupacion()%tamPaginas)==0:
			paginasUsar=int(proceso.getOcupacion()/tamPaginas)
		else:
			paginasUsar=int(proceso.getOcupacion()/tamPaginas)+1
		#Creación de las paginas
		for i in range(paginasUsar):
			if(tamPaginas<tamRestanteProceso):
				listaPaginas.append(Pagina(proceso.getNombre()+"-"+str(i), tamPaginas, proceso))
				tamRestanteProceso=tamRestanteProceso-tamPaginas
			else:
				listaPaginas.append(Pagina(proceso.getNombre()+"-"+str(i), tamRestanteProceso, proceso))

	return listaPaginas

def asignarPaginasAMemoria(memoria, listaPaginas, paginas):
	"""
	Asigna las paginas a memoria (dado un criterio de reemplazo).
		-recorre la lista de paginas creadas de un proceso y las va almacenando en marcos de la memoria RAM
	"""
	i=0 #Contador de posición
	if (len(paginas)<=len(memoria.getMarcos())-memoria.getMarcosOcupados()):
		for pag in paginas:
			while (i<len(memoria.getMarcos())):
				if memoria.getMarco(i).getPagina()==None:
					memoria.setMarco(i,pag)
					break
				i+=1
	return memoria

def procesoExiste(listaProcesos, nombreProceso):
	"""
	Verifica si el nombre de un proceso ya existe para no volver a usarlo y evitar errores de repetición.
	"""
	for proceso in listaProcesos:
		if proceso.getNombre()==nombreProceso:
			return True
	return False



"""
ELEMENTOS DE MENÚ
"""

def verListaDeProcesos(listaProcesos):
	"""
	Genera la visibilidad por consola de los procesos existentes.
	"""
	print("LISTA DE PROCESOS:")
	for i in range(len(listaProcesos)):
		print("Proceso " + str(i) + ": " + listaProcesos[i].getNombre() + " ("+ str(listaProcesos[i].getOcupacion()) +") ")

def verListaDePaginas(listaPaginas):
	"""
	Genera la visibilidad por consola de las paginas existentes.
	"""
	print("LISTA DE PAGINAS:")
	for i in range(len(listaPaginas)):
		print("Pagina " + str(i) + ": " + listaPaginas[i].getNombre() + " ("+ str(listaPaginas[i].getOcupacion()) +"), que cubre el proceso " + listaPaginas[i].getProceso().getNombre())

def verListaDeMarcos(ram):
	"""
	Genera la visibilidad por consola de los marcos de la RAM y su contenido.
	"""
	print("LISTA DE MARCOS:")
	for marco in ram.getMarcos():
		if marco.getPagina()!=None:
			print("Nombre: "+marco.getPagina().getNombre()+", Tamaño: "+str(marco.getPagina().getOcupacion()))
		else:
			print("Espacio libre")

def crearProceso(ram, listaProcesos, listaPaginas, cantMaxPaginas, tamPaginas, nombre="Nombre", tamano=1):
	"""
	Creación y registro de un proceso.

		-Decide primero si el proceso existe o si hay suficiente espacio en la memoria virtual para almacenarlo
		-Crea el proceso y lo registra en la lista de procesos
		-Lo pagina, añade estas páginas a la memoria virtual (listaPaginas)
		-Asigna las paginas a marcos en la memoria RAM

	"""
	if procesoExiste(listaProcesos, nombre) or (tamano>(tamPaginas*(cantMaxPaginas-len(listaPaginas)))):
		return None
	else:
		procesoNuevo=Proceso(nombre,tamano)
		listaProcesos.append(procesoNuevo)
		nuevasPaginas=paginarProceso(listaPaginas,cantMaxPaginas,tamPaginas,procesoNuevo)
		listaPaginas = listaPaginas + nuevasPaginas
		ram=asignarPaginasAMemoria(ram,listaPaginas,nuevasPaginas)
		return [ram, listaProcesos, listaPaginas]


def eliminarProceso(ram, listaProcesos, listaPaginas, nombreProceso):
	"""
	Eliminación de un proceso.
		-Elimina el proceso del registro de procesos
		-Recorre la lista de paginas y elimina el proceso de esta
		-Recorre la memoria ram y elimina la lista de procesos
	"""

	for i in range(len(listaProcesos)):
		if(listaProcesos[i].getNombre()==nombreProceso):
			listaProcesos.pop(i)
			break

	for i in range(len(listaPaginas)):											#Recorre la lista de manera inversa
		if(listaPaginas[len(listaPaginas)-1-i].getProceso().getNombre()==nombreProceso):
			listaPaginas.pop(len(listaPaginas)-1-i)

	for i in range(len(ram.getMarcos())):
		if(ram.getMarcos()[len(ram.getMarcos())-1-i].getPagina()!=None):
			if(ram.getMarcos()[len(ram.getMarcos())-1-i].getPagina().getNombre()==nombreProceso):
				ram.getMarcos()[len(ram.getMarcos())-1-i].setPagina(None)
	return [ram, listaProcesos, listaPaginas]


def graficar(ram,listaProcesos,bitsMemoria):
	"""
	Graficación de la memoria RAM.
		-Genera una matriz
		-Asigna colores a cada proceso
		-Designa colores a la matriz
		-Uso de la función de graficación
	"""
	matriz=[]
	tamMatrizX=2**int(bitsMemoria/2)
	tamMatrizY=int(len(ram.getMarcos())/tamMatrizX)
	print(tamMatrizX)
	print(tamMatrizY)
	listaColores=[]
	numeracion=1
	#AsignarColor
	for i in range(len(ram.getMarcos())):
		if ram.getMarcos()[i].getPagina()==None:
			listaColores.append(0)
		else:
			if(i!=0 and ram.getMarcos()[i-1].getPagina().getProceso().getNombre()!=ram.getMarcos()[i].getPagina().getProceso().getNombre()):
				numeracion+=1
			listaColores.append(numeracion)
	#AsignarMatriz
	contador=0
	for i in range(tamMatrizX):
		fila=[]
		for j in range(tamMatrizY):
			fila.append(listaColores[contador])
			contador+=1
		matriz.append(fila)
	#Graficar
	graficador.figure(figsize=(tamMatrizX,tamMatrizY))
	graficador.imshow(matriz)
	graficador.show()


"""
MENÚ
"""

#Fase inicial
salir=False
while(True):
	print("VALORES DE ENTRADA")
	tamMemoria=int(input("Introduzca el tamaño de la memoria física (cantidad de bits) \n"))	#Tamaño de la memoria física
	tamVirtual=int(input("Introduzca el tamaño de la memoria virtual (cantidad de bits) \n"))	#Tamaño de la memoria física
	tamMarcos=int(input("Introduzca el tamaño de los marcos (cantidad de bits) \n"))			#Tamaño de los marcos
	if (tamMarcos<=tamMemoria and tamMemoria<=tamVirtual):
		break

#Creación de la memoria
ram=Memoria(int(tamMemoria),int(tamMarcos))
listaProcesos=[]
listaPaginas=[]
cantMaxPaginas=2**(int(tamVirtual)-int(tamMarcos))
tamMarcos=2**(tamMarcos)

#Simulación
while(not salir):
	print("\n1. Ver lista de procesos")
	print("2. Ver lista de páginas")
	print("3. Ver lista de marcos en memoria física")
	print("4. Crear proceso")
	print("5. Eliminar proceso")
	print("6. Visualizar memoria ram")
	print("7. Terminar simulación")
	entrada=input("Elija una opción válida: \n")


	if entrada==str(1):
		verListaDeProcesos(listaProcesos)

	elif entrada==str(2):
		verListaDePaginas(listaPaginas)

	elif entrada==str(3):
		verListaDeMarcos(ram)

	elif entrada==str(4):
		nombreProceso=input("Introduzca el nombre del proceso \n")
		tamProceso=input("Introduzca el tamaño del proceso \n")
		tuplaDeCreacion=crearProceso(ram, listaProcesos, listaPaginas, cantMaxPaginas, tamMarcos, nombreProceso, int(tamProceso))
		if tuplaDeCreacion!=None:
			ram=tuplaDeCreacion[0]
			listaProcesos=tuplaDeCreacion[1]
			listaPaginas=tuplaDeCreacion[2]
			print("Proceso creado")
		else:
			print("Fallo en la creación del proceso")

	elif entrada==str(5):
		nombreProceso=input("Introduzca el nombre del proceso \n")
		tuplaDeEliminacion=eliminarProceso(ram ,listaProcesos, listaPaginas ,nombreProceso)
		ram=tuplaDeEliminacion[0]
		listaProcesos=tuplaDeEliminacion[1]
		listaPaginas=tuplaDeEliminacion[2]

	elif entrada==str(6):
		graficar(ram, listaProcesos, tamMemoria)


	elif entrada==str(7):
		salir=False
		print("Simulación terminada")
		break

	else:
		print("Opción no válida")







