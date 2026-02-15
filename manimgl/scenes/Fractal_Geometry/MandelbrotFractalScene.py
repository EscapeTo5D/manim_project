from manimlib import *

script = ['茱莉亚集', '曼德勃罗集', '北斗星', '北极']
ROOT_COLORS_BRIGHT = [RED, GREEN, BLUE, YELLOW, MAROON_B]
ROOT_COLORS_DEEP = ["#440154", "#3b528b", "#21908c", "#5dc963", "#29abca"]
CUBIC_COLORS = [RED_E, TEAL_E, BLUE_E]
MANDELBROT_COLORS = [
    "#00065c",
    "#061e7e",
    "#0c37a0",
    "#205abc",
    "#4287d3",
    "#D9EDE4",
    "#F0F9E4",
    "#BA9F6A",
    "#573706",
]


def get_c_dot_label(dot, get_c, font_size=24, direction=UP):
    c_label = VGroup(
        Tex("c = ", font_size=font_size),
        DecimalNumber(get_c(), font_size=font_size, include_sign=True)
    ).arrange(RIGHT, buff=0.075)
    c_label[0].shift(0.02 * DOWN)
    c_label.set_color(YELLOW)
    c_label.set_stroke(BLACK, 5, background=True)
    c_label.add_updater(lambda m: m.next_to(dot, direction, SMALL_BUFF))
    c_label.add_updater(lambda m: m[1].set_value(get_c()))
    return c_label


def roots_to_coefficients(roots):
    n = len(list(roots))
    return [
        ((-1) ** (n - k)) * sum(
            np.prod(tup)
            for tup in it.combinations(roots, n - k)
        )
        for k in range(n)
    ] + [1]


def poly(x, coefs):
    return sum(coefs[k] * x ** k for k in range(len(coefs)))


def dpoly(x, coefs):
    return sum(k * coefs[k] * x ** (k - 1) for k in range(1, len(coefs)))


def coefs_to_poly_string(coefs):
    n = len(coefs) - 1
    tex_str = "" if coefs[-1] == 1 else str(int(coefs[-1]))
    tex_str += f"z^{{{n}}}"
    for c, k in zip(coefs[-2::-1], it.count(n - 1, -1)):
        if c == 0:
            continue
        if isinstance(c, complex):
            num_str = "({:+}".format(int(c.real))
            num_str += "+ {:+})".format(int(c.imag))
        else:
            num_str = "{:+}".format(int(c))
        if abs(c) == 1 and k > 0:
            num_str = num_str[:-1]
        tex_str += num_str
        if k == 0:
            continue
        elif k == 1:
            tex_str += "z"
        else:
            tex_str += f"z^{{{k}}}"
    return tex_str


def find_root(func, dfunc, seed=complex(1, 1), tol=1e-8, max_steps=100):
    # Use newton's method
    last_seed = np.inf
    for n in range(max_steps):
        if abs(seed - last_seed) < tol:
            break
        last_seed = seed
        seed = seed - func(seed) / dfunc(seed)
    return seed


def coefficients_to_roots(coefs):
    if len(coefs) == 0:
        return []
    elif coefs[-1] == 0:
        return coefficients_to_roots(coefs[:-1])
    roots = []
    # Find a root, divide out by (x - root), repeat
    for i in range(len(coefs) - 1):
        root = find_root(
            lambda x: poly(x, coefs),
            lambda x: dpoly(x, coefs),
        )
        roots.append(root)
        new_reversed_coefs, rem = np.polydiv(coefs[::-1], [1, -root])
        coefs = new_reversed_coefs[::-1]
    return roots


