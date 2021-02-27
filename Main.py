from Proceso import *

print("Nuevo proceso:")

while True:
    nombre = input("Ingrese el nombre del proceso ")
    tiempo_ini = input("Ingrese el tiempo inicial del proceso")
    tiempo_eje = input("Ingrese el tiempo de ejecución del proceso ")
    bloque_ini = input("Ingrese el tiempo donde se bloquea el proceso ")
    bloqueo_dur = input("Ingrese la duracion del bloqueo del proceso ")
    proceso = Proceso(nombre, tiempo_ini, tiempo_eje, bloque_ini, bloqueo_dur)

    salida = input("Añadir otro proceso? Escriba S o N ")
    if salida == "N": break
1





