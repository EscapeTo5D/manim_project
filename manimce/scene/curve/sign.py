from manim import *

class Sign(Scene):
    def construct(self):
        image = SVGMobject(r"D:\manim_project\images\vector_images\sign.svg", fill_color=WHITE, stroke_color=WHITE)
        self.add(image)
        self.wait()