from manim import *
import itertools as it
from _functools import reduce
import operator as op


class FourierCirclesScene(ZoomedScene):

    def __init__(
            self,
            n_vectors=10,
            big_radius=2,
            colors=[
                BLUE_D,
                BLUE_C,
                BLUE_E,
                GREY_BROWN,
            ],  # 圆圈的颜色
            vector_config={
                'buff': 0,
                'max_tip_length_to_length_ratio': 0.25,
                'tip_length': 0.15,
                'max_stroke_width_to_length_ratio': 8,
                'stroke_width': 1.7,
            },
            circle_config={
                'stroke_width': 0.4
            },
            base_frequency=1,
            slow_factor=0.3,
            center_point=ORIGIN,
            parametric_function_step_size=0.001,
            drawn_path_color=YELLOW,  # 绘制过程中线的颜色
            drawn_path_stroke_width=2,  #
            interpolate_config=[0, 1],
            # Zoom config
            include_zoom_camera=False,
            scale_zoom_camera_to_full_screen=False,
            scale_zoom_camera_to_full_screen_at=4,
            zoom_factor=0.8,  # 缩放因子：越小放大的区域越小，越小放大倍数越大
            zoomed_display_height=3,
            zoomed_display_width=4,
            image_frame_stroke_width=20,
            zoomed_camera_config={
                "default_frame_stroke_width": 1,  # 放大框的线粗细
                "background_opacity": 1,  # 放大框的不透明度
                'cairo_line_width_multiple': 0.01
            },
            zoom_position=lambda mob: mob.move_to(ORIGIN),
            zoom_camera_to_full_screen_config={
                "run_time": 3,
                "func": there_and_back_with_pause,
                "velocity_factor": 1,
            },
            wait_before_start=None,
            **kwargs,
    ):
        self.n_vectors = n_vectors
        self.big_radius = big_radius
        self.colors = colors  #
        self.vector_config = vector_config
        self.circle_config = circle_config
        self.base_frequency = base_frequency  #
        self.slow_factor = slow_factor
        self.center_point = center_point
        self.parametric_function_step_size = parametric_function_step_size
        self.drawn_path_color = drawn_path_color
        self.drawn_path_stroke_width = drawn_path_stroke_width
        self.interpolate_config = interpolate_config
        self.include_zoom_camera = include_zoom_camera
        self.scale_zoom_camera_to_full_screen = scale_zoom_camera_to_full_screen
        self.scale_zoom_camera_to_full_screen_at = scale_zoom_camera_to_full_screen_at
        self.zoom_position = zoom_position
        self.zoom_camera_to_full_screen_config = zoom_camera_to_full_screen_config
        self.wait_before_start = wait_before_start

        super().__init__(
            zoom_factor=zoom_factor,
            zoomed_display_height=zoomed_display_height,
            zoomed_display_width=zoomed_display_width,
            image_frame_stroke_width=image_frame_stroke_width,
            zoomed_camera_config=zoomed_camera_config,
            **kwargs
        )

    def setup(self):
        ZoomedScene.setup(self)
        self.slow_factor_tracker = ValueTracker(
            self.slow_factor
        )
        self.vector_clock = ValueTracker(0)
        self.add(self.vector_clock)

    def add_vector_clock(self):
        self.vector_clock.add_updater(
            lambda m, dt: m.increment_value(
                self.get_slow_factor() * dt
            )
        )

    def get_slow_factor(self):
        return self.slow_factor_tracker.get_value()

    def get_vector_time(self):
        return self.vector_clock.get_value()

    def get_freqs(self):
        n = self.n_vectors
        # 取正负对称的频率点
        all_freqs = list(range(n // 2, -n // 2, -1))
        all_freqs.sort(key=abs)
        return all_freqs

    def get_coefficients(self):
        return [complex(0) for _ in range(self.n_vectors)]

    def get_color_iterator(self):
        return it.cycle(self.colors)

    def get_rotating_vectors(self, freqs=None, coefficients=None):
        vectors = VGroup()
        self.center_tracker = VectorizedPoint(self.center_point)

        if freqs is None:
            freqs = self.get_freqs()
        if coefficients is None:
            coefficients = self.get_coefficients()

        last_vector = None
        for freq, coefficient in zip(freqs, coefficients):
            if last_vector:
                center_func = last_vector.get_end
            else:
                center_func = self.center_tracker.get_location
            vector = self.get_rotating_vector(
                coefficient=coefficient,
                freq=freq,
                center_func=center_func,
            )
            # 添加 -> jermain
            vector.shift(vector.center_func() - vector.get_start())
            vectors.add(vector)
            last_vector = vector
        return vectors

    def get_rotating_vector(self, coefficient, freq, center_func):
        vector = Vector(RIGHT * abs(coefficient), **self.vector_config)

        if abs(coefficient) == 0:
            phase = 0
        else:
            phase = np.log(coefficient).imag  # 取得Fn的相位 Im[ln(Fn)]
        # 向量Fn
        vector.rotate(phase, about_point=ORIGIN)

        vector.freq = freq
        vector.coefficient = coefficient
        vector.center_func = center_func
        vector.add_updater(self.update_vector)
        return vector

    def update_vector(self, vector, dt):
        time = self.get_vector_time()
        coef = vector.coefficient
        freq = vector.freq
        phase = np.log(coef).imag

        vector.set_length(abs(coef))
        vector.set_angle(phase + time * freq * TAU)
        vector.shift(vector.center_func() - vector.get_start())
        return vector

    def get_circles(self, vectors):
        return VGroup(*[
            self.get_circle(
                vector,
                color=color
            )
            for vector, color in zip(
                vectors,
                self.get_color_iterator()
            )
        ])

    def get_circle(self, vector, color=BLUE):
        circle = Circle(color=color, **self.circle_config)
        circle.center_func = vector.get_start
        circle.radius_func = vector.get_length
        # 添加 -> jermain
        circle.scale_to_fit_width(2 * circle.radius_func())
        circle.shift(circle.center_func())

        circle.add_updater(self.update_circle)
        return circle

    def update_circle(self, circle):
        # jermain
        circle.scale_to_fit_width(2 * circle.radius_func())
        circle.move_to(circle.center_func())
        return circle

    def get_vector_sum_path(self, vectors, color=YELLOW):
        coefs = [v.coefficient for v in vectors]
        freqs = [v.freq for v in vectors]
        center = vectors[0].get_start()

        path = ParametricFunction(
            lambda t: center + reduce(op.add, [
                complex_to_R3(
                    coef * np.exp(TAU * 1j * freq * t)
                )
                for coef, freq in zip(coefs, freqs)
            ]),
            t_range=[0, 1, self.parametric_function_step_size],
            color=color,
        )
        return path

    def get_drawn_path_alpha(self):
        return self.get_vector_time()

    def get_drawn_path(self, vectors, stroke_width=None, **kwargs):
        if stroke_width is None:
            stroke_width = self.drawn_path_stroke_width
        path = self.get_vector_sum_path(vectors, **kwargs)

        broken_path = CurvesAsSubmobjects(path)
        broken_path.curr_time = 0
        start, end = self.interpolate_config

        def update_path(path, dt):
            alpha = self.get_drawn_path_alpha()
            n_curves = len(path)
            for a, sp in zip(np.linspace(0, 1, n_curves), path):
                b = (alpha - a)
                if b < 0:
                    width = 0
                else:
                    width = stroke_width * interpolate(start, end, (1 - (b % 1)))
                sp.set_stroke(width=width)
            path.curr_time += dt
            return path

        broken_path.set_color(self.drawn_path_color)
        broken_path.add_updater(update_path)
        return broken_path

    def get_y_component_wave(self,
                             vectors,
                             left_x=1,
                             color=PINK,
                             n_copies=2,
                             right_shift_rate=5):
        path = self.get_vector_sum_path(vectors)
        wave = ParametricFunction(
            lambda t: op.add(
                right_shift_rate * t * LEFT,
                path.function(t)[1] * UP
            ),
            t_min=path.t_min,
            t_max=path.t_max,
            color=color,
        )
        wave_copies = VGroup(*[
            wave.copy()
            for x in range(n_copies)
        ])
        wave_copies.arrange(RIGHT, buff=0)
        top_point = wave_copies.get_top()
        wave.creation = Create(
            wave,
            run_time=(1 / self.get_slow_factor()),
            rate_func=linear,
        )
        cycle_animation(wave.creation)
        wave.add_updater(lambda m: m.shift(
            (m.get_left()[0] - left_x) * LEFT
        ))

        def update_wave_copies(wcs):
            index = int(
                wave.creation.total_time * self.get_slow_factor()
            )
            wcs[:index].match_style(wave)
            wcs[index:].set_stroke(width=0)
            wcs.next_to(wave, RIGHT, buff=0)
            wcs.align_to(top_point, UP)

        wave_copies.add_updater(update_wave_copies)

        return VGroup(wave, wave_copies)

    def get_wave_y_line(self, vectors, wave):
        return DashedLine(
            vectors[-1].get_end(),
            wave[0].get_end(),
            stroke_width=1,
            dash_length=DEFAULT_DASH_LENGTH * 0.5,
        )

    def get_coefficients_of_path(self, path, n_samples=10000, freqs=None):
        if freqs is None:
            freqs = self.get_freqs()
        dt = 1 / n_samples
        ts = np.arange(0, 1, dt)
        samples = np.array([
            path.point_from_proportion(t)
            for t in ts
        ])
        samples -= self.center_point
        complex_samples = samples[:, 0] + 1j * samples[:, 1]
        return [
            np.array([
                np.exp(-TAU * 1j * freq * t) * cs
                for t, cs in zip(ts, complex_samples)
            ]).sum() * dt for freq in freqs
        ]

    def zoom_config(self):
        # This is not in the original version of the code.
        self.activate_zooming(animate=False)
        self.zoom_position(self.zoomed_display)
        self.zoomed_camera.frame.add_updater(lambda mob: mob.move_to(self.vectors[-1].get_end()))

    def scale_zoom_camera_to_full_screen_config(self):
        # This is not in the original version of the code.
        def fix_update(mob, dt, velocity_factor, dt_calculate):
            if dt == 0 and mob.counter == 0:
                rate = velocity_factor * dt_calculate
                mob.counter += 1
            else:
                rate = dt * velocity_factor
            if dt > 0:
                mob.counter = 0
            return rate

        fps = 1 / self.camera.frame_rate  #
        mob = self.zoomed_display
        mob.counter = 0
        velocity_factor = self.zoom_camera_to_full_screen_config["velocity_factor"]
        mob.start_time = 0
        run_time = self.zoom_camera_to_full_screen_config["run_time"]
        # jermain
        mob_height = mob.get_height()
        mob_width = mob.get_width()
        mob_center = mob.get_center()
        ctx = self.zoomed_camera.cairo_line_width_multiple

        def update_camera(mob, dt):
            line = Line(
                mob_center,
                # self.camera_frame.get_center()
                # 修改 -> jermain
                self.camera.frame_center,
            )
            mob.start_time += fix_update(mob, dt, velocity_factor, fps)
            if mob.start_time <= run_time:
                alpha = mob.start_time / run_time
                alpha_func = self.zoom_camera_to_full_screen_config["func"](alpha)
                coord = line.point_from_proportion(alpha_func)

                mob.set_height(
                    interpolate(
                        mob_height,
                        # self.camera_frame.get_height(),
                        # 修改 -> jermain
                        self.camera.frame_height,
                        alpha_func
                    ),
                    # 当前还没有排查为什么加入会报错
                    # stretch=True
                )
                mob.set_width(
                    interpolate(
                        mob_width,
                        # self.camera_frame.get_width(),
                        # 修改 -> jermain
                        self.camera.frame_width,
                        alpha_func
                    ),
                    # 当前还没有排查为什么加入会报错
                    # stretch=True
                )
                self.zoomed_camera.cairo_line_width_multiple = interpolate(
                    ctx,
                    self.camera.cairo_line_width_multiple,
                    alpha_func
                )
                mob.move_to(coord)
            return mob

        self.zoomed_display.add_updater(update_camera)


class AbstractFourierOfSVGSymbol(FourierCirclesScene):
    def __init__(
            self,
            n_vectors=100,
            center_point=ORIGIN,
            slow_factor=0.05,
            n_cycles=None,
            run_time=10,
            file_name=None,
            start_drawn=False,
            path_custom_position=lambda mob: mob,
            max_circle_stroke_width=1,
            svg_config={
                "fill_opacity": 0,
                "stroke_color": WHITE,
                "stroke_width": 1,
                "height": 7
            },
            include_zoom_camera=False,
            scale_zoom_camera_to_full_screen=False,
            scale_zoom_camera_to_full_screen_at=1,
            zoom_position=lambda mob: mob.scale(0.8).move_to(ORIGIN).to_edge(RIGHT),
            **kwargs,
    ):

        self.n_cycles = n_cycles
        self.run_time = run_time
        self.file_name = file_name
        self.path_custom_position = path_custom_position
        self.max_circle_stroke_width = max_circle_stroke_width
        self.svg_config = svg_config
        self.start_drawn = start_drawn,
        self.include_zoom_camera = include_zoom_camera
        self.scale_zoom_camera_to_full_screen = scale_zoom_camera_to_full_screen
        self.scale_zoom_camera_to_full_screen_at = scale_zoom_camera_to_full_screen_at
        # self.zoom_position = zoom_position

        super().__init__(
            n_vectors=n_vectors,
            center_point=center_point,
            slow_factor=slow_factor,
            include_zoom_camera=include_zoom_camera,
            zoom_position=zoom_position,
            scale_zoom_camera_to_full_screen=scale_zoom_camera_to_full_screen,
            scale_zoom_camera_to_full_screen_at=scale_zoom_camera_to_full_screen_at,
            **kwargs
        )

    def construct(self):
        # This is not in the original version of the code.
        self.add_vectors_circles_path()
        if self.wait_before_start is not None:
            self.wait(self.wait_before_start)
        self.add_vector_clock()
        self.add(self.vector_clock)
        if self.include_zoom_camera:
            self.zoom_config()
        # # jermain
        if self.n_cycles:
            if not self.scale_zoom_camera_to_full_screen:
                for n in range(self.n_cycles):
                    self.run_one_cycle()
            else:
                cycle = 1 / self.slow_factor
                total_time = cycle * self.n_cycles
                total_time -= self.scale_zoom_camera_to_full_screen_at
                self.wait(self.scale_zoom_camera_to_full_screen_at)
                self.scale_zoom_camera_to_full_screen_config()
                self.wait(total_time)

        elif not self.n_cycles and self.run_time:
            if self.scale_zoom_camera_to_full_screen:
                self.run_time -= self.scale_zoom_camera_to_full_screen_at
                self.wait(self.scale_zoom_camera_to_full_screen_at)
                self.scale_zoom_camera_to_full_screen_config()
            self.wait(self.run_time)

    def add_vectors_circles_path(self):
        path = self.get_path()
        self.path_custom_position(path)  #
        coeds = self.get_coefficients_of_path(path)

        vectors = self.get_rotating_vectors(coefficients=coeds)
        circles = self.get_circles(vectors)
        self.set_decreasing_stroke_widths(circles)
        drawn_path = self.get_drawn_path(vectors)

        self.vector_clock.increment_value(0)

        # self.add(path)
        self.add(vectors)
        self.add(circles)
        self.add(drawn_path)

        self.vectors = vectors
        self.circles = circles
        self.path = path
        self.drawn_path = drawn_path

    def run_one_cycle(self):
        time = 1 / self.slow_factor
        self.wait(time)

    def set_decreasing_stroke_widths(self, circles):
        mcsw = self.max_circle_stroke_width
        for k, circle in zip(it.count(1), circles):
            circle.set_stroke(width=max(
                mcsw / k,
                mcsw,
            ))
        return circles

    def get_shape(self):
        shape = SVGMobject(self.file_name, **self.svg_config)
        return shape

    def get_path(self):
        shape = self.get_shape()
        path = shape.family_members_with_points()[0]
        return path


class ZoomedDisplayToFullScreen(AbstractFourierOfSVGSymbol):
    def __init__(
            self,
            slow_factor=1/60,
            n_vectors=1000,
            run_time=60,
            file_name="images/wukong.svg",
            # Zoom config
            include_zoom_camera=True,
            zoom_position=lambda zc: zc.to_corner(DR),
            # Zoomed display to Full screen config
            scale_zoom_camera_to_full_screen=True,
            scale_zoom_camera_to_full_screen_at=4,
            zoom_camera_to_full_screen_config={
                "run_time": 4,
                "func": smooth,
                "velocity_factor": 1
            },
            **kwargs,
    ):
        super().__init__(
            slow_factor=slow_factor,
            n_vectors=n_vectors,
            run_time=run_time,
            file_name=file_name,
            # Zoom config
            include_zoom_camera=include_zoom_camera,
            zoom_position=zoom_position,
            # Zoomed display to Full screen config
            scale_zoom_camera_to_full_screen=scale_zoom_camera_to_full_screen,
            scale_zoom_camera_to_full_screen_at=scale_zoom_camera_to_full_screen_at,
            zoom_camera_to_full_screen_config=zoom_camera_to_full_screen_config,
            **kwargs
        )


class ZoomedDisplayToFullScreenWithRestore(ZoomedDisplayToFullScreen):
   def __init__(
           self,
           run_time=120,
           zoom_camera_to_full_screen_config={
               "run_time": 12,
               "func": lambda t: there_and_back_with_pause(t, 1/10),
               # learn more: manimlib/utils/rate_functions.py
               "velocity_factor": 1,
           },
           **kwargs
   ):
       super().__init__(
           run_time=run_time,
           zoom_camera_to_full_screen_config=zoom_camera_to_full_screen_config,
           **kwargs
       )
