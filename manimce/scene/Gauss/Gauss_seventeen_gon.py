import math
from numpy import *
from manimlib import *
script = [
    "高斯十七边形"
]
get_angle = lambda c: np.angle(-c) + PI if not c / abs(c) == 1 else 0
convert_angle = lambda a: a if a >= 0 else a + TAU
colors = [
    "#FF0000",  # Red
    "#00FF00",  # Green
    "#0000FF",  # Blue
    "#FFFF00",  # Yellow
    "#FF00FF",  # Magenta
    "#00FFFF",  # Cyan
    "#800000",  # Maroon
    "#808000",  # Olive
    "#008000",  # Dark Green
    "#800080",  # Purple
    "#808080",  # Gray
    "#C0C0C0",  # Silver
    "#FFA500",  # Orange
    "#A52A2A",  # Brown
    "#8B4513",  # Saddle Brown
    "#FFD700",  # Gold
    "#4B0082"  # Indigo
]


def rotate_point_around_another(point, center):
    """
    计算一个点围绕另一个点旋转后的坐标。

    :param point: 原始点的坐标，形如 (x, y, z)
    :param center: 旋转中心的坐标，形如 (x, y, z)
    :return: 旋转后的点的坐标，形如 (x, y, z)
    """
    # 将点平移到以中心为原点的坐标系中
    translated_point = point - center
    agl = 11 * PI / 34
    angle = 2 * agl

    # 旋转矩阵
    rotation_matrix = np.array([
        [np.cos(angle), -np.sin(angle), 0],
        [np.sin(angle), np.cos(angle), 0],
        [0, 0, 1]
    ])

    # 对平移后的点应用旋转矩阵
    rotated_translated_point = rotation_matrix @ translated_point

    # 将旋转后的点平移回原始坐标系中
    rotated_point = rotated_translated_point + center

    return rotated_point


class Compass(VGroup):
    CONFIG = {
        'stroke_color': GREY_E,
        'fill_color': WHITE,
        'stroke_width': 2,
        'leg_length': 3,
        'leg_width': 0.12,
        'r': 0.2,
        'depth_test': True,
    }

    def __init__(self, span=2.5, **kwargs):
        VGroup.__init__(self, **kwargs)
        self.span = span
        self.create_compass()

    def create_compass(self):
        s, l, r, w = self.span, self.leg_length, self.r, self.leg_width
        self.theta = np.arcsin(s / 2 / l)

        self.c = Circle(radius=r, fill_color=self.fill_color, fill_opacity=1, stroke_color=self.stroke_color,
                        stroke_width=self.stroke_width * 5)
        c2 = Circle(radius=r + self.stroke_width * 5 / 100 / 2, fill_opacity=0, stroke_color=self.fill_color,
                    stroke_width=self.stroke_width)

        self.leg_1 = Polygon(ORIGIN, l * RIGHT, (l - w * np.sqrt(3)) * RIGHT + w * DOWN, w * DOWN,
                             stroke_width=0, stroke_color=self.fill_color, fill_color=self.stroke_color,
                             fill_opacity=1).rotate(-PI / 2 - self.theta, about_point=self.c.get_center())
        self.leg_2 = Polygon(ORIGIN, l * RIGHT, (l - w * np.sqrt(3)) * RIGHT + w * UP, w * UP,
                             stroke_width=0, stroke_color=self.fill_color, fill_color=self.stroke_color,
                             fill_opacity=1).rotate(-PI / 2 + self.theta, about_point=self.c.get_center())

        # self.leg_1, self.leg_2 = VGroup(leg_01, leg_11),  VGroup(leg_02, leg_12, pen_point)
        h = Line(UP * r, UP * (r + r * 1.8), stroke_color=self.stroke_color, stroke_width=self.stroke_width * 6)

        self.head = VGroup(h, self.c, c2)
        self.add(self.leg_1, self.leg_2, self.head)
        self.move_to(ORIGIN)

        return self

    def get_niddle_tip(self):
        return self.leg_1.get_vertices()[1]

    def get_pen_tip(self):
        return self.leg_2.get_vertices()[1]

    def move_niddle_tip_to(self, pos):
        self.shift(pos - self.get_niddle_tip())
        return self

    def rotate_about_niddle_tip(self, angle=PI / 2):
        self.rotate(angle=angle, about_point=self.get_niddle_tip())

    def get_span(self):
        # return self.span 如果进行了缩放而self.span没变会有问题
        return get_norm(self.get_pen_tip() - self.get_niddle_tip())

    def set_span(self, s):
        self.span = s
        l, r, w = self.leg_length, self.r, self.leg_width
        theta_new, theta_old = np.arcsin(s / 2 / l), self.theta
        sign = np.sign(
            get_angle(R3_to_complex(self.leg_2.get_vertices()[1] - self.leg_2.get_vertices()[0])) - get_angle(
                R3_to_complex(self.leg_1.get_vertices()[1] - self.leg_1.get_vertices()[0])))
        rotate_angle = 2 * (theta_new - theta_old) * sign
        self.leg_2.rotate(rotate_angle, about_point=self.c.get_center())
        self.theta = theta_new
        self.head.rotate(rotate_angle / 2, about_point=self.c.get_center())
        self.rotate_about_niddle_tip(-rotate_angle / 2)
        return self

    def set_compass(self, center, pen_tip):
        self.move_niddle_tip_to(center)
        self.set_span(get_norm(pen_tip - center))
        self.rotate_about_niddle_tip(
            np.angle(R3_to_complex(pen_tip - center)) - np.angle(R3_to_complex(self.get_pen_tip() - center)))
        return self

    def set_compass_to_draw_arc(self, arc):
        return self.set_compass(arc.arc_center, arc.get_start())

    def reverse_tip(self):
        return self.flip(axis=self.head[0].get_end() - self.head[0].get_start(), about_point=self.c.get_center())


