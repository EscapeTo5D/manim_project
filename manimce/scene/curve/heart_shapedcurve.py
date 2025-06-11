
from manim import *


class ParametricCurveExample(Scene):
    def construct(self):

        ax = Axes(
            x_range=[-48, 48, 5],
            y_range=[-30, 30, 5],
            x_length=12,
            y_length=7.5,
            axis_config={'tip_shape': StealthTip, "color": RED},  # 这将设置坐标轴线条颜色为红色

        )
        labels = ax.get_axis_labels()

        t = ValueTracker(0)
        path = VMobject()

        def func(t):
            return np.array(
                [
                    16 * (np.sin(t) ** 3),
                    13 * np.cos(t) - 5 * np.cos(2 * t) - 2 * np.cos(3 * t) - np.cos(4 * t),
                ]
            )

        cardioid = ax.plot_parametric_curve(
            func,
            t_range=[0, 2 * PI],
            color="#DC143C",
        )

        initial_point = ax.coords_to_point(*func(t.get_value()))
        dot = Dot(point=initial_point, radius=0.01)
        dot.add_updater(lambda x: x.move_to(ax.c2p(*func(t.get_value()))))
        path.set_points_as_corners([dot.get_center(), dot.get_center()])

        def update_path(path):
            previous_path = path.copy()
            previous_path.add_points_as_corners([dot.get_center()])
            path.become(previous_path)

        plane = NumberPlane(x_range=[-48, 48, 5], y_range=[-30, 30, 5], x_length=12, y_length=7.5,
                            background_line_style={"stroke_opacity": 0.7, "stroke_color": GREY})
        path.add_updater(update_path)
        basel = MathTex(r"x = 16\sin ^{3} \left ( t \right )").move_to(LEFT * 4.4 + UP * 3).set_color(BLUE)
        basel1 = MathTex(
            r"y=13\cos \left ( t \right ) -5\cos \left ( 2t \right ) -2\cos \left ( 3t \right ) -\cos \left ( 4t \right ) ").move_to(
            LEFT + UP * 2).set_color(BLUE)
        tex = VGroup(basel, basel1)
        self.wait()
        self.play(Write(tex), run_time=4)
        path.set_color("#DC143C")
        path.set_fill("#DC143C", opacity=0.7)
        self.play(FadeIn(plane, ax, labels), run_time=2)
        self.play(Create(cardioid), run_time=3)
        self.add(dot, path)
        self.play(t.animate.set_value(6.1), run_time=4, rate_functions=rate_functions.ease_in_expo)
        self.remove(dot, path)
        cardioid.set_fill("#DC143C", opacity=0.7)
        self.add(cardioid)
        self.wait()