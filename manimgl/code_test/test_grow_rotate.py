
from manim_imports_ext import *


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

class GrowAndRotate(Scene):
    def construct(self):
        # test
        self.play(SpinInFromNothing(Square(), angle=PI, run_time=5))