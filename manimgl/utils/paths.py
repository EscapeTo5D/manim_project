from __future__ import annotations
from manimlib.utils.paths import *
from manimlib.utils.space_ops import rotation_matrix
from manimlib.constants import OUT
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Callable
    from manimlib.typing import Vect3, Vect3Array

def spiral_path(angle: float, axis: Vect3 = OUT):
    if abs(angle) < STRAIGHT_PATH_THRESHOLD:
        return straight_path()
    if np.linalg.norm(axis) == 0:
        axis = OUT
    unit_axis = axis / np.linalg.norm(axis)

    def path(
            start_points: Vect3Array, end_points: Vect3Array, alpha: float
    ) -> Vect3Array:
        rot_matrix = rotation_matrix((alpha - 1) * angle, unit_axis)
        return start_points + alpha * np.dot(end_points - start_points, rot_matrix.T)

    return path