class DrawingScene(Scene):
    CONFIG = {
        'compass_config': {
            'stroke_color': GREY_E,
            'fill_color': WHITE,
            'stroke_width': 2,
            'leg_length': 3,
            'leg_width': 0.12,
            'r': 0.2,
            'depth_test': True,
        },
        'ruler_config': {
            'width': 10,
            'height': 0.8,
            'stroke_width': 8,
            'stroke_color': GREY_E,
            'stroke_opacity': 0.4,
            'fill_color': WHITE,
            'fill_opacity': 0.5,
        },
        'dot_config': {
            'radius': 0.06,
            'color': GREY_E,
        },
        'line_config': {
            'stroke_color': '#FFFF00',
            'stroke_width': 1.8,
        },
        'arc_config': {
            'stroke_color': LIGHT_PINK,
            'stroke_width': 1.8,
        },
        'brace_config': {
            'fill_color': GREY_E,
            'buff': 0.025,
        },
        'text_config': {
            'size': 0.6 * 5,  # 5 times than the actual size and the sacle down
            'font': 'Cambria Math',
            'color': GREY_E,
        },
        'add_ruler': False,
    }

    def setup(self):
        self.cp = Compass(**self.compass_config)
        self.ruler = VGroup(
            Rectangle(**self.ruler_config)
            .set_fill(YELLOW, opacity=self.ruler_config['fill_opacity'])  # 设置为红色
            .set_height(self.ruler_config['height'] - self.ruler_config['stroke_width'] / 2 / 100, stretch=True)
            .round_corners(self.ruler_config['height'] / 8),
            Rectangle(**self.ruler_config).set_opacity(0)
        )

        self.dot = Dot(**self.dot_config)

        self.cp.move_to(UP * 10)
        if self.add_ruler:
            self.ruler.move_to(DOWN * 10)
            self.add(self.ruler)
        self.add(self.cp)

        self.temp_points = []

    def construct(self):

        self.add(self.cp)
        self.play(self.cp.move_niddle_tip_to, ORIGIN, run_time=1)
        self.wait(0.3)
        self.set_span(3.6, run_time=1, rate_func=smooth)
        self.wait(0.5)
        self.set_compass(DL * 0.5, UR * 0.5, run_time=1, rate_func=there_and_back)
        arc = Arc(color=GREY_E)
        self.set_compass_to_draw_arc(arc)
        self.draw_arc_by_compass(arc)

        self.wait()

    def set_span(self, s, run_time=1, rate_func=smooth):

        s_old = self.cp.get_span()
        n = int(run_time * self.camera.frame_rate)
        dt = 1 / self.camera.frame_rate
        t_series = np.linspace(1, n, n) / n
        # s_series = s_old + rate_func(t_series) * (s - s_old)
        s_series = [s_old + rate_func(t_series[i]) * (s - s_old) for i in range(n)]
        for i in range(n):
            self.cp.set_span(s_series[i])
            self.wait(dt)

    def set_compass_direction(self, start, end, run_time=1, rate_func=smooth):
        vect = end - start
        a = np.angle(R3_to_complex(vect))
        c_old, p_old = self.cp.get_niddle_tip(), self.cp.get_pen_tip()
        a_old = np.angle(R3_to_complex(p_old - c_old))
        n = int(run_time * self.camera.frame_rate)
        dt = 1 / self.camera.frame_rate
        t_series = np.linspace(1, n, n) / n
        c_series = [c_old + rate_func(t_series[i]) * (start - c_old) for i in range(n)]
        delta_a = (a - a_old) / n
        for i in range(n):
            self.bring_to_front(self.cp)
            self.cp.move_niddle_tip_to(c_series[i])
            self.cp.rotate_about_niddle_tip(delta_a)
            self.wait(dt)

    def set_compass(self, center, pen_tip, run_time=1, rate_func=smooth, emphasize_dot=False):
        if emphasize_dot:
            run_time -= 0.15
        c_old, p_old = self.cp.get_niddle_tip(), self.cp.get_pen_tip()
        n = int(run_time * self.camera.frame_rate)
        dt = 1 / self.camera.frame_rate
        t_series = np.linspace(1, n, n) / n
        # s_series = s_old + rate_func(t_series) * (s - s_old)
        c_series = [c_old + rate_func(t_series[i]) * (center - c_old) for i in range(n)]
        p_series = [p_old + rate_func(t_series[i]) * (pen_tip - p_old) for i in range(n)]

        for i in range(n):
            self.bring_to_front(self.cp)
            self.cp.set_compass(c_series[i], p_series[i])
            self.wait(dt)
        if emphasize_dot:
            self.emphasize_dot([center, pen_tip], run_time=0.15)

    def set_compass_(self, center, pen_tip, adjust_angle=0, run_time=1, rate_func=smooth, emphasize_dot=False):

        vect = center - pen_tip
        a = np.angle(R3_to_complex(vect)) + adjust_angle
        s = get_norm(vect)
        c_old, p_old, s_old = self.cp.get_niddle_tip(), self.cp.get_pen_tip(), self.cp.get_span()
        a_old = np.angle(R3_to_complex(p_old - c_old))
        if emphasize_dot:
            run_time -= 0.15
        n = int(run_time * self.camera.frame_rate)
        dt = 1 / self.camera.frame_rate
        t_series = np.linspace(1, n, n) / n
        c_series = [c_old + rate_func(t_series[i]) * (center - c_old) for i in range(n)]
        delta_a = (a - a_old) / n
        s_series = [s_old + rate_func(t_series[i]) * (s - s_old) for i in range(n)]

        for i in range(n):
            self.bring_to_front(self.cp)
            self.cp.move_niddle_tip_to(c_series[i])
            self.cp.rotate_about_niddle_tip(delta_a)
            self.cp.set_span(s_series[i])
            self.wait(dt)
        if emphasize_dot:
            self.emphasize_dot([center, pen_tip], run_time=0.15)

    def set_compass_to_draw_arc(self, arc, **kwargs):
        self.set_compass(arc.arc_center, arc.get_start(), **kwargs)

    def set_compass_to_draw_arc_(self, arc, **kwargs):
        self.set_compass_(arc.arc_center, arc.get_start(), **kwargs)

    def draw_arc_by_compass(self, arc, is_prepared=True, run_time=1, rate_func=smooth, reverse=False, add_center=False,
                            **kwargs):
        self.bring_to_front(self.cp)
        if not is_prepared: self.set_compass_to_draw_arc(arc, run_time=0.5)
        theta = arc.angle if not reverse else -1 * arc.angle
        self.play(Rotating(self.cp, angle=theta, about_point=self.cp.get_niddle_tip()), ShowCreation(arc),
                  rate_func=rate_func, run_time=run_time)
        if add_center:
            d = Dot(self.cp.get_niddle_tip(), **self.dot_config).scale(0.5)
            self.temp_points.append(d)
            self.add(d)

    def emphasize_dot(self, pos, add_dot=False, size=1.2, run_time=0.2, **kwargs):
        if type(pos) == list:
            d = VGroup(
                *[Dot(pos[i], radius=size / 2, color=GREY_C, fill_opacity=0.25).scale(0.25) for i in range(len(pos))])
        else:
            d = Dot(pos, radius=size / 2, color=GREY_C, fill_opacity=0.25).scale(0.25)
        self.add(d)
        if type(pos) == list:
            self.play(d[0].scale, 4, d[1].scale, 4, rate_func=linear, run_time=run_time)

        else:
            self.play(d.scale, 4, rate_func=linear, run_time=run_time)

        self.remove(d)
        if add_dot:
            if type(pos) == list:
                dot = VGroup(*[Dot(pos[i], **kwargs) for i in range(len(pos))])
            else:
                dot = Dot(pos, **kwargs)
            self.add(dot)
            return dot

    def set_ruler(self, pos1, pos2, run_time=1, rate_func=smooth):
        p1, p2 = self.ruler[-1].get_vertices()[1], self.ruler[-1].get_vertices()[0]
        c12 = (p1 + p2) / 2
        center = (pos1 + pos2) / 2
        self.bring_to_front(self.ruler)
        self.play(self.ruler.shift, center - c12, run_time=run_time / 2, rate_func=rate_func)
        self.play(Rotating(self.ruler, angle=np.angle(R3_to_complex(pos2 - pos1)) - np.angle(R3_to_complex(p2 - p1)),
                           about_point=center), run_time=run_time / 2, rate_func=rate_func)

    def draw_line(self, pos1, pos2, is_prepared=True, run_time=1.2, rate_func=smooth, pre_time=0.8):
        if not is_prepared: self.set_ruler(pos1, pos2, run_time=pre_time)
        self.dot.move_to(pos1)
        self.emphasize_dot(pos1, run_time=0.15)
        self.add(self.dot)
        l = Line(pos1, pos2, **self.line_config)
        self.play(ShowCreation(l), self.dot.move_to, pos2, run_time=run_time - 0.3, rate_func=rate_func)
        self.emphasize_dot(pos2, run_time=0.15)
        self.remove(self.dot)
        return l

    def draw_line_(self, l, is_prepared=True, run_time=1.2, rate_func=smooth, pre_time=0.8):
        pos1, pos2 = l.get_start(), l.get_end()
        if not is_prepared: self.set_ruler(pos1, pos2, run_time=pre_time)
        self.dot.move_to(pos1)
        self.emphasize_dot(pos1, run_time=0.15)
        self.add(self.dot)
        # l = Line(pos1, pos2, **self.line_config)
        self.play(ShowCreation(l), self.dot.move_to, pos2, run_time=run_time - 0.3, rate_func=rate_func)
        self.emphasize_dot(pos2, run_time=0.15)
        self.remove(self.dot)
        return l

    def put_aside_ruler(self, direction=DOWN, run_time=0.5):
        self.bring_to_front(self.ruler)
        self.play(self.ruler.move_to, direction * 15, run_time=run_time)

    def put_aside_compass(self, direction=DOWN, run_time=0.5):
        self.bring_to_front(self.cp)
        self.play(self.cp.move_to, direction * 15, run_time=run_time)

    def get_length_label(self, p1, p2, text='', reverse_label=False, add_bg=False, bg_color=WHITE):
        l = Line(p1, p2)
        b = Brace(l, direction=complex_to_R3(np.exp(1j * (l.get_angle() + PI / 2 * (1 - 2 * float(reverse_label))))),
                  **self.brace_config)
        t = Text(text, **self.text_config).scale(0.2)
        if add_bg:
            bg = SurroundingRectangle(t, fill_color=bg_color, fill_opacity=0.6, stroke_opacity=0).set_height(
                t.get_height() + 0.05, stretch=True).set_width(t.get_width() + 0.05, stretch=True)
            b.put_at_tip(bg, buff=0.0)
            b.put_at_tip(t, buff=0.05)
            return b, bg, t
        else:
            b.put_at_tip(t, buff=0.05)
            return b, t

    def set_compass_and_show_span(self, p1, p2, run_time=1, show_span_time=[0.4, 0.3, 0.9, 0.4], text='',
                                  reverse_label=False, add_bg=True, **kwargs):
        self.set_compass(p1, p2, run_time=run_time, **kwargs)
        bt = self.get_length_label(p1, p2, text=text, reverse_label=reverse_label, add_bg=add_bg)
        b, t = bt[0], bt[-1]
        st = show_span_time
        self.play(ShowCreation(b), run_time=st[0])
        if add_bg:
            self.add(bt[1])
            self.play(FadeIn(t), run_time=st[1])
        else:
            self.play(FadeIn(t), run_time=st[1])
        self.wait(st[2])
        self.play(FadeOut(VGroup(*bt)), run_time=st[3])
        return bt

    def set_compass_and_show_span_(self, p1, p2, run_time=1, show_span_time=[0.4, 0.3, 0.9, 0.4], text='',
                                   reverse_label=False, add_bg=True, **kwargs):
        self.set_compass_(p1, p2, run_time=run_time, **kwargs)
        bt = self.get_length_label(p1, p2, text=text, reverse_label=reverse_label)
        b, t = bt[0], bt[-1]
        st = show_span_time
        self.play(ShowCreation(b), run_time=st[0])
        if add_bg:
            self.add(bt[1])
            self.play(FadeIn(t), run_time=st[1])
        else:
            self.play(FadeIn(t), run_time=st[1])
        self.wait(st[2])
        self.play(FadeOut(VGroup(*bt)), run_time=st[3])
        return bt

    def highlight_on(self, *mobjects, to_front=True, stroke_config={'color': '#66CCFF', 'width': 4}, run_time=1,
                     **kwargs):
        self.highlight = VGroup(*mobjects)
        self.play(self.highlight.set_stroke, stroke_config, run_time=run_time, **kwargs)
        if to_front:
            self.bring_to_front(self.highlight)
            self.bring_to_front(self.cp, self.ruler)

    def highlight_off(self, *mobjects):

        pass

    def show_arc_info(self, arc, time_list=[0.5, 0.2, 0.3]):

        c, r, s, a, ps, pe = arc.arc_center, arc.radius, arc.start_angle, arc.angle, arc.get_start(), arc.get_end()
        d_center = Dot(c, radius=0.08, color=PINK)
        r1, r2 = DashedLine(c, ps, stroke_width=3.5, stroke_color=PINK), DashedLine(c, pe, stroke_width=3.5,
                                                                                    stroke_color=PINK)
        arc_new = Arc(arc_center=c, radius=r, start_angle=s, angle=a, stroke_width=8, stroke_color=RED)
        self.play(ShowCreation(arc_new), run_time=time_list[0])
        self.play(FadeIn(arc_new), run_time=time_list[1])
        self.play(ShowCreation(r1), ShowCreation(r2), run_time=time_list[2])


