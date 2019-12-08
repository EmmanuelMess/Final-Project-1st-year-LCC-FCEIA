"""
Arbol binario de busqueda autodesbalanceante
Invariantes:
    * las de un arbol binario de busqueda
    * la raiz no tiene nodo izquierdo
"""

def crearPriorityQueue():
    return {"raiz": None}


def _generarNodo(hijoIzq, hijoDer, prioridad, contenido):
    return {"hijoIzq": hijoIzq, "hijoDer": hijoDer, "prioridad": prioridad, "contenido": contenido}


def _rotarDerecha(arbol):
    nuevoPadre = arbol["hijoIzq"]
    arbol["hijoIzq"] = nuevoPadre["hijoDer"]

    nuevoPadre["hijoDer"] = arbol

    return nuevoPadre


def pushPriorityQueue(pq, prioridad, valor):
    if pq["raiz"] is None:
        pq["raiz"] = _generarNodo(None, None, prioridad, valor)
        return

    if prioridad < pq["raiz"]["prioridad"]:
        pq["raiz"] = _generarNodo(None, pq["raiz"], prioridad, valor)
        return

    padre = pq["raiz"]
    posicion = "hijoDer"

    while padre[posicion] is not None:
        padre = padre[posicion]
        if prioridad < padre["prioridad"]:
            posicion = "hijoIzq"
        else:
            posicion = "hijoDer"

    padre[posicion] = _generarNodo(None, None, prioridad, valor)

def popPriorityQueue(pq):
    elem = pq["raiz"]["contenido"]

    pq["raiz"] = pq["raiz"]["hijoDer"]

    if pq["raiz"] is None:
        return elem

    while pq["raiz"]["hijoIzq"] is not None:
        pq["raiz"] = _rotarDerecha(pq["raiz"])

    return elem

def esVacio(pq):
    return pq["raiz"] is None
