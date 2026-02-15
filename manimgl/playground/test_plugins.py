from manim_imports_ext import *

class TestPlugins(Scene):
    def construct(self):
        # test
        circle = Circle().scale(2)
        text = Text("你好")
        self.add(circle)
        self.add(text)     

        # 你好
        self.remove(circle) 