class Gauss_heptadecagon(DrawingScene):
    CONFIG = {
        'compass_config': {
            'stroke_color': LIGHT_PINK,
            'fill_color': WHITE,
            'stroke_width': 2,
            'leg_length': 4.05,
            'leg_width': 0.12,
            'r': 0.2,
            'depth_test': True,
        },
        'add_ruler': True,
    }

    def construct(self):
        p1 = (0, 0.75, 0)
        p2 = (1.5, 3 / 8, 0)
        p3 = (0, -np.sqrt(153 / 64) + 0.75, 0)
        s = (np.sqrt(153) - 3) / 4
        ag = arctan(s / 3)
        text = Text('Gauss Heptadecagon', font='Cambria Math', color=WHITE).scale(2)
        text1 = Text(script[0], font='KaiTi').set_color_by_gradient(PURPLE_E, RED_E).scale(1.6)
        v = AnimationGroup(text.animate.shift(UP * 1.5), ShowCreation(text1))
        self.play(Write(text))
        self.wait(0.5)
        self.play(v)
        self.wait(1)
        self.play(FadeOut(text), FadeOut(text1))
        c1 = Circle(radius=2, stroke_width=3, stroke_color='#66CCFF')
        self.play(FadeIn(self.ruler))
        l1 = self.draw_line(LEFT * 6, RIGHT * 6, is_prepared=False)
        self.put_aside_ruler()
        self.set_compass((0, 0, 0), (1, 0, 0))
        self.wait(0.2)
        self.set_compass(c1.get_center(), (2, 0, 0), run_time=0.4)
        arc_1 = Arc(arc_center=(-2, 0, 0), radius=4, start_angle=-PI / 2.5, angle=2 * PI / 2.5, **self.arc_config)
        arc_2 = Arc(arc_center=(2, 0, 0), radius=4, start_angle=1.5 * PI / 2.5, angle=2 * PI / 2.5, **self.arc_config)
        self.wait(0.14)
        self.bring_to_back(c1)
        self.draw_arc_by_compass(c1, run_time=1.5)

        self.wait(0.2)
        # self.cp.reverse_tip()
        self.set_compass((-2, 0, 0), (2, 0, 0), run_time=0.4)
        self.wait(0.25)
        self.set_compass_to_draw_arc(arc_1, emphasize_dot=True)
        self.wait(0.12)

        self.draw_arc_by_compass(arc_1)
        self.wait(0.25)
        self.set_compass_to_draw_arc(arc_2, emphasize_dot=True)
        self.wait(0.12)

        self.draw_arc_by_compass(arc_2)
        self.wait(0.2)
        self.put_aside_compass()
        self.set_ruler(UP, DOWN)
        l2 = self.draw_line(UP * 3.8, DOWN * 3.8)
        self.put_aside_ruler(direction=LEFT)
        self.play(FadeOut(arc_1), FadeOut(arc_2), run_time=0.8)
        c_v = Group(c1, l2, l1)
        self.play(c_v.scale, 1.5, run_time=1)
        arc_3 = Arc(arc_center=(0, 3, 0), radius=3, start_angle=1.1 * PI, angle=2 * PI / 2.5, **self.arc_config)
        self.wait(0.2)
        self.set_compass_to_draw_arc(arc_3, run_time=1.2)
        self.wait(0.2)
        self.draw_arc_by_compass(arc_3)
        self.put_aside_compass()
        self.wait(0.2)
        l3 = self.draw_line(UP * 1.5 + LEFT * 3, UP * 1.5 + RIGHT * 3, is_prepared=False)
        self.wait(0.2)
        self.put_aside_ruler()
        self.wait(0.2)
        arc_4 = Arc(arc_center=(0, 1.5, 0), radius=1.5, start_angle=1.1 * PI, angle=2 * PI / 2.5, stroke_color=GREEN_C,
                    stroke_width=1.8)
        self.set_compass_to_draw_arc(arc_4, run_time=1.2)
        self.draw_arc_by_compass(arc_4)
        arc_5 = Arc(arc_center=(0, 0, 0), radius=1.5, start_angle=0.1 * PI, angle=2 * PI / 2.5, stroke_color=GREEN_C,
                    stroke_width=1.8)
        self.set_compass_to_draw_arc(arc_5, run_time=1.2)
        self.draw_arc_by_compass(arc_5)
        self.put_aside_compass()
        self.wait(0.2)
        l4 = self.draw_line(UP * 0.75 + LEFT * np.sqrt(30 / 16), UP * 0.75 + RIGHT * np.sqrt(30 / 16),
                            is_prepared=False)
        self.wait(0.2)
        l5 = self.draw_line(UP * 0.75, RIGHT * 3, is_prepared=False)
        self.wait(0.2)
        self.put_aside_ruler()
        self.play(FadeOut(arc_3), FadeOut(arc_4), FadeOut(arc_5), FadeOut(l3), FadeOut(l4), run_time=1.2)
        arc_6 = Arc(arc_center=p1, radius=np.sqrt(153 / 64), start_angle=-np.arctan(0.25), angle=-4.2 * PI / 3,
                    **self.arc_config)
        arc_60 = Arc(arc_center=p1, radius=np.sqrt(153 / 64), start_angle=-np.arctan(0.25), angle=-2 * ag,
                     **self.arc_config)
        self.cp.reverse_tip()
        self.set_compass_to_draw_arc(arc_6, run_time=1.2)
        self.draw_arc_by_compass(arc_6)
        self.add(arc_60)
        self.wait(0.2)

        r = math.dist(p3, p2)
        r2 = np.sqrt(153 / 64)
        arc_7 = Arc(arc_center=p3, radius=r, start_angle=np.arctan(np.sqrt(153 / 144) - 0.25),
                    angle=- PI / 2.5, **self.arc_config)
        arc_8 = Arc(arc_center=p2, radius=r, start_angle=np.pi + np.arctan(np.sqrt(153 / 144) - 0.25),
                    angle=PI / 2.5, **self.arc_config)
        self.set_compass_to_draw_arc(arc_7, run_time=1.2)
        self.draw_arc_by_compass(arc_7)
        self.cp.reverse_tip()
        self.set_compass_to_draw_arc(arc_8, run_time=0.5)
        self.draw_arc_by_compass(arc_8)
        self.wait(0.2)
        self.put_aside_compass()

        l6 = self.draw_line(UP * 0.75, DOWN * 9 / 4 + RIGHT * s, is_prepared=False)
        self.wait(0.2)
        self.put_aside_ruler()
        arc_9 = Arc(arc_center=(sin(ag) * r2, -cos(ag) * r2 + 0.75, 0), radius=sin(ag / 2) * r2 * 2,
                    start_angle=pi + ag / 2, angle=PI / 2.5, **self.arc_config)
        self.set_compass_to_draw_arc(arc_9, run_time=1)
        self.draw_arc_by_compass(arc_9)
        arc_10 = Arc(arc_center=(0, -r2 + 0.75, 0), radius=sin(ag / 2) * r2 * 2,
                     start_angle=ag / 2, angle=-PI / 2.5, **self.arc_config)
        self.cp.reverse_tip()
        self.set_compass_to_draw_arc(arc_10, run_time=0.5)
        self.draw_arc_by_compass(arc_10)
        self.wait(0.2)
        self.put_aside_compass()
        l7 = self.draw_line(UP * 0.75, DOWN * 9 / 4 + RIGHT * tan(ag / 2) * 3, is_prepared=False)
        arc_11 = Arc(arc_center=(0, 0.75, 0), radius=r2 * 1.3, start_angle=-PI / 2, angle=ag / 2,
                     stroke_color=RED_C,
                     stroke_width=2)
        text_0 = Tex('\\frac{\\alpha }{4}').next_to(arc_11, DOWN, buff=0.1).scale(0.6).set_color(RED_C)
        text_1 = Tex('\\alpha').move_to(RIGHT * 1.4 + DOWN * 0.79).scale(0.6).set_color(LIGHT_PINK)
        self.wait(0.2)
        self.put_aside_ruler()
        self.wait(0.2)
        all_vg = VGroup(arc_6, arc_7, arc_8, arc_9, arc_10, l6)
        self.play(FadeOut(all_vg), run_time=1)
        self.play(FadeIn(arc_11), FadeIn(text_0), FadeIn(text_1))
        self.wait(0.8)
        self.play(FadeOut(arc_11), FadeOut(text_0), FadeOut(text_1), FadeIn(arc_6), FadeOut(arc_60), run_time=0.8)
        l8 = self.draw_line(UP * (0.75 + r2 * cos(ag / 2)) + r2 * sin(ag / 2) * LEFT,
                            DOWN * 9 / 4 + RIGHT * tan(ag / 2) * 3, is_prepared=False)
        self.remove(l7)
        self.put_aside_ruler()
        self.wait(0.2)


