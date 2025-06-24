from manimlib import *
from numpy import *
from typing import Callable, Iterable, Tuple

class ShaderSurface(Surface):
    shader_folder: str = str(Path(Path(__file__).parent.parent / "shader_surface"))

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
            line = VMobject().set_points_smoothly(points)
            line.set_stroke(WHITE, width=1, opacity=0.8)
            lines.add(line)

        # v方向的线
        for j in range(self.resolution):
            u_val = j / (self.resolution - 1)
            points = [surface_point(u_val, i / (self.resolution - 1)) for i in range(self.resolution)]
            line = VMobject().set_points_smoothly(points)
            line.set_stroke(WHITE, width=1, opacity=0.8)
            lines.add(line)

        return lines