class NewtonFractal(Mobject):
    CONFIG = {
        "shader_folder": "newton_fractal",
        "shader_dtype": [
            ('point', np.float32, (3,)),
        ],
        "colors": ROOT_COLORS_DEEP,
        "coefs": [1.0, -1.0, 1.0, 0.0, 0.0, 1.0],
        "scale_factor": 1.0,
        "offset": ORIGIN,
        "n_steps": 30,
        "julia_highlight": 0.0,
        "max_degree": 5,
        "saturation_factor": 0.0,
        "opacity": 1.0,
        "black_for_cycles": False,
        "is_parameter_space": False,
    }

    def __init__(self, plane, **kwargs):
        super().__init__(
            scale_factor=plane.get_x_unit_size(),
            offset=plane.n2p(0),
            **kwargs,
        )
        self.replace(plane, stretch=True)

    def init_data(self):
        self.data: dict[str, np.ndarray] = {
            "points": np.zeros((0, 3)),
            "bounding_box": np.zeros((3, 3)),
            "rgbas": np.zeros((1, 4)),
        }

    def init_uniforms(self):
        super().init_uniforms()
        self.set_colors(self.colors)
        self.set_julia_highlight(self.julia_highlight)
        self.set_coefs(self.coefs)
        self.set_scale(self.scale_factor)
        self.set_offset(self.offset)
        self.set_n_steps(self.n_steps)
        self.set_saturation_factor(self.saturation_factor)
        self.set_opacity(self.opacity)
        self.uniforms["black_for_cycles"] = float(self.black_for_cycles)
        self.uniforms["is_parameter_space"] = float(self.is_parameter_space)

    def set_colors(self, colors):
        self.uniforms.update({
            f"color{n}": np.array(color_to_rgba(color))
            for n, color in enumerate(colors)
        })
        return self

    def set_julia_highlight(self, value):
        self.uniforms["julia_highlight"] = value

    def set_coefs(self, coefs, reset_roots=True):
        full_coefs = [*coefs] + [0] * (self.max_degree - len(coefs) + 1)
        self.uniforms.update({
            f"coef{n}": np.array([coef.real, coef.imag], dtype=np.float64)
            for n, coef in enumerate(map(complex, full_coefs))
        })
        if reset_roots:
            self.set_roots(coefficients_to_roots(coefs), False)
        self.coefs = coefs
        return self

    def set_roots(self, roots, reset_coefs=True):
        self.uniforms["n_roots"] = float(len(roots))
        full_roots = [*roots] + [0] * (self.max_degree - len(roots))
        self.uniforms.update({
            f"root{n}": np.array([root.real, root.imag], dtype=np.float64)
            for n, root in enumerate(map(complex, full_roots))
        })
        if reset_coefs:
            self.set_coefs(roots_to_coefficients(roots), False)
        self.roots = roots
        return self

    def set_scale(self, scale_factor):
        self.uniforms["scale_factor"] = scale_factor
        return self

    def set_offset(self, offset):
        self.uniforms["offset"] = np.array(offset)
        return self

    def set_n_steps(self, n_steps):
        self.uniforms["n_steps"] = float(n_steps)
        return self

    def set_saturation_factor(self, saturation_factor):
        self.uniforms["saturation_factor"] = float(saturation_factor)
        return self

    def set_opacities(self, *opacities):
        for n, opacity in enumerate(opacities):
            self.uniforms[f"color{n}"][3] = opacity
        return self

    def set_opacity(self, opacity, recurse=True):
        self.set_opacities(*len(self.roots) * [opacity])
        return self


class MandelbrotFractal(NewtonFractal):
    CONFIG = {
        "shader_folder": "mandelbrot_fractal",
        "shader_dtype": [
            ('point', np.float32, (3,)),
        ],
        "scale_factor": 1.0,
        "offset": ORIGIN,
        "colors": MANDELBROT_COLORS,
        "n_colors": 9,
        "parameter": complex(0, 0),
        "n_steps": 300,
        "mandelbrot": True,
    }

    def init_data(self):
        self.data: dict[str, np.ndarray] = {
            "points": np.zeros((0, 3)),
            "bounding_box": np.zeros((3, 3)),
            "rgbas": np.zeros((1, 4)),
        }
        self.set_points([UL, DL, UR, DR])

    def init_uniforms(self):
        Mobject.init_uniforms(self)
        self.uniforms["mandelbrot"] = float(self.mandelbrot)
        self.set_parameter(self.parameter)
        self.set_opacity(self.opacity)
        self.set_scale(self.scale_factor)
        self.set_colors(self.colors)
        self.set_offset(self.offset)
        self.set_n_steps(self.n_steps)

    def set_parameter(self, c):
        self.uniforms["parameter"] = np.array([c.real, c.imag])
        return self

    def set_opacity(self, opacity):
        self.uniforms["opacity"] = opacity
        return self

    def set_colors(self, colors):
        for n in range(len(colors)):
            self.uniforms[f"color{n}"] = color_to_rgb(colors[n])
        return self


