from jedi.api import file_name

from manim_imports_ext import *

class Sign(Scene):
    def construct(self):
        # q
        svg = SVGMobject(r"D:\manim_project\images\vector_images\sign.svg", fill_color=WHITE, stroke_color=WHITE)
        self.add(svg)
        self.play(ShowCreation(
            rate_func = linear,
            run_time=1
        ))