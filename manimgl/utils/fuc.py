from __future__ import annotations
from manim_imports_ext import *
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Callable
    from manimlib.typing import Vect3, Vect3Array

def rotation_matrix_4d(angle_xw=0, angle_yw=0.0, angle_zw=0, angle_xy=0, angle_yz=0, angle_xz=0,):
    r_xw = np.array([
        [np.cos(angle_xw), 0, 0, np.sin(angle_xw)],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [-np.sin(angle_xw), 0, 0, np.cos(angle_xw)]
    ])
    r_yw = np.array([
        [1, 0, 0, 0],
        [0, np.cos(angle_yw), 0, -np.sin(angle_yw)],
        [0, 0, 1, 0],
        [0, np.sin(angle_yw), 0, np.cos(angle_yw)]
    ])
    r_zw = np.array([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, np.cos(angle_zw), -np.sin(angle_zw)],
        [0, 0, np.sin(angle_zw), np.cos(angle_zw)]
    ])
    r_xy = np.array([
        [np.cos(angle_xy), np.sin(angle_xy), 0, 0],
        [-np.sin(angle_xy), np.cos(angle_xy), 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ])
    r_yz = np.array([
        [1, 0, 0, 0],
        [0, np.cos(angle_yz), np.sin(angle_yz), 0],
        [0, -np.sin(angle_yz), np.cos(angle_yz), 0],
        [0, 0, 0, 1]
    ])
    r_xz = np.array([
        [np.cos(angle_xz), 0, -np.sin(angle_xz), 0],
        [0, 1, 0, 0],
        [np.sin(angle_xz), 0, np.cos(angle_xz), 0],
        [0, 0, 0, 1]
    ])
    return r_xw @ r_yw @ r_zw @ r_xy @ r_yz @ r_xz