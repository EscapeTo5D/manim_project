from math import tan

from manimlib import *


class SurfaceExample(Scene):
    CONFIG = {
        "camera_class": ThreeDCamera,
    }

    def construct(self):
        ax = ThreeDAxes()
        ax1 = ThreeDAxes(
            x_range=[-1, 1, 1],
            y_range=[-1, 1, 1],
            z_range=[-1, 1, 1],
        )
        t = ValueTracker(0)
        sphere1 = Sphere(radius=0.8)
        circle = Circle(radius=5.0, stroke_width=0.7).set_color(RED_D)
        sun_texture = "images/8k_sun.jpg"
        milky_texture = "images/milky_way.jpg"
        background_image = ImageMobject(milky_texture).scale(2).fix_in_frame()
        self.add(background_image)
        sphere = Sphere(radius=0.6)
        line = Line3D(start=ax1.c2p(tan(PI* 47 / 360)/1.4, 0, -1/1.4), end=ax1.c2p(tan(PI* 313 / 360)/1.4, 0, 1/1.4), stroke_width=1.5).set_color(BLUE_E)
        # 你可以使用最多两个图像对曲面进行纹理处理，
        # 这两个图像将被解释为朝向灯光的一侧和远离灯光的一侧。
        # 这些可以是URL，也可以是指向本地文件的路径
        # day_texture = "EarthTextureMap"
        # night_texture = "NightEarthTextureMap"
        day_texture = "images/earth.jpg"
        night_texture = "https://upload.wikimedia.org/wikipedia/commons/thumb/b/ba/The_earth_at_night.jpg/1280px-The_earth_at_night.jpg"
        surfaces = [
            TexturedSurface(surface, day_texture, night_texture)
            for surface in [sphere]
        ]
        surface_sun = [
            TexturedSurface(surface, sun_texture)
            for surface in [sphere1]
        ]
        # for mob in surfaces:
        #     mob.shift(IN)
        #     mob.mesh = SurfaceMesh(mob)
        #     mob.mesh.set_stroke(BLUE, 1, opacity=0.5)

        # 设置视角
        frame = self.camera.frame
        frame.set_euler_angles(
            theta=-20 * DEGREES,
            phi=75 * DEGREES,
        )

        surface = surfaces[0]
        surface.rotate(PI* 47 / 360, axis=DOWN)
        self.add(circle)
        self.add(surface)
        # self.play(
        #     FadeIn(surface),
        #     ShowCreation(surface.mesh, lag_ratio=0.01, run_time=3),
        # )
        # for mob in surfaces:
        #     mob.add(mob.mesh)
        # surface.save_state()
        # self.play(Rotate(surface, 2* PI), run_time=5)
        light = self.camera.light_source.move_to(np.array([0, 0, 0]))
        self.add(light,surface_sun[0])
        earth = Group(line.move_to(ax1.coords_to_point(0, 0, 0)),surface.move_to(ax1.coords_to_point(0, 0, 0)))
        # earth = line.move_to(ax1.coords_to_point(0, 0, 0))
        def func(t):
            return np.array(
                [
                    5 * np.sin(t),
                    5 * np.cos(t),
                    0,
                ]
            )

        initial_point = ax.coords_to_point(*func(t.get_value()))
        earth.move_to(initial_point)  # 设置球的初始位置
        earth.add_updater(lambda x: x.move_to(ax.c2p(*func(t.get_value()))))
        # light.save_state()
        # self.play(light.move_to, 3 * IN, run_time=5)
        # self.play(AnimationGroup(MoveAlongPath(surface, circle)), run_time=15, rate_func=linear)
        self.play(t.animate.set_value(10), Rotate(earth,10*PI,axis=np.array([tan(PI* 47 / 360), 0, -1])),run_time=20, rate_func=linear)