class Gauss_step1(DrawingScene):
    CONFIG = {
        'compass_config': {
            'stroke_color': LIGHT_PINK,
            'fill_color': WHITE,
            'stroke_width': 2,
            'leg_length': 4.05,
            'leg_width': 0.12,
            'r': 0.2,
            'depth_test': True,
        },
        'add_ruler': True,
    }

    def construct(self):
        p1 = (0, 0.75, 0)
        s = (np.sqrt(153) - 3) / 4
        ag = arctan(s / 3)
        r2 = np.sqrt(153 / 64)
        x1 = -sqrt(459 / 64)
        x2 = sqrt(1 + tan(ag / 2) ** 2)
        x3 = -sqrt(153 / 64)
        t = 1 + tan(ag / 2 + pi / 4) ** 2
        x4 = -sqrt(2 / t) * 0.16
        x5 = -sqrt(2 / t) * (sqrt(3) + 1) * r2 / 2
        x0 = x1 / x2
        y0 = x0 * tan(ag / 2) + 0.75
        y1 = x4 * tan(ag / 2 + pi / 4) + 0.75
        y2 = x5 * tan(ag / 2 + pi / 4) + 0.75
        x6 = 3 / (4 * tan(ag / 2 + pi / 4))
        r3 = x6 + 3
        y3 = sqrt(r3 ** 2 / 4 - (1.5 - x6 / 2) ** 2)
        cta = arctan(y3 / (1.5 - x6 / 2))
        x7 = 3 / 4 * tan(ag / 2)
        r4 = sqrt(x7 ** 2 + y3 ** 2)
        cta_1 = arctan(y3 / x7)
        y4 = sqrt(9 - (x7 + r4) ** 2)
        p2 = (x7 + r4, y4, 0)
        r5 = math.dist((3, 0, 0), p2)
        c1 = Circle(radius=3, stroke_width=3, stroke_color='#66CCFF')
        l1 = Line(array([-9, 0, 0]), array([9, 0, 0]), **self.line_config)
        l2 = Line(array([0, -5.7, 0]), array([0, 5.7, 0]), **self.line_config)
        l3 = Line(array([0, 0.75, 0]), array([3, 0, 0]), **self.line_config)
        l4 = Line(array([-r2 * sin(ag / 2), 0.75 + r2 * cos(ag / 2)]), array([tan(ag / 2) * 3, -9 / 4]),
                  **self.line_config)
        arc_1 = Arc(arc_center=p1, radius=np.sqrt(153 / 64), start_angle=-np.arctan(0.25), angle=-4.2 * PI / 3,
                    **self.arc_config)
        self.add(c1, l1, l2, arc_1, l3, l4)
        self.wait(0.2)
        arc_2 = Arc(arc_center=(sin(ag / 2) * r2, -cos(ag / 2) * r2 + 0.75, 0), radius=2 * r2,
                    start_angle=(pi + ag) / 2, angle=PI / 2.5, **self.arc_config)
        arc_3 = Arc(arc_center=(-sin(ag / 2) * r2, cos(ag / 2) * r2 + 0.75, 0), radius=2 * r2,
                    start_angle=(-pi + ag) / 2, angle=-PI / 2.5, **self.arc_config)
        self.cp.reverse_tip()
        self.set_compass_to_draw_arc(arc_2, run_time=0.5)
        self.draw_arc_by_compass(arc_2)
        self.cp.reverse_tip()
        self.set_compass_to_draw_arc(arc_3, run_time=1)
        self.draw_arc_by_compass(arc_3)
        self.wait(0.2)
        self.put_aside_compass()
        l5 = self.draw_line(x0 * RIGHT + y0 * UP, 0.75 * UP, is_prepared=False)
        self.wait(0.2)
        self.put_aside_ruler()
        angle_90 = Square(0.32, stroke_width=2.5, stroke_color=RED_E).shift(UR * 0.16).move_to(
            x4 * RIGHT + y1 * UP).rotate(ag / 2)
        self.bring_to_back(angle_90)
        tex1 = Tex('90^{o}').move_to(LEFT * 0.2 + UP * 0.15).scale(0.6).set_color(RED_E)
        self.play(FadeIn(angle_90), FadeIn(tex1), run_time=0.5)
        self.wait(1)
        self.play(FadeOut(angle_90), FadeOut(tex1), run_time=0.5)
        arc_4 = Arc(arc_center=(sin(ag / 2) * r2, -cos(ag / 2) * r2 + 0.75, 0), radius=sqrt(2) * r2,
                    start_angle=pi * 3 / 4 + ag / 2, angle=PI / 2.5, **self.arc_config)
        self.cp.reverse_tip()
        self.set_compass_to_draw_arc(arc_4, run_time=1)
        self.draw_arc_by_compass(arc_4)

        arc_5 = Arc(arc_center=(x3 / x2, x3 * tan(ag / 2) + 0.75, 0), radius=sqrt(2) * r2,
                    start_angle=- pi / 4 + ag / 2, angle=-PI / 2.5, **self.arc_config)
        self.cp.reverse_tip()
        self.set_compass_to_draw_arc(arc_5, run_time=1)
        self.draw_arc_by_compass(arc_5)
        self.wait(0.2)
        self.put_aside_compass()
        l6 = self.draw_line(x5 * RIGHT + y2 * UP, 0.75 * UP, is_prepared=False)
        self.put_aside_ruler()
        self.wait(0.2)
        v_1 = VGroup(arc_1, arc_2, arc_3, arc_4, arc_5, l5)
        self.play(FadeOut(v_1), run_time=1)
        arc_6 = Arc(arc_center=(0, 0.75, 0), radius=r2 * 0.6, start_angle=-pi / 2 + ag / 2, angle=-pi / 4,
                    stroke_width=2.5, stroke_color=RED_C)
        tex2 = Tex('45^{o}').move_to(DOWN * 0.5).scale(0.6).set_color(RED_E)
        tex_background = Rectangle(width=0.5, height=0.25).move_to(DOWN * 0.5).set_color(
            BLACK).set_opacity(1)
        v_2 = VGroup(arc_6, tex_background, tex2)
        self.play(FadeIn(v_2), run_time=0.7)
        self.wait(1)
        self.play(FadeOut(v_2), FadeOut(l3), run_time=0.5)
        arc_7 = Arc(arc_center=(-x6, 0, 0), radius=r3, start_angle=-PI / 2.5, angle=2 * PI / 2.5,
                    **self.arc_config)
        arc_8 = Arc(arc_center=(3, 0, 0), radius=r3, start_angle=1.5 * PI / 2.5, angle=2 * PI / 2.5,
                    **self.arc_config)
        self.set_compass_to_draw_arc(arc_7, run_time=1)
        self.draw_arc_by_compass(arc_7)
        self.set_compass_to_draw_arc(arc_8, run_time=1)
        self.draw_arc_by_compass(arc_8)
        self.wait(0.2)
        self.put_aside_compass()
        l7 = self.draw_line(UP * r3 * sqrt(3) / 2 + RIGHT * (1.5 - x6 / 2),
                            DOWN * r3 * sqrt(3) / 2 + RIGHT * (1.5 - x6 / 2), is_prepared=False)
        self.wait(0.2)
        self.put_aside_ruler()
        arc_9 = Arc(arc_center=(1.5 - x6 / 2, 0, 0), radius=r3 / 2, start_angle=-pi, angle=-cta, **self.arc_config)
        self.cp.reverse_tip()
        self.set_compass_to_draw_arc(arc_9, run_time=1)
        self.draw_arc_by_compass(arc_9)
        self.put_aside_compass()
        self.play(FadeOut(arc_7), FadeOut(arc_8), FadeOut(l7), run_time=1)
        arc_10 = Arc(arc_center=(x7, 0, 0), radius=r4, start_angle=pi - cta_1, angle=-pi + cta_1, **self.arc_config)
        self.set_compass_to_draw_arc(arc_10, run_time=1)
        self.draw_arc_by_compass(arc_10)
        self.wait(0.2)
        arc_11 = Arc(arc_center=(x7 + r4, 0, 0), radius=0.7, start_angle=-pi, angle=PI, **self.arc_config)
        self.cp.reverse_tip()
        self.set_compass_to_draw_arc(arc_11, run_time=0.5)
        self.draw_arc_by_compass(arc_11)
        arc_12 = Arc(arc_center=(x7 + r4 - 0.7, 0, 0), radius=1.4, start_angle=0, angle=PI / 3, **self.arc_config)
        self.set_compass_to_draw_arc(arc_12, run_time=0.5)
        self.draw_arc_by_compass(arc_12)
        arc_13 = Arc(arc_center=(x7 + r4 + 0.7, 0, 0), radius=1.4, start_angle=pi, angle=-PI / 3, **self.arc_config)
        self.cp.reverse_tip()
        self.set_compass_to_draw_arc(arc_13, run_time=0.5)
        self.draw_arc_by_compass(arc_13)
        self.put_aside_compass()
        self.wait(0.2)
        l8 = self.draw_line(UP * y4 + RIGHT * (x7 + r4), RIGHT * (x7 + r4), is_prepared=False)
        self.wait(0.2)
        self.put_aside_ruler()
        angle_90 = Square(0.32, stroke_width=2.5, stroke_color=RED_E).shift(UR * 0.16).move_to(
            (x7 + r4 + 0.16) * RIGHT + 0.16 * UP)
        v_3 = VGroup(arc_9, arc_10, l6, arc_11, arc_12, arc_13, l4)
        self.play(FadeOut(v_3), run_time=1)
        self.bring_to_back(angle_90)
        self.play(FadeIn(angle_90), run_time=0.5)
        l9 = self.draw_line(UP * y4 + RIGHT * (x7 + r4), (0, 0, 0), is_prepared=False)
        arc_14 = Arc(arc_center=(0, 0, 0), radius=0.5, start_angle=0, angle=6 * PI / 17,
                     stroke_width=2.5, stroke_color=RED_C)
        self.put_aside_ruler()
        tex3 = Tex('3\\frac{360^{o} }{17} ').move_to(RIGHT * 0.9 + UP * 0.35).scale(0.6).set_color(RED_E)
        self.play(FadeOut(angle_90), FadeIn(arc_14), FadeIn(tex3), run_time=0.5)
        self.wait(0.5)
        self.play(FadeOut(arc_14), FadeOut(tex3), FadeOut(l9), run_time=0.5)
        arc_15 = Arc(arc_center=(3, 0, 0), radius=r5, start_angle=23 * PI / 34, angle=11 * PI / 17, **self.arc_config)
        agl = 11 * PI / 34
        initial_center = np.array([3, 0, 0])
        point_to_rotate = np.array([x7 + r4, y4, 0])
        num_rotations = 17
        # 计算每次旋转后的中心点和起始角度
        centers = []
        l10 = Line(array([x7 + r4, y4, 0]), array([3, 0, 0]), **self.line_config)
        self.cp.reverse_tip()
        self.set_compass_to_draw_arc(arc_15, run_time=0.5, emphasize_dot=False)
        self.play(FadeIn(l10), run_time=0.5)
        self.wait(0.5)
        self.play(FadeOut(l10), FadeOut(l8), run_time=0.5)
        self.cp.reverse_tip()
        for i in range(1, num_rotations + 1):
            next_point = rotate_point_around_another(point_to_rotate, initial_center)
            point_to_rotate = initial_center
            initial_center = next_point
            # 添加到列表中
            centers.append(point_to_rotate)
        # 将列表转换为 numpy 数组
        points = np.array(centers)

        # 忽略 z 坐标，只使用 x 和 y 坐标来计算极角
        xy_points = points[:, :2]

        # 计算每个点的极角
        angles = np.arctan2(xy_points[:, 1], xy_points[:, 0])

        # 按极角排序
        sorted_indices = np.argsort(angles)
        sorted_points = points[sorted_indices]
        sorted_points_list = [np.array(point) for point in sorted_points]
        # 创建包含多个弧线的组
        arcs = VGroup(
            *[Arc(arc_center=centers[i], radius=r5, start_angle=(1 - i) * pi + (2 * i - 1) * agl, angle=2 * agl,
                  **self.arc_config) for i in
              range(num_rotations)]
        )

        for i in range(num_rotations):
            self.cp.reverse_tip()
            self.set_compass_to_draw_arc(arcs[i], run_time=0.1, emphasize_dot=False)
            self.draw_arc_by_compass(arcs[i], run_time=0.32)
        self.wait(0.2)
        self.put_aside_compass()
        for i in range(num_rotations):
            if i == num_rotations - 1:
                dl = Line(sorted_points_list[i], sorted_points_list[0], stork_width=1.5, stroke_color=colors[i])
                self.draw_line_(dl, is_prepared=False, run_time=0.2,
                                pre_time=0.2)
            else:
                dl = Line(sorted_points_list[i], sorted_points_list[i + 1], stork_width=1.5, stroke_color=colors[i])
                self.draw_line_(dl, is_prepared=False, run_time=0.2,
                                pre_time=0.2)
        self.wait(0.2)
        self.put_aside_ruler()
        self.play(FadeOut(arcs), FadeOut(c1), FadeOut(l1), FadeOut(l2), run_time=1)
        lines = AnimationGroup(
            *[ShowCreation(Line(sorted_points_list[i], array([0,0,0]), stork_width=0.1, stroke_color=colors[i])) for i in
              range(num_rotations)]
        )
        self.play(lines)

