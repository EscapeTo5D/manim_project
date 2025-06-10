cript = '''

'''
from manim_imports_ext import *


class CalabiYauSurfaceScene(InteractiveScene):
    def construct(self):

        # 设置TEXT 和 equation 公式
        title_e = Text(
            "Calabi-Yau Manifold",
            font_size=48,
            color=YELLOW,
            t2f={"world": "Forte"}
        ).to_edge(UP).fix_in_frame()
        title_c = Text(
            "\u5361\u62c9\u6bd4-\u4e18\u6210\u6850\u6d41\u5f62",
            font_size=48,
            font="Source Han Sans"
        ).to_edge(UP).fix_in_frame()
        self.add(title_e)
        # Calabi-Yau 
        axes = ThreeDAxes()
        calabi_yau_45 = CalabiYauSurface(
            axes=axes,
            n=5,
            alpha=PI / 4,
            resolution=(51, 51),
        )
        self.add(calabi_yau_45)
        self.wait(6)

class ComplexSurfaceWireframeScene(InteractiveScene):
    def construct(self):

        # 添加和展示线框
        wireframe = ComplexSurfaceWireframe()
        self.play(
            RotatingCreate(wireframe,
            axis=UP,
            angle=2*PI,
            run_time=6,
            rate_func=linear
        ))

class CalabiYauVisualization(InteractiveScene):
    def construct(self):
        # 添加卡拉比流形
        axes = ThreeDAxes()
        calabi_yau_shader = CalabiYauSurface(
            axes=axes,
            n=5,
            alpha=PI / 4,
            resolution=(21, 21),
            brightness=1.1
        )
        wireframe = ComplexSurfaceWireframe()
        self.play(ShowCreation(calabi_yau_shader), run_time=4)