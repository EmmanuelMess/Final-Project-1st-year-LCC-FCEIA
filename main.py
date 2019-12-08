import subprocess
import time

from priorityqueue import *


def leerEntrada():
    FORMATO = {'0': 0, '1': 1, 'I': 2, 'X': 3} #Mover esto a una funcion duplica el tiempo total de leerEntrada()

    inicio, final = (0, 0), (0, 0)

    with open("./salida_intermedia.txt", "r") as entrada:
        mapa = [[FORMATO[char] for char in line[:-1]] for line in entrada]

    dimension = len(mapa)

    for (y, linea) in enumerate(mapa):
        for (x, lugar) in enumerate(linea):# Optimizar este codigo no generaria ganancias tangibles en investigacion empirica
            if lugar == 2:
                inicio = (y, x)
            elif lugar == 3:
                final = (y, x)

    return mapa, dimension, inicio, final


"""
Se puede pasar por el casillero dado por el punto?
"""
def chequear(mapa, dimension, punto):
    (y, x) = punto
    return not (x < 0 or dimension <= x or y < 0 or dimension <= y or mapa[y][x] == 1) #El or es para que cortocircuitee


"""
No es exacta, es una estimacion tipo vuelo de pajaro
"""
def distanciaHeuristica(final, posicion):
    return (final[0] - posicion[0])**2 + (final[1] - posicion[1])**2


"""
Devuelve la posicion de un item en un array unidimecional, 
a partir de sus coordenadas bidimencionales.
Permite 'unidimensionalizar' un array/lista bidimensional
"""
def indice(i, j, ancho):
    return i*ancho + j


"""
Algoritmo A* con optimizaciones:
 Usa diccionarios en vez de listas (para evitar una enormidad de listas creadas sin usarse o listas enormes).
 Usa una priority queue autodesbalanceante.

Problemas conocidos:
 Si no hay camino a la salida suele tomar una enormidad de tiempo en enterarse,
  una solucion posible es recorrer una cantidad minima de casilleros desde la salida primero, 
  luego ir desde el inicio.
"""
def Aestrella(mapa, dimension, inicio, final):
    nodosPuntaje = {}
    nodosAnteriores = {}
    nodosAProcesar = crearPriorityQueue()

    pushPriorityQueue(nodosAProcesar, 0, inicio)
    nodosPuntaje[0] = 0

    while not esVacio(nodosAProcesar):
        (nodoY, nodoX) = popPriorityQueue(nodosAProcesar)

        if final == (nodoY, nodoX):
            return nodosAnteriores

        def procesarNodo(nuevoNodo):
            (nuevoNodoY, nuevoNodoX) = nuevoNodo

            if chequear(mapa, dimension, nuevoNodo) \
                    and (indice(nuevoNodoY, nuevoNodoX, dimension) not in nodosPuntaje
                         or distanciaHeuristica(final, nuevoNodo) + nodosPuntaje[indice(nodoY, nodoX, dimension)] < nodosPuntaje[indice(nuevoNodoY, nuevoNodoX, dimension)]):
                pushPriorityQueue(nodosAProcesar, distanciaHeuristica(final, nuevoNodo) + nodosPuntaje[indice(nodoY, nodoX, dimension)], nuevoNodo)
                nodosPuntaje[indice(nuevoNodoY, nuevoNodoX, dimension)] = 1 + nodosPuntaje[indice(nodoY, nodoX, dimension)]
                nodosAnteriores[indice(nuevoNodoY, nuevoNodoX, dimension)] = (nodoY, nodoX)

        procesarNodo((nodoY+1, nodoX))
        procesarNodo((nodoY-1, nodoX))
        procesarNodo((nodoY, nodoX+1))
        procesarNodo((nodoY, nodoX-1))

    return {}


if __name__ == '__main__':
    DEBUG = False

    resultado = []
    semilla = 0
    while not resultado:
        semilla = time.time_ns() if not DEBUG else (semilla +1)   # NOTA: time.time_ns() es desde python 3.7

        response = subprocess.run(args=["./c/cmake-build-debug/TrabajoFinal2019", "c/entrada.txt", "-s", str(semilla)])

        if response.returncode != 0:
            print("Error")

        MAPA, DIMENSION, INICIO, FINAL = leerEntrada()

        resultado = Aestrella(MAPA, DIMENSION, INICIO, FINAL)#TODO testear del final al principio

        if not resultado:
            if DEBUG:
                [print(line) for line in MAPA]
                print("")

    camino = [FINAL]
    (actualY, actualX) = FINAL

    while (actualY, actualX) != INICIO:
        camino.insert(0, resultado[indice(actualY, actualX, DIMENSION)])
        actualY, actualX = resultado[indice(actualY, actualX, DIMENSION)]

    if DEBUG:
        for (y, x) in camino[1:-1]:
            MAPA[y][x] = 'P'

        [print(line) for line in MAPA]#TODO salida como (i,j)

    with open("salida.txt", "w") as archivoSalida:
        camino = [(x+1, y+1) for (y, x) in camino]
        print(camino, file=archivoSalida)