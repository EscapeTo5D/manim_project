cript = '''

'''
from manim_imports_ext import *


class CalabiYauSurfaceScene(InteractiveScene):
    def construct(self):

        # 设置TEXT 和 equation 公式
        math_equation = Tex()
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
        math_equation = Tex("\\left\\{\\begin{array}{c}x=\\Re\\left(\\sqrt[n]{e^{2 i \\pi k} \\cos^{2}  (a+b i) }  \\right)"
                            " \\\\y=\\Re\\left(\\sqrt[n]{e^{2 i \\pi g} \\sin^{2}  (a+b i)}\\right)"
                            " \\\\z=\\Im\\left(\\cos (t) \\sqrt[n]{e^{2 i \\pi k} \\cos^{2}  (a+b i)}+\\sin (t) "
                            "\\sqrt[n]{e^{2 i \\pi g} \\sin^{2}  (a+b i)}\\right)\\end{array}\\right.")
        math_equation.scale(0.5).move_to(LEFT)
        self.play(ShowCreation(math_equation))

class CalabiYauVisualization(InteractiveScene):
    def construct(self):
        # 创建 n=2 到 n=5 的曲面对象
        axes = ThreeDAxes()
        surfaces = [
            CalabiYauSurface(axes=axes, n=n, alpha=PI / 4, resolution=(51, 51))
            for n in range(2, 6)
        ]
        current = surfaces[0]
        self.add(current)
        for next_surface in surfaces[1:]:
            self.play(ReplacementTransform(current, next_surface), run_time=3)
            current = next_surface

        # 添加卡拉比流形
        axes = ThreeDAxes()
        calabi_yau_shader = CalabiYauSurface(
            axes=axes,
            n=2,
            alpha=PI / 4,
            resolution=(31, 31),
            brightness=1.0
        )
        wireframe = ComplexSurfaceWireframe(n=2)
        self.play(SpinInFromNothing(calabi_yau_shader, axis=UP, angle=2 * PI, run_time=2))
        self.wait()
        self.play(SpinInFromNothing(wireframe, axis=UP, angle=2 * PI, run_time=2))
        # 不同n下的卡拉比丘流形

        
        self.play(SpinShowCreation(wireframe, axis=UP
            , angle=2*PI), run_time=6)


class ComplexSurface(InteractiveScene):
    def construct(self):
        # tt
        wireframe = ComplexSurfaceWireframe()
        self.play(Rotate(wireframe, axis=UP, angle=2*PI,run_time=3) ,rate_func=linear)