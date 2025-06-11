from math import *

import numpy as np
from manimlib import *

script_1 = '赤道 0°'
script_2 = '北回归线 23.5°'
script_3 = '南回归线 23.5°'
script_4 = '北极圈 66.5°'
script_5 = '南极圈 66.5°'
script_6 = '阳光'
script_7 = '地轴'


class TreeDExample(Scene):
    def construct(self):
        milky_texture = "images/milky_way.jpg"
        day_texture = "images/earth.jpg"
        night_texture = "https://upload.wikimedia.org/wikipedia/commons/thumb/b/ba/The_earth_at_night.jpg/1280px" \
                        "-The_earth_at_night.jpg"

        def arrow_func(t, r):
            return Group(Arrow(start=np.array([(r + 2) * cos(t * DEGREES), 0,
                                               (r + 2) * sin(t * DEGREES)]),
                               end=np.array([r * cos(t * DEGREES), 0, r * sin(t * DEGREES)])).set_color(YELLOW),
                         Arrow(start=np.array([(r + 2) * cos(t * DEGREES) - 0.5 * sin(t * DEGREES), 0,
                                               (r + 2) * sin(t * DEGREES) + 0.5 * cos(t * DEGREES)]),
                               end=np.array([r * cos(t * DEGREES) - 0.5 * sin(t * DEGREES), 0,
                                             r * sin(t * DEGREES) + 0.5 * cos(t * DEGREES)])).set_color(YELLOW),
                         Arrow(start=np.array([(r + 2) * cos(t * DEGREES) + 0.5 * sin(t * DEGREES), 0,
                                               (r + 2) * sin(t * DEGREES) - 0.5 * cos(t * DEGREES)]),
                               end=np.array([r * cos(t * DEGREES) + 0.5 * sin(t * DEGREES), 0,
                                             r * sin(t * DEGREES) - 0.5 * cos(t * DEGREES)])).set_color(YELLOW))

        dz = Line3D(np.array([0, 0, -3]), np.array([0, 0, 3])).set_color(BLUE_E)
        sphere = Sphere(radius=2.5, fill_opacity=1.0)
        arrow = CurvedArrow(np.array([0.5, 0, 2.6]), np.array([-0.5, 0, 2.6]), radius=1, angle=PI * 3 / 2).scale(0.7)
        background_image = ImageMobject(milky_texture).scale(2).fix_in_frame()
        self.add(background_image)

        surfaces = [
            TexturedSurface(surface, day_texture, night_texture)
            for surface in [sphere]
        ]
        # for mob in surfaces:
        #     mob.shift(IN)
        #     mob.mesh = SurfaceMesh(mob)
        #     mob.mesh.set_stroke(BLUE, 1, opacity=0.5)
        # for mob in surfaces:
        #     mob.add(mob.mesh)
        surface = surfaces[0].rotate(angle=PI / 3, axis=np.array([0, 0, -1]))
        frame = self.camera.frame
        frame.set_euler_angles(
            theta=0 * DEGREES,
            phi=90 * DEGREES,
        )
        equator = ParametricCurve(
            lambda t: np.array(
                [
                    10 * np.sin(t),
                    10 * np.cos(t),
                    0,
                ]
            ),
            t_range=[0, 2 * PI],
            color="#FFB90F",
            stroke_width=1,
        )
        north_tropic_line = ParametricCurve(
            lambda t: np.array(
                [
                    10 * np.sin(t),
                    10 * np.cos(t),
                    2.5 * sin(23.5 * DEGREES),
                ]
            ),
            t_range=[0, 2 * PI],
            color="#0FF1CE",
            stroke_width=0.6,
        )
        arctic_circle = ParametricCurve(
            lambda t: np.array(
                [
                    10 * np.sin(t),
                    10 * np.cos(t),
                    2.5 * sin(66.5 * DEGREES),
                ]
            ),
            t_range=[0, 2 * PI],
            color="#FF0000",
            stroke_width=0.5,
        )
        light = self.camera.light_source.move_to(np.array([0, -100000, 0]))
        self.add(light, surface)
        self.wait()
        # 地轴 倾斜角23.5°
        dz_text = Text(script_7, font='Source Han Sans').move_to(np.array([-0.3, 2.8, 0])).scale(0.4).set_color(
            RED).fix_in_frame()
        self.play(FadeIn(dz), FadeIn(dz_text))
        self.wait(2)
        self.play(FadeOut(dz_text))
        # 自转
        self.play(frame.animate.rotate(30 * DEGREES, LEFT), light.move_to, np.array([0, -100000 * sin(PI * 2 / 3), 500]))
        fx = Group(Text('N').move_to(np.array([0, 3.2, 0])).set_color(RED), Text('S').move_to(np.array([0, -3.2, 0])).set_color(YELLOW),
                   Text('E').move_to(np.array([3.2, 0, 0])).set_color(BLUE), Text('W').move_to(np.array([-3.2, 0, 0])).set_color(GREEN)).fix_in_frame()
        self.play(FadeIn(arrow), FadeIn(fx))
        self.wait(2)
        surface.add_updater(lambda m, dt: m.rotate(0.5 * dt, OUT))
        self.play(FadeOut(arrow))
        self.wait(3)
        # 赤道
        self.play(equator.animate.scale(0.25), run_time=2)
        equator_text = Text(script_1, font='Source Han Sans').scale(0.3).move_to(np.array([2.8, 0, 0])).set_color(
            '#FFB90F').fix_in_frame()
        self.play(FadeIn(equator_text))
        self.wait(2)
        # 北回归线
        self.play(north_tropic_line.animate.scale(cos(23.5 * DEGREES) / 4), run_time=2)
        north_tropic_line_text = Text(script_2, font='Source Han Sans').scale(0.3).move_to(
            np.array([3.17 * cos(23.5 * DEGREES), 2.5 * sin(23.5 * DEGREES), 0])).set_color(
            '#0FF1CE').fix_in_frame()
        self.play(FadeIn(north_tropic_line_text))
        self.wait(2)
        # 北极圈
        self.play(arctic_circle.animate.scale(cos(66.5 * DEGREES) / 4), run_time=2)
        arctic_circle_text = Text(script_4, font='Source Han Sans').scale(0.3).move_to(
            np.array([3.8 * cos(66.5 * DEGREES), 2.5 * sin(66.5 * DEGREES), 0])).set_color(
            '#FF0000').fix_in_frame()
        self.play(FadeIn(arctic_circle_text))
        self.wait(2)
        self.play(frame.animate.rotate(30 * DEGREES, RIGHT), light.move_to, np.array([0, -1000, 0]))
        self.wait()
        self.play(light.move_to, np.array([100000, 0, 100000 * tan(PI * 47 / 360)]), run_time=1)
        arrow_group_eq = arrow_func(23.5, 3)
        sun_text = Text(script_6, font='Source Han Sans').scale(0.4).move_to(
            np.array([5.1 * cos(23.5 * DEGREES), 5.1 * sin(23.5 * DEGREES),
                      0])).set_color(YELLOW).fix_in_frame()
        self.play(FadeIn(arrow_group_eq), FadeIn(sun_text), run_time=1)
        path = Line(np.array([4 * cos(23.5 * DEGREES), 0,
                              4 * sin(23.5 * DEGREES)]), np.array([3.7 * cos(23.5 * DEGREES), 0,
                                                                   3.7 * sin(23.5 * DEGREES)]))
        arrow_group_eq.save_state()
        self.play(MoveAlongPath(arrow_group_eq, path))
        self.play(Restore(arrow_group_eq))
        self.play(FadeOut(arrow_group_eq), FadeOut(sun_text))
        # 北极昼
        self.play(frame.animate.rotate(90 * DEGREES, LEFT), run_time=1)
        self.wait(PI * 0.7)
        # self.play(Rotate(surface, angle=PI, axis=np.array([0, 0, 1])), run_time=10)
        self.play(frame.animate.rotate(180 * DEGREES, OUT))
        self.wait(PI * 1.7)
        # 夏至日落
        # self.play(Rotate(surface, angle=PI, axis=np.array([0, 0, 1])), run_time=10)
        # self.wait(2)