class JuliaFractal(MandelbrotFractal):
    CONFIG = {
        "n_steps": 100,
        "mandelbrot": False,
    }

    def set_c(self, c):
        self.set_parameter(c)


class MandelbrotIntro(Scene):
    n_iterations = 30

    def construct(self):
        self.add_process_description()
        self.add_plane()
        self.show_iterations()
        self.add_mandelbrot_image()

    def add_process_description(self):
        kw = {
            "tex_to_color_map": {
                "{c}": YELLOW,
            }
        }
        terms = self.terms = VGroup(
            Tex("z_{n + 1} = z_n^2 + {c}", **kw),
            Tex("{c} \\text{ can be changed}", **kw),
            Tex("z_0 = 0", **kw),
        )
        terms.arrange(DOWN, buff=MED_LARGE_BUFF, aligned_edge=LEFT)
        terms.to_corner(UL)

        equation = Tex("f(z) = z^2 + c")
        equation.to_edge(UP)

        self.process_terms = terms
        self.add(equation)
        self.wait()
        self.play(FadeTransform(equation, terms[0]))

    def add_plane(self):
        plane = self.plane = ComplexPlane((-2, 1), (-2, 2))
        plane.set_height(4)
        plane.set_height(1.5 * FRAME_HEIGHT)
        plane.next_to(2 * LEFT, RIGHT, buff=0)
        plane.add_coordinate_labels(font_size=24)
        self.add(plane)

    def show_iterations(self):
        plane = self.plane

        # c0 = complex(-0.2, 0.95)
        c0 = complex(-0.6, 0.4)

        c_dot = self.c_dot = Dot()
        c_dot.set_fill(YELLOW)
        c_dot.set_stroke(BLACK, 5, background=True)
        c_dot.move_to(plane.n2p(c0))
        c_dot.add_updater(lambda m: m)  # Null

        n_iter_tracker = ValueTracker(1)

        def get_n_iters():
            return int(n_iter_tracker.get_value())

        def get_c():
            return plane.p2n(c_dot.get_center())

        def update_lines(lines):
            z1 = 0
            c = get_c()
            new_lines = []

            for n in range(get_n_iters()):
                try:
                    z2 = z1 ** 2 + c
                    new_lines.append(Line(
                        plane.n2p(z1),
                        plane.n2p(z2),
                        stroke_color=GREY,
                        stroke_width=2,
                    ))
                    new_lines.append(Dot(
                        plane.n2p(z2),
                        fill_color=YELLOW,
                        fill_opacity=0.5,
                        radius=0.05,
                    ))
                    z1 = z2
                except Exception:
                    pass

            lines.set_submobjects(new_lines)

        c_label = get_c_dot_label(c_dot, get_c)

        lines = VGroup()
        lines.set_stroke(background=True)
        lines.add_updater(update_lines)
        self.add(lines, c_dot, c_label)

        def increase_step(run_time=1.0):
            n_iter_tracker.increment_value(1)
            lines.update()
            lines.suspend_updating()
            self.add(*lines, c_dot, c_label)
            self.play(
                ShowCreation(lines[-2]),
                TransformFromCopy(lines[-3], lines[-1]),
                run_time=run_time
            )
            self.add(lines, c_dot, c_label)
            lines.resume_updating()

        kw = {
            "tex_to_color_map": {
                "c": YELLOW,
            }
        }
        new_lines = VGroup(
            Tex("z_1 = 0^2 + c = c", **kw),
            Tex("z_2 = c^2 + c", **kw),
            Tex("z_3 = (c^2 + c)^2 + c", **kw),
            Tex("z_4 = ((c^2 + c)^2 + c)^2 + c", **kw),
            Tex("\\vdots", **kw),
        )
        new_lines.arrange(DOWN, aligned_edge=LEFT)
        new_lines[-2].scale(0.8, about_edge=LEFT)
        new_lines.next_to(self.process_terms[2], DOWN, aligned_edge=LEFT)
        new_lines[-1].match_x(new_lines[-2][0][2])

        # Show c
        self.wait()
        self.play(Write(self.process_terms[1]))
        self.wait(10)

        # Show first step
        dot = Dot(plane.n2p(0))
        self.play(FadeIn(self.process_terms[2], 0.5 * DOWN))
        self.play(FadeIn(dot, scale=0.2, run_time=2))
        self.play(FadeOut(dot))

        self.play(FadeIn(new_lines[0], 0.5 * DOWN))
        self.play(ShowCreationThenFadeOut(
            lines[0].copy().set_stroke(BLUE, 5)
        ))
        self.wait(3)

        # Show second step
        self.play(FadeIn(new_lines[1], 0.5 * DOWN))
        increase_step()
        self.wait(10)

        # Show 3rd to nth steps
        self.play(FadeIn(new_lines[2], 0.5 * DOWN))
        increase_step()
        self.play(FadeIn(new_lines[3], 0.5 * DOWN))
        increase_step()
        self.wait(5)
        self.play(FadeIn(new_lines[4]))
        for n in range(self.n_iterations):
            increase_step(run_time=0.25)

        # Play around
        self.wait(15)

    def add_mandelbrot_image(self):
        mandelbrot_set = MandelbrotFractal(self.plane)

        self.add(mandelbrot_set, *self.mobjects)
        self.play(
            FadeIn(mandelbrot_set, run_time=2),
            # self.plane.animate.set_opacity(0.5)
            self.plane.animate.set_stroke(WHITE, opacity=0.25)
        )

    # Listeners
    def on_mouse_motion(self, point, d_point):
        super().on_mouse_motion(point, d_point)
        if self.window.is_key_pressed(ord(" ")):
            self.c_dot.move_to(point)


