from manimlib import *
from utils.paths import spiral_path


class SpinInFromNothing(GrowFromCenter):
    def __init__(
        self,
        mobject: Mobject,
        angle: float = PI / 2,
        axis: np.ndarray = OUT,
        point_color: str = None,
        **kwargs
    ) -> None:
        self.angle = angle
        self.axis = axis

        if 'axis' in kwargs:
            del kwargs['axis']

        super().__init__(
            mobject,
            path_func=spiral_path(angle, axis),
            point_color=point_color,
            **kwargs
        )