from OpenGL.GL import *
from OpenGL.GLU import *
import pygame
from pygame.locals import *
import numpy as np
from get_nearest_vertex import *
# the code for display and etc is based on the tutorial from
# https://pythonprogramming.net/opengl-rotating-cube-example-pyopengl-tutorial/

# example object, defined by default position and edges
V = [(1, -1, -1),(1, 1, -1),(-1, 1, -1),(-1, -1, -1),(1, -1, 1),(1, 1, 1),(-1, -1, 1),(-1, 1, 1)]
E = [(0, 1), (0, 3), (0, 4), (2, 1), (2, 3), (2, 7), (6, 3), (6, 4), (6, 7), (5, 1), (5, 4), (5, 7)]
k_drag = 1.0e5
cube = {"V0":np.array(V),
        "E":np.array(E),
        "q_t":np.array(V),
        "q_dot_t":np.zeros(np.array(V).shape),
        "mass_per_particle":1}
def pixel2rayDir(pixel, display, z, aspect_ratio, y_angle, camera_pos):

    display = np.array(display, dtype=np.double)
    screen_height = np.tan(y_angle / 180.0 * np.pi / 2.0) * z * 2.0
    screen_width = screen_height * aspect_ratio
    pixel[0] = (pixel[0] - display[0]/2.0)/display[0] * screen_width
    pixel[1] = (pixel[1] - display[1]/2.0)/display[1] * screen_height
    ray = np.array([pixel[0], -pixel[1], 0]) - camera_pos
    ray = ray / np.linalg.norm(ray)
    return ray

def draw_object(object_dict):
    edges = object_dict["E"]
    vertices = object_dict["q_t"]
    glBegin(GL_LINES)
    for e in range(0, edges.shape[0]):
        edge = edges[e]
        for v in edge:
            glVertex3fv(vertices[v])
    glEnd()
def update(in_obect, dt, force):
    return in_obect

def visualize(object_dict_list, dt):

    ###########################
    ##### cammera params ######
    ###########################
    display = (800, 600)
    z = 10
    aspect_ratio = float(display[0]) / float(display[1])
    y_angle = 45
    camera_pos = np.array([0.0, 0.0, -z])
    ########################################
    ############# MISC setup ###############
    ########################################

    # set up interface for visualization
    pygame.init()
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    # set up perspective and camera position
    gluPerspective(y_angle, aspect_ratio, 0.1, 50.0)
    glTranslatef(camera_pos[0], camera_pos[1], camera_pos[2]) # the camera parameters are (left right, up down, forward backward)

    ########################################
    ###### set up control parameterrs ######
    ########################################
    hold = False # if the mouse is being held
    simulate = True # True = play, False = pause
    p_pressed = False
    drag_start = np.zeros([0, 0, 0])
    drag_handle = None
    selected_vertex = None
    ########################################
    ########## begin simulation ############
    ########################################
    ext_force = []
    for i in range(0, len(object_dict_list)):
        ext_force.append(np.zeros([3, ]))
    print("simulation begins")
    while simulate:
        #####################
        # interaction logic #
        #####################
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN and p_pressed == False:
                hold = True
                drag_start = np.array(pygame.mouse.get_pos(), dtype=np.double)
                drag_start3D = pixel2rayDir(drag_start, display, z, aspect_ratio, y_angle, camera_pos)
                drag_handle, selected_vertex = find_nearest_vertex(object_dict_list, drag_start3D, camera_pos)
            if event.type == pygame.MOUSEBUTTONUP and p_pressed == False:
                hold = False
                drag_handle = None
        if hold:
            drag_current = np.array(pygame.mouse.get_pos(), dtype=np.double)
            drag_current3D = pixel2rayDir(drag_current, display, z, aspect_ratio, y_angle, camera_pos)
            drag_handle = drag_current3D * np.linalg.norm(drag_handle-camera_pos) + camera_pos
            ext_force = 0
        #####################
        #   update logic    #
        #####################
        for i in range(0, len(object_dict_list)):
            object_dict_list[i] = update(object_dict_list[i], dt, ext_force[i])
        #####################
        #   display logic   #
        #####################
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        for i in range(0, len(object_dict_list)):
            draw_object(object_dict_list[i])
        if not drag_handle is None:
            glPointSize(5.0)
            glBegin(GL_LINES)
            glVertex3fv(drag_handle)
            glVertex3fv(object_dict_list[selected_vertex[0]]["q_t"][selected_vertex[1]])
            glEnd()
        pygame.display.flip()
        # drraw object
        pygame.time.wait(10)
if __name__ == "__main__":
    print(cube["q_t"].shape)
    visualize([cube], 0.01)