class MandelbrotSetPreview(Scene):
    def construct(self):
        plane = ComplexPlane(
            (-2, 1), (-2, 2),
            background_line_style={
                "stroke_color": GREY_B,
                "stroke_opacity": 0.5,
            }
        )
        plane.set_width(0.7 * FRAME_WIDTH)
        plane.axes.set_stroke(opacity=0.5)
        plane.add_coordinate_labels(font_size=18)

        mandelbrot = MandelbrotFractal(plane)
        mandelbrot.set_n_steps(0)

        self.add(mandelbrot, plane)
        self.play(
            mandelbrot.animate.set_n_steps(600),
            rate_func=lambda a: a ** 3,
            run_time=10,
        )
        self.wait()


class ClassicJuliaSetDemo(MandelbrotIntro):
    def construct(self):

        # Init planes
        kw = {
            "background_line_style": {
                "stroke_width": 0.5,
            }
        }
        planes = VGroup(
            ComplexPlane((-2, 2), (-2, 2), **kw),
            ComplexPlane((-2, 2), (-2, 2), **kw),
        )
        for plane, corner in zip(planes, [DL, DR]):
            plane.set_stroke(WHITE, opacity=0.5)
            plane.set_height(6.5)
            plane.to_corner(corner, buff=MED_SMALL_BUFF)
            plane.to_edge(DOWN, MED_LARGE_BUFF)

        planes[1].add_coordinate_labels(font_size=18)
        planes[0].add_coordinate_labels(font_size=18)
        # planes[0].add_coordinate_labels(
        #     (-1, 0, 1, 1j, -1j),
        #     font_size=18
        # )

        # Init fractals
        mandelbrot = MandelbrotFractal(planes[0])
        julia = JuliaFractal(planes[1])
        fractals = Group(mandelbrot, julia)

        self.add(*fractals, *planes)
        R = 0.25

        # Add c_dot 茱莉亚集
        c_dot = self.c_dot = Dot(radius=0.04)
        c_dot.set_fill(YELLOW, 1)

        cardioid1 = ParametricCurve(
            lambda t: planes[0].c2p(
                2 * R * math.cos(t) - R * math.cos(2 * t),
                2 * R * math.sin(t) - R * math.sin(2 * t),
            ),
            t_range=(0, TAU)
        )

        cardioid2 = ParametricCurve(
            lambda t: planes[1].c2p(
                2 * R * math.cos(t) - R * math.cos(2 * t),
                2 * R * math.sin(t) - R * math.sin(2 * t),
            ),
            t_range=(0, TAU)
        )

        def get_c():
            return planes[0].p2n(c_dot.get_center())

        t_tracker = ValueTracker(0)
        get_t = t_tracker.get_value
        # c_dot.move_to(planes[0].c2p(1.76, -0.31))
        c_dot.add_updater(lambda m: m.move_to(cardioid1.pfp(get_t())))
        # c_dot.add_updater(lambda m: m)

        c_label = get_c_dot_label(c_dot, get_c, direction=UR)
        julia.add_updater(lambda m: m.set_c(
            plane.p2n(cardioid2.pfp(get_t()))
        ))
        # julia.add_updater(lambda m: m.set_c(get_c()))
        self.add(c_dot, c_label)

        # Add labels
        kw = {
            "tex_to_color_map": {
                "{z_0}": GREY_A,
                "{c}": YELLOW,
                "\\text{Pixel}": BLUE_D,
            },
        }

        space_labels = VGroup(
            Tex("{c}\\text{-space}", **kw),
            Tex("{z_0}\\text{-space}", **kw),
        )
        text_labels = Group(
            Text(script[1], font='KaiTi').set_color_by_gradient(PURPLE_E, GREEN_E),
            Text(script[0], font='KaiTi').set_color_by_gradient(PURPLE_E, GREEN_E))
        for text, label, plane in zip(text_labels,space_labels, planes):
            label.scale(0.5)
            text.scale(0.6)
            label.move_to(plane, UL).shift(SMALL_BUFF * DR)
            text.next_to(label, 0.5*RIGHT).shift(0.02 * UR)
        self.add(space_labels,text_labels)
        self.play(
            t_tracker.animate.set_value(1),
            rate_func=linear,
            run_time=10
        )
        # Animations
        # self.wait(2)


