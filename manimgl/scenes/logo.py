from manim_imports_ext import *
from numpy import *


class HeartCurveScene(Scene):
    def construct(self):
        # 创建心形函数
        def heart_func(t):
            return np.array(
                [
                    2 * (np.sin(t) ** 3),
                    (
                        13 * np.cos(t)
                        - 5 * np.cos(2 * t)
                        - 2 * np.cos(3 * t)
                        - np.cos(4 * t)
                    )
                    / 8,
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
        self.play(ShowCreation(heart_curve), run_time=6)


class LogoScene(Scene):
    def construct(self):
        # 创建坐标系和点
        a_val = 1.5
        b_val = 3.5
        axes = Axes(
            x_range=(-1, 10, 1),
            y_range=(-1, 8, 1),
            width=10,
            height=6,
            axis_config={"color": GREY, "stroke_width": 6},
        )
        x_labels = Tex("x").next_to(axes.get_x_axis().get_end(), UR)
        y_labels = Tex("y").next_to(axes.get_y_axis().get_end(), UR)

        self.add(x_labels, y_labels, axes)

        # 函数图像
        def func(x):
            return 0.100 * x**3 - 1.500 * x**2 + 6.578 * x - 2.924

        graph = axes.get_graph(func, x_range=(0.2, 9), color=BLUE_C, stroke_width=6)
        slope = (func(b_val) - func(a_val)) / (b_val - a_val)
        intercept = func(a_val) - slope * a_val
        secant_func = lambda x: slope * x + intercept
        secant_line = axes.get_graph(secant_func, color=RED_C, x_range=[-1.5, 7])
        pt_a = axes.c2p(a_val, func(a_val))
        pt_b = axes.c2p(b_val, func(b_val))
        dot_a = Dot(pt_a, color=BLACK, radius=0.08)
        dot_b = Dot(pt_b, color=BLACK, radius=0.08)
        self.add(graph, secant_line, dot_a, dot_b)

        # 辅助线

        line_a_x = DashedLine(pt_a, axes.c2p(a_val, 0), color=WHITE, dash_length=0.1)
        line_a_y = DashedLine(
            pt_a, axes.c2p(0, func(a_val)), color=WHITE, dash_length=0.1
        )

        line_b_x = DashedLine(pt_b, axes.c2p(b_val, 0), color=WHITE, dash_length=0.1)
        line_b_y = DashedLine(
            pt_b, axes.c2p(0, func(b_val)), color=WHITE, dash_length=0.1
        )
        v_line = Line(
            axes.c2p(b_val, func(a_val)),
            axes.c2p(b_val, func(b_val)),
            color="#3f7d5c",
            stroke_width=6,
        )
        h_line = Line(
            axes.c2p(a_val, func(a_val)),
            axes.c2p(b_val, func(a_val)),
            color="#942357",
            stroke_width=6,
        )
        self.add(line_a_x, line_a_y, line_b_x, line_b_y, v_line, h_line)
        self.add(dot_a, dot_b)

        # 标签
        label_a_x = Tex("a", color=BLACK).next_to(axes.c2p(a_val, 0), DOWN)
        label_b_x = Tex("b", color=BLACK).next_to(axes.c2p(b_val, 0), DOWN)

        label_f_a = Tex("f(a)", color=BLACK).next_to(axes.c2p(0, func(a_val)), LEFT)
        label_f_b = Tex("f(b)", color=BLACK).next_to(axes.c2p(0, func(b_val)), LEFT)
        arrow_a = (
            Triangle(color=WHITE, fill_opacity=1)
            .scale(0.1).set_stroke(width=0)
            .move_to(axes.c2p(a_val, -0.1))
        )
        arrow_b = (
            Triangle(color=WHITE, fill_opacity=1)
            .scale(0.1).set_stroke(width=0)
            .move_to(axes.c2p(b_val, -0.1))
        )
        arrow_f_a = (
            Triangle(color=WHITE, fill_opacity=1)
            .scale(0.1).set_stroke(width=0)
            .rotate(270 * DEGREES)
            .move_to(axes.c2p(-0.1, func(a_val)))
        )
        arrow_f_b = (
            Triangle(color=WHITE, fill_opacity=1)
            .scale(0.1).set_stroke(width=0)
            .rotate(270 * DEGREES)
            .move_to(axes.c2p(-0.1, func(b_val)))
        )
        self.add(
            label_a_x,
            label_b_x,
            label_f_a,
            label_f_b,
            arrow_a,
            arrow_b,
            arrow_f_a,
            arrow_f_b,
        )
        
        # 矩形
        rects = axes.get_riemann_rectangles(
            graph,
            x_range=[4, 9],
            dx=0.5,
            input_sample_type="left", # 矩形高度取右端点，或者是 "center"
            stroke_width=1,
            stroke_color=GREY_B,
            fill_opacity=0.9,
            stroke_background=False,
            colors=[PURPLE, ORANGE],
        )

        self.add(rects)