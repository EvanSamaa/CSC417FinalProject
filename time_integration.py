import numpy as np
from scipy.linalg import polar

def update_rigid(object_dict_list, dt, ext_force, k):
    #################################################
    ###### getting variables from object dict #######
    #################################################

    qt = object_dict_list["q_t"]
    q0 = object_dict_list["V0"]
    t0 = object_dict_list["t_0"]
    t = qt.mean(axis=0, keepdims=True)
    q_dot_t = object_dict_list["q_dot_t"]
    mass = object_dict_list["mass"]

    #################################################
    ############## actual update rule ###############
    #################################################
    q = q0 - t0
    p = qt - t
    Apq = np.zeros((q.shape[1], q.shape[1]))
    Aqq = np.zeros((q.shape[1], q.shape[1]))
    for i in range(0, q.shape[0]):
        Apq = Apq + np.expand_dims(p[i, :], axis=1) @ np.expand_dims(q[i, :], axis=1).transpose()
        Aqq = Aqq + np.expand_dims(q[i, :], axis=1) @ np.expand_dims(q[i, :], axis=1).transpose()
    R, S = polar(Apq)
    R_t = Apq * np.linalg.inv(S)
    R_t = np.expand_dims(R_t, 0)
    print(R_t)
    g = (R_t @ np.expand_dims(q0 - t0, 2))[:, :, 0] + t
    # here I'm using backawrds euler to be a bit more stable
    new_q_dot_t = q_dot_t + dt * ext_force / mass + (g - qt) / dt
    qt = qt + new_q_dot_t * dt
    object_dict_list["q_t"] = qt
    object_dict_list["q_dot_t"] = new_q_dot_t
    return object_dict_list

