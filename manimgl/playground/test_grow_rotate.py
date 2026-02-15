from manim_imports_ext import *


class GrowAndRotate(Scene):
    def construct(self):
        # test
        surface= ComplexSurfaceWireframe()
        self.play(SpinInFromNothing(surface, angle=2*PI, axis=UP, 
            run_time=2))