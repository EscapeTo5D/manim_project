cript = '''

'''
from manimlib import *
from typing import Callable, Iterable, Tuple
from numpy import *


class ShaderSurface(Surface):
    shader_folder: str = str(Path(Path(__file__).parent, "shader_surface"))

    def __init__(
            self,
            uv_func: Callable[[float, float], Iterable[float]],
            u_range: tuple[float, float] = (0, 1),
            v_range: tuple[float, float] = (0, 1),
            brightness = 1.5,
            **kwargs
    ):
        self.passed_uv_func = uv_func
        super().__init__(u_range=u_range, v_range=v_range, **kwargs)

        # 初始化shader uniforms
        self.set_uniform(time=0)
        self.set_uniform(brightness=brightness)

        # 添加时间更新器
        self.add_updater(lambda m, dt: m.increment_time(dt))

    def uv_func(self, u, v):
        return self.passed_uv_func(u, v)

    def increment_time(self, dt):
        self.uniforms["time"] += 1 * dt
        return self

class CalabiYauSurface(Group):
    def __init__(
        self,
        axes: ThreeDAxes,
        n: int = 5,
        alpha: float = PI / 4,
        resolution: tuple[int, int] = (51, 51),
        u_range: tuple[float, float] = (0, PI / 2),
        v_range: tuple[float, float] = (-1, 1),
        brightness = 1.2,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.n = n
        self.alpha = alpha
        self.resolution = resolution
        self.u_range = u_range
        self.v_range = v_range
        self.axes = axes
        self.brightness=brightness
        self.build_surfaces()
    """
    ℜ((e^(2πik1))^(1/n) * cosh(a + bi)^(2/n))
    ℜ((e^(2πik2))^(1/n) * sin(a + bi)^(2/n))
    ℑ((cos(t)*(e^(2πik1))^(1/n)*cos(a + bi)^(2/n)+sin(t)*(e^(2πik2))^(1/n)*sin(a + bi)^(2/n))
    """
    @staticmethod
    def z1k(x: float, y: float, k: int, n: int) -> complex:
        z = x + 1j * y
        return exp(2j * PI * k / n) * (cos(z) ** (2 / n))

    @staticmethod
    def z2k(x: float, y: float, k: int, n: int) -> complex:
        z = x + 1j * y
        return exp(2j * PI * k / n) * (sin(z) ** (2 / n))

    def calabi_yau_point(
        self, x: float, y: float, k1: int, k2: int, n: int, alpha: float
    ) -> Tuple[float, float, float]:
        z1 = self.z1k(x, y, k1, n)
        z2 = self.z2k(x, y, k2, n)
        calabi_x = real(z1)
        calabi_y = real(z2)
        calabi_z = cos(alpha) * imag(z1) + sin(alpha) * imag(z2)
        return calabi_x, calabi_y, calabi_z

    def build_surfaces(self):
        """构建所有 (k1, k2) 组合的 ShaderSurface 并添加进组"""
        for k1 in range(self.n):
            for k2 in range(self.n):
                surface_func = lambda u, v : self.calabi_yau_point(
                    u, v, k1, k2, self.n, self.alpha
                )
                surface = ShaderSurface(
                    lambda u, v: self.axes.c2p(*surface_func(u, v)),
                    resolution=self.resolution,
                    u_range=self.u_range,
                    v_range=self.v_range,
                    brightness=self.brightness
                )
                self.add(surface)

        self.rotate(PI / 4, axis=OUT)
        self.rotate(PI / 2, axis=RIGHT)
        self.scale(1.5)

class RotatingShowCreate(Animation):
    """
    旋转创建动画 - 使用submobject机制实现逐个创建
    """
    def __init__(
        self,
        mobject: VMobject,
        angle: float = PI,
        axis: np.ndarray = OUT,
        about_point: np.ndarray | None = None,
        about_edge: np.ndarray | None = None,
        lag_ratio: float = 1.0,  # 添加lag_ratio参数控制时间差
        rate_func: Callable[[float], float] = linear,
        **kwargs
    ):
        self.angle = angle
        self.axis = axis
        self.about_point = about_point
        self.about_edge = about_edge
        
        super().__init__(
            mobject, 
            lag_ratio=lag_ratio,
            rate_func=rate_func, 
            **kwargs
        )
        
        if self.about_point is None and self.about_edge is None:
            self.about_point = mobject.get_center()
    
    def interpolate_submobject(
        self,
        submob: VMobject,
        start_submob: VMobject,
        alpha: float
    ) -> None:
        """对每个submobject分别处理创建和旋转"""
        # 先复制数据
        submob.data[:] = start_submob.data[:]
        
        # 应用创建效果（部分显示）
        sub_alpha = self.rate_func(alpha)
        submob.pointwise_become_partial(start_submob, 0, sub_alpha)
        
        # 应用旋转效果
        submob.rotate(
            sub_alpha * self.angle,
            axis=self.axis,
            about_point=self.about_point,
            about_edge=self.about_edge,
        )

class ComplexSurfaceWireframe(VGroup):
    """复数函数曲面的线框表示"""
    def __init__(self, n=5, resolution=11, alpha=PI/4,**kwargs):
        super().__init__(**kwargs)
        self.n = n
        self.alpha: float = alpha
        self.resolution = resolution
        self.build_wireframes()

    def build_wireframes(self):
        for k1 in range(self.n):
            for k2 in range(self.n):
                lines = self.create_wireframe_lines(self.n, k1, k2, self.alpha)
                self.add(lines)

        self.rotate(PI / 4, axis=OUT)
        self.rotate(PI / 2, axis=RIGHT)
        self.scale(1.5)

    def create_wireframe_lines(self, n, k1, k2, alpha: float):
        """创建给定参数下的网格线框"""
        def surface_point(u, v):
            x = u * PI / 2
            y = (v - 0.5) * 2
            z_xy = complex(x, y)

            exp_factor1 = exp(1j * 2 * PI * k1 / n)
            exp_factor2 = exp(1j * 2 * PI * k2 / n)

            cos_term = cos(z_xy) ** (2 / n)
            sin_term = sin(z_xy) ** (2 / n)

            z1 = exp_factor1 * cos_term
            z2 = exp_factor2 * sin_term

            # point_x = (z1.real + z2.real)
            # point_y = (z1.imag + z2.imag)
            # point_z = (z2.real - z1.real)
            point_x = z1.real
            point_y = z2.real
            point_z = cos(alpha) * z1.imag + sin(alpha) * z2.imag

            return array([point_x, point_y, point_z])

        lines = VGroup()

        # u方向的线
        for i in range(self.resolution):
            v_val = i / (self.resolution - 1)
            points = [surface_point(j / (self.resolution - 1), v_val) for j in range(self.resolution)]
            line = VMobject().set_points_as_corners(points)
            line.set_stroke(WHITE, width=1, opacity=0.8)
            lines.add(line)

        # v方向的线
        for j in range(self.resolution):
            u_val = j / (self.resolution - 1)
            points = [surface_point(u_val, i / (self.resolution - 1)) for i in range(self.resolution)]
            line = VMobject().set_points_as_corners(points)
            line.set_stroke(WHITE, width=1, opacity=0.8)
            lines.add(line)

        return lines

class RotatingCreate(Animation):

    def __init__(
            self,
            mobject: VMobject,
            angle: float = PI,
            axis: np.ndarray = OUT,
            about_point: np.ndarray | None = None,
            about_edge: np.ndarray | None = None,
            run_time: float = 5.0,  # 添加默认运行时间
            rate_func: Callable[[float], float] = linear,
            **kwargs
    ):
        self.angle = angle
        self.axis = axis
        self.about_point = about_point
        self.about_edge = about_edge

        super().__init__(
            mobject,
            run_time=run_time,
            rate_func=rate_func,
            **kwargs
        )

        self.starting_mobject = mobject.copy()
        if self.about_point is None and self.about_edge is None:
            self.about_point = mobject.get_center()

    def interpolate_mobject(self, alpha: float) -> None:
        # 简化的单一方法实现
        sub_alpha = self.rate_func(self.time_spanned_alpha(alpha))

        # 数据复制和创建效果
        for mob_target, mob_start in zip(
                self.mobject.family_members_with_points(),
                self.starting_mobject.family_members_with_points()
        ):
            mob_target.data[:] = mob_start.data[:]
            mob_target.pointwise_become_partial(mob_start, 0, sub_alpha)

        # 旋转
        self.mobject.rotate(
            sub_alpha * self.angle,
            axis=self.axis,
            about_point=self.about_point,
            about_edge=self.about_edge,
        )

class CalabiYauSurfaceScene(InteractiveScene):
    def construct(self):
        # 设置场景
        run_time = 6
        background = FullScreenRectangle(fill_color=BLACK).fix_in_frame()
        self.add(background)

        # 设置TEXT 和 equation 公式
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

        # self.play(
        #     LaggedStart(
        #         surfaces_group.animate.rotate(PI / 2, axis=IN),
        #         surfaces_group.animate.rotate(-PI / 2, axis=RIGHT),
        #         Transform(title_e, title_c, run_time=1),
        #         lag_ratio=0.3
        #     ),
        #     run_time=4
        # )


class ComplexSurfaceWireframeScene(InteractiveScene):
    def construct(self):
        # 背景
        background = FullScreenRectangle(fill_color=BLACK).fix_in_frame()
        self.add(background)

        # 添加和展示线框
        wireframe = ComplexSurfaceWireframe()
        self.play(
            RotatingShowCreate(wireframe),
            run_time=4,
            rate_func=linear
        )


class CalabiYauVisualization(InteractiveScene):
    def construct(self):
        # 背景
        background = FullScreenRectangle(fill_color=BLACK).fix_in_frame()
        self.add(background)
        # 添加卡拉比流形
        axes = ThreeDAxes()
        calabi_yau_shader = CalabiYauSurface(
            axes=axes,
            n=5,
            alpha=PI / 4,
            resolution=(21, 21),
            brightness=1.1
        )
        Rotate
        wireframe = ComplexSurfaceWireframe()
        self.play(RotatingShowCreation(calabi_yau_shader, 2*PI, UP), run_time=4)