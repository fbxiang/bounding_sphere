import ctypes
import os
import numpy as np


class Sphere(ctypes.Structure):
    _fields_ = [
        ("x", ctypes.c_double),
        ("y", ctypes.c_double),
        ("z", ctypes.c_double),
        ("r", ctypes.c_double),
    ]


dll = ctypes.cdll.LoadLibrary(os.path.join(os.path.dirname(__file__), "_C.so"))
dll.min_sphere.argtypes = [ctypes.c_void_p, ctypes.c_size_t]
dll.min_sphere.restype = Sphere


def bounding_sphere(points: np.ndarray):
    points = np.ascontiguousarray(points.astype(np.float64).reshape([-1, 3]))
    sphere = dll.min_sphere(points.__array_interface__["data"][0], points.shape[0])
    return np.array([sphere.x, sphere.y, sphere.z], dtype=np.float64), sphere.r
