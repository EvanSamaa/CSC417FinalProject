import numpy as np

def spring_force(k, pt1, pt2, l_0):
    ##### k = spring constant
    ##### pt1 = location of particle 1
    ##### pt2 = location of particle 2
    ##### l_0 = default length of the spring

    force_magnitude = (np.linalg.norm(pt1 - pt2) - l_0) * k
    arr21 = pt2 - pt1
    arr21 = arr21/np.linalg.norm(arr21)
    arr12 = -arr21
    force12 = arr21 * force_magnitude # the force acting upon pt1 from pt2
    force21 = arr12 * force_magnitude # the force acting upon pt2 from pt1
    return force12, force21