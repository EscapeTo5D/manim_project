from manim import *

class Two3DCoordinateSystems(ThreeDScene):
    def construct(self):
        t = ValueTracker(0)
        # 创建第一个三维坐标系
        axes1 = ThreeDAxes(
            x_range=(-5, 5),
            y_range=(-5, 5),
            z_range=(-5, 5),
            color=BLUE
        )
        ad = Arrow3D(RED, DOWN)
        sphere = Surface(
            lambda u, v: np.array([
                0.6 * np.cos(u) * np.cos(v),
                0.6 * np.cos(u) * np.sin(v),
                0.6 * np.sin(u)
            ]), v_range=[0, TAU], u_range=[-PI / 2, PI / 2],
            checkerboard_colors=[RED_D, RED_E], resolution=(15, 32)
        )
        # 创建第二个三维坐标系
        axes2 = ThreeDAxes(
            x_range=(-1, 1, 1),
            y_range=(-1, 1, 1),
            z_range=(-1, 1, 1),
            color=RED,
            x_length=2,
            y_length=2,
            z_length=2
        )
        yuan = Circle(radius=5)

        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
        # 设置第二个坐标系初始旋转角度
        # axes2.rotate(PI / 4, axis=axes1.z_axis)
        def func(t):
            return np.array(
                [
                    2 * np.sin(t),
                    2 * np.cos(t),
                    0,
                ]
            )
        # 添加两个坐标系
        s = sphere.move_to(axes2.coords_to_point(0, 0, 0))
        vg = VGroup(s, axes2)
        initial_point = axes1.coords_to_point(*func(t.get_value()))
        vg.move_to(initial_point)  # 设置球的初始位置

        self.add(axes1, vg)
        vg.add_updater(lambda x: x.move_to(axes1.c2p(*func(t.get_value()))))
        # 让第二个坐标系围绕第一个坐标系原点做圆周运动
        self.play(t.animate.set_value(8), Rotate(vg,10*PI),run_time=20, rate_func=linear)
        self.wait()