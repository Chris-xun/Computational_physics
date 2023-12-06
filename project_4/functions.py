import numpy as np
import matplotlib.pyplot as plt


def k(point1, point2):
    k = 2/(1/point1 + 1/point2)
    return k


# rate of heat transfer on the boundries
def phi(T, h):
    return h*T