class MandelbrotStill(Scene):
    def construct(self):
        plane = ComplexPlane((-3, 2), (-1.3, 1.3))
        plane.set_height(FRAME_HEIGHT)
        fractal = MandelbrotFractal(plane)
        self.add(fractal)
        # self.wait()


class JuliaStill(Scene):
    def construct(self):
        plane = ComplexPlane((-4, 4), (-1.5, 1.5))
        plane.set_height(FRAME_HEIGHT)
        fractal = JuliaFractal(plane)
        fractal.set_c(-0.03 + 0.74j)
        fractal.set_n_steps(100)
        self.add(fractal)
        # self.wait()


class TwoToMillionPoints(Scene):
    c = -0.18 + 0.77j
    plane_height = 7

    def construct(self):
        plane, julia_fractal = self.get_plane_and_fractal()

        words = TexText("$\\approx 2^{1{,}000{,}000}$ solutions!")
        words.set_stroke(BLACK, 8, background=True)
        words.move_to(plane, UL)
        words.shift(MED_SMALL_BUFF * DR)

        points = self.get_julia_set_points(plane, 100000, 1000)
        dots = DotCloud(points)
        dots.set_color(YELLOW)
        dots.set_opacity(1)
        dots.set_radius(0.025)
        dots.add_updater(lambda m: m)
        dots.make_3d()

        self.add(julia_fractal, plane, words)
        self.play(ShowCreation(dots, run_time=10))

    def get_plane_and_fractal(self):
        plane = ComplexPlane((-2, 2), (-2, 2))
        plane.set_height(self.plane_height)
        fractal = JuliaFractal(plane)
        fractal.set_c(self.c)
        return plane, fractal

    def get_julia_set_points(self, plane, n_points, n_steps):
        values = np.array([
            complex(math.cos(x), math.sin(x))
            for x in np.linspace(0, TAU, n_points)
        ])

        c = self.c
        for n in range(n_steps):
            units = -1 + 2 * np.random.randint(0, 2, len(values))
            values[:] = (units * np.sqrt(values[:])) - c
        values += c

        return np.array(list(map(plane.n2p, values)))


