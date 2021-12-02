import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *


def find_nearest_vertex(object_list, cursor_ray_dir, camera_pos):
    min_distance = np.inf

    for i in range(0, len(object_list)):
        V = object_list[i]["q_t"]
        z_mean = np.linalg.norm(V.mean(axis=0) - camera_pos)
        print(cursor_ray_dir)
        cursor_pos_3D = cursor_ray_dir * z_mean
        print(cursor_pos_3D, V[0])
        return cursor_pos_3D, V[0]
        for i in range(0, V.shape[0]):
            pass
    return




