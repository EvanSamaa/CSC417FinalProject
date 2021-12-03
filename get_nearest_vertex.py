import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *


def find_nearest_vertex(object_list, cursor_ray_dir, camera_pos):
    min_distance = np.inf
    min_object = -1
    cursor_pose_3D_final = None
    closest_vertex = None
    for i in range(0, len(object_list)):
        V = object_list[i]["q_t"]
        z_vertices = np.linalg.norm(V - np.expand_dims(camera_pos, axis=0), axis=1, keepdims=True)
        z_vertices = np.tile(z_vertices, [1, 3])
        cursor_pos_3D = np.expand_dims(cursor_ray_dir, axis=0) * z_vertices + np.expand_dims(camera_pos, axis=0)
        distance = np.square(V - cursor_pos_3D).sum(axis=1)
        new_min = min(distance.min(), min_distance)
        if new_min == distance.min():
            min_object = i
            index = np.argmin(distance)
            cursor_pose_3D_final = cursor_pos_3D[index]
            closest_vertex = index
        min_distance = new_min


    return cursor_pose_3D_final, [min_object, closest_vertex]