class MentionFatouSetsAndJuliaSets(Scene):
    colors = [RED_E, BLUE_E, TEAL_E, MAROON_E]

    def construct(self):
        # Introduce terms
        f_group, j_group = self.get_fractals()
        f_name, j_name = VGroup(
            Text("Fatou set"),
            Text("Julia set"),
        )
        f_name.next_to(f_group, UP, MED_LARGE_BUFF)
        j_name.next_to(j_group, UP, MED_LARGE_BUFF)

        self.play(
            Write(j_name),
            GrowFromCenter(j_group)
        )
        self.wait()
        self.play(
            Write(f_name),
            *map(GrowFromCenter, f_group)
        )
        self.wait()

        # Define Fatou set
        fatou_condition = self.get_fatou_condition()
        fatou_condition.set_width(FRAME_WIDTH - 1)
        fatou_condition.center().to_edge(UP, buff=1.0)
        lhs, arrow, rhs = fatou_condition
        f_line = Line(LEFT, RIGHT)
        f_line.match_width(fatou_condition)
        f_line.next_to(fatou_condition, DOWN)
        f_line.set_stroke(WHITE, 1)

        self.play(
            FadeOut(j_name, RIGHT),
            FadeOut(j_group, RIGHT),
            Write(lhs)
        )
        self.wait()
        for words in lhs[-1]:
            self.play(FlashUnder(
                words,
                buff=0,
                time_width=1.5
            ))
        self.play(Write(arrow))
        self.play(LaggedStart(
            FadeTransform(f_name.copy(), rhs[1][:8]),
            FadeIn(rhs),
            lag_ratio=0.5
        ))
        self.wait()

        # Show Julia set
        otherwise = Text("Otherwise...")
        otherwise.next_to(rhs, DOWN, LARGE_BUFF)
        j_condition = TexText("$z_0 \\in$", " Julia set", " of $f$")
        j_condition.match_height(rhs)
        j_condition.next_to(otherwise, DOWN, LARGE_BUFF)

        j_group.set_height(4.0)
        j_group.to_edge(DOWN)
        j_group.set_x(-1.0)
        j_name = j_condition.get_part_by_tex("Julia set")
        j_underline = Underline(j_name, buff=0.05)
        j_underline.set_color(YELLOW)
        arrow = Arrow(
            j_name.get_bottom(),
            j_group.get_right(),
            path_arc=-45 * DEGREES,
        )
        arrow.set_stroke(YELLOW, 5)

        julia_set = j_group[0]
        julia_set.update()
        julia_set.suspend_updating()
        julia_copy = julia_set.copy()
        julia_copy.clear_updaters()
        julia_copy.set_colors(self.colors)
        julia_copy.set_julia_highlight(0)

        mover = f_group[:-4]
        mover.generate_target()
        mover.target.match_width(rhs)
        mover.target.next_to(rhs, UP, MED_LARGE_BUFF)
        mover.target.shift_onto_screen(buff=SMALL_BUFF)

        self.play(
            ShowCreation(f_line),
            FadeOut(f_name),
            MoveToTarget(mover),
        )
        self.play(
            Write(otherwise),
            FadeIn(j_condition, 0.5 * DOWN)
        )
        self.wait()
        self.play(
            ShowCreation(j_underline),
            ShowCreation(arrow),
            FadeIn(j_group[1]),
            FadeIn(julia_copy)
        )
        self.play(
            GrowFromPoint(julia_set, julia_set.get_corner(UL), run_time=2),
            julia_copy.animate.set_opacity(0.2)
        )
        self.wait()

    def get_fractals(self, jy=1.5, fy=-2.5):
        coefs = roots_to_coefficients([-1.5, 1.5, 1j, -1j])
        n = len(coefs) - 1
        colors = self.colors
        f_planes = VGroup(*(self.get_plane() for x in range(n)))
        f_planes.arrange(RIGHT, buff=LARGE_BUFF)
        plusses = Tex("+").replicate(n - 1)
        f_group = Group(*it.chain(*zip(f_planes, plusses)))
        f_group.add(f_planes[-1])
        f_group.arrange(RIGHT)
        fatou = Group(*(
            NewtonFractal(f_plane, coefs=coefs, colors=colors)
            for f_plane in f_planes
        ))
        for i, fractal in enumerate(fatou):
            opacities = n * [0.2]
            opacities[i] = 1
            fractal.set_opacities(*opacities)
        f_group.add(*fatou)
        f_group.set_y(fy)

        j_plane = self.get_plane()
        j_plane.set_y(jy)
        julia = NewtonFractal(j_plane, coefs=coefs, colors=5 * [GREY_A])
        julia.set_julia_highlight(1e-3)
        j_group = Group(julia, j_plane)

        for fractal, plane in zip((*fatou, julia), (*f_planes, j_plane)):
            fractal.plane = plane
            fractal.add_updater(
                lambda m: m.set_offset(
                    m.plane.get_center()
                ).set_scale(
                    m.plane.get_x_unit_size()
                ).replace(m.plane)
            )

        fractals = Group(f_group, j_group)
        return fractals

    def get_plane(self):
        plane = ComplexPlane(
            (-2, 2), (-2, 2),
            background_line_style={"stroke_width": 1, "stroke_color": GREY}
        )
        plane.set_height(2)
        plane.set_opacity(0)
        box = SurroundingRectangle(plane, buff=0)
        box.set_stroke(WHITE, 1)
        plane.add(box)
        return plane

    def get_fatou_condition(self):
        zn = Tex(
            "z_0", "\\overset{f}{\\longrightarrow}",
            "z_1", "\\overset{f}{\\longrightarrow}",
            "z_2", "\\overset{f}{\\longrightarrow}",
            "\\dots",
            "\\longrightarrow"
        )
        words = VGroup(
            TexText("Stable fixed point"),
            TexText("Stable cycle"),
            TexText("$\\infty$"),
        )
        words.arrange(DOWN, aligned_edge=LEFT)
        brace = Brace(words, LEFT)
        zn.next_to(brace, LEFT)
        lhs = VGroup(zn, brace, words)

        arrow = Tex("\\Rightarrow")
        arrow.scale(2)
        arrow.next_to(lhs, RIGHT, MED_LARGE_BUFF)
        rhs = Tex("z_0 \\in", " \\text{Fatou set of $f$}")
        rhs.next_to(arrow, RIGHT, buff=MED_LARGE_BUFF)

        result = VGroup(lhs, arrow, rhs)

        return result


