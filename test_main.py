from main import *


def test_distanciaHeuristica_basico():
    assert 0 == distanciaHeuristica((0, 0), (0, 0))
    assert 1 == distanciaHeuristica((0, 0), (1, 0))