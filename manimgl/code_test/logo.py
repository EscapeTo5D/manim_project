from manim_imports_ext import *
from numpy import *

class HeartCurveScene(Scene):
    def construct(self):
        # 创建心形函数
        def heart_func(t):
            return np.array(
                [
                    2 * (np.sin(t) ** 3),
                    (13 * np.cos(t) - 5 * np.cos(2 * t) - 2 * np.cos(3 * t) - np.cos(4 * t))/8,
                    0,  # 这里给 z 分量为 0，保持二维
                ]
            )
        heart_curve = ParametricCurve(
            heart_func,
            t_range=(0, 2 * PI, 0.1),  # 调整分辨率为 0.1
            color=RED,  # 设定曲线颜色
        )
        dot_1 = Dot(radius=0.01, color=GREEN)
        def update_dot(dot):
            dot.move_to(heart_curve.get_end())
        dot_1.add_updater(update_dot)
        tail = TracingTail(dot_1, time_traced=3).set_color(GREEN)
        self.add(tail)
        self.add(dot_1)
        heart_curve.set_opacity(0).set_stroke(width=4)
        self.play(ShowCreation(heart_curve),run_time=6)