class ShowJuliaSetPoint(TwoToMillionPoints):
    plane_height = 14
    show_disk = False
    n_steps = 60
    disk_radius = 0.02

    def construct(self):
        # Background
        plane, fractal = self.get_plane_and_fractal()

        plane.add_coordinate_labels(font_size=24)
        for mob in plane.family_members_with_points():
            if isinstance(mob, Line):
                mob.set_stroke(opacity=0.5 * mob.get_stroke_opacity())
        self.add(fractal, plane)

        # Points
        points = list(self.get_julia_set_points(plane, n_points=1, n_steps=1000))

        def func(p):
            z = plane.p2n(p)
            return plane.n2p(z ** 2 + self.c)

        for n in range(100):
            points.append(func(points[-1]))

        dot = Dot(points[0])
        dot.set_color(YELLOW)

        self.add(dot)

        if self.show_disk:
            dot.scale(0.5)
            disk = dot.copy()
            disk.insert_n_curves(10000)
            disk.set_height(plane.get_x_unit_size() * self.disk_radius)
            disk.set_fill(YELLOW, 0.25)
            disk.set_stroke(YELLOW, 2, 1)
            self.add(disk, dot)

        frame = self.camera.frame
        path_arc = 30 * DEGREES
        point = dot.get_center().copy()
        for n in range(self.n_steps):
            new_point = func(point)
            arrow = Arrow(point, new_point, path_arc=path_arc, buff=0)
            arrow.set_stroke(WHITE, opacity=0.9)
            self.add(dot.copy().set_opacity(0.5))
            anims = []
            if self.show_disk:
                disk.generate_target()
                disk.target.apply_function(func)
                disk.target.make_smooth()
                anims.append(MoveToTarget(disk, path_arc=path_arc))
                if disk.target.get_height() > frame.get_height():
                    anims.extend([
                        mob.animate.scale(2.0)
                        for mob in [frame, fractal]
                    ])
            self.play(
                ApplyMethod(dot.move_to, new_point, path_arc=path_arc),
                ShowCreation(arrow),
                *anims,
            )
            self.play(FadeOut(arrow))
            point = new_point


