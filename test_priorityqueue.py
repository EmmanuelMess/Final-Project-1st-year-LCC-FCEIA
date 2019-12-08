from priorityqueue import *


def testPriorityQueue_basico():
    pq = crearPriorityQueue()
    pushPriorityQueue(pq, 0, 'A')
    assert popPriorityQueue(pq) == 'A'


def testPriorityQueue_varios():
    pq = crearPriorityQueue()

    pushPriorityQueue(pq, 0, 'A')
    pushPriorityQueue(pq, 3, 'D')
    pushPriorityQueue(pq, 2, 'C')
    pushPriorityQueue(pq, 1, 'B')

    assert popPriorityQueue(pq) == 'A'
    assert popPriorityQueue(pq) == 'B'
    assert popPriorityQueue(pq) == 'C'
    assert popPriorityQueue(pq) == 'D'


def testPriorityQueue_x():
    pq = crearPriorityQueue()

    for i in reversed(range(0, 90)):
        pushPriorityQueue(pq, i, i)

    for i in range(0, 90):
        assert popPriorityQueue(pq) == i


def testPriorityQueue_esVacio():
    pq = crearPriorityQueue()

    assert esVacio(pq)

    pushPriorityQueue(pq, 0, 'A')

    assert not esVacio(pq)