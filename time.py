import cProfile
import subprocess

import time

import main

if __name__ == '__main__':
    semilla = time.time_ns()  # NOTA: time.time_ns() es desde python 3.7

    cProfile.run("subprocess.run(args=['./c/cmake-build-debug/TrabajoFinal2019', 'c/entrada.txt', '-s', str(semilla)])")

    cProfile.run("main.leerEntrada()")
    MAPA, DIMENSION, INICIO, FINAL = main.leerEntrada()

    cProfile.run("main.Aestrella(MAPA, DIMENSION, INICIO, FINAL)")