class ShowFatouDiskExample(Scene):
    disk_radius = 0.1
    n_steps = 14

    def construct(self):
        c = -1.06 + 0.11j
        plane = ComplexPlane((-3, 3), (-2, 2))
        for line in plane.family_members_with_points():
            line.set_stroke(opacity=0.5 * line.get_stroke_opacity())
        plane.set_height(1.8 * FRAME_HEIGHT)
        plane.add_coordinate_labels(font_size=18)
        fractal = JuliaFractal(plane, parameter=c)

        # z0 = -1.1 + 0.1j
        z0 = -0.3 + 0.2j

        dot = Dot(plane.n2p(z0), radius=0.025)
        dot.set_fill(YELLOW)

        disk = dot.copy()
        disk.set_height(2 * self.disk_radius * plane.get_x_unit_size())
        disk.set_fill(YELLOW, 0.5)
        disk.set_stroke(YELLOW, 1.0)
        disk.insert_n_curves(1000)

        def func(point):
            return plane.n2p(plane.p2n(point) ** 2 + c)

        self.add(fractal, plane)
        self.add(disk, dot)
        self.play(DrawBorderThenFill(disk))

        path_arc = 10 * DEGREES
        for n in range(self.n_steps):
            point = dot.get_center()
            new_point = func(point)
            arrow = Arrow(point, new_point, path_arc=path_arc, buff=0.1)
            self.play(
                dot.animate.move_to(new_point),
                disk.animate.apply_function(func),
                ShowCreation(arrow),
                path_arc=path_arc,
            )
            self.play(FadeOut(arrow))

        self.embed()


class DescribeChaos(Scene):
    def construct(self):
        j_point = 3 * LEFT
        j_value = -0.56554 - 0.29968j

        plane = ComplexPlane((-3, 3), (-2, 2))
        plane.scale(1000)
        plane.shift(j_point - plane.n2p(j_value))
        fractal = MandelbrotFractal(plane)
        # fractal.set_c(-0.5 + 0.5j)
        self.add(fractal, plane)

        # for dot in surrounding_dots:
        #     dot.shift(0.1 * (random.random() - 0.5))

        frame = self.camera.frame
        frame.save_state()
        frame.replace(plane)
        self.play(Restore(frame, run_time=5))
        self.wait()


class AmbientJulia(Scene):
    def construct(self):
        plane = ComplexPlane(
            (-4, 4), (-2, 2),
            background_line_style={
                "stroke_color": GREY_A,
                "stroke_width": 1,
            }
        )
        plane.axes.set_stroke(width=1, opacity=0.5)
        plane.set_height(14)
        fractal = JuliaFractal(plane)
        fractal.set_n_steps(100)

        R = 0.25
        cardioid = ParametricCurve(
            lambda t: plane.c2p(
                2 * R * math.cos(t) - R * math.cos(2 * t),
                2 * R * math.sin(t) - R * math.sin(2 * t),
            ),
            t_range=(0, TAU)
        )

        t_tracker = ValueTracker(0)
        get_t = t_tracker.get_value

        fractal.add_updater(lambda m: m.set_c(
            plane.p2n(cardioid.pfp(get_t()))
        ))

        self.add(fractal, plane)
        self.play(
            t_tracker.animate.set_value(1),
            rate_func=linear,
            run_time=40
        )
