from manimlib import *
import numpy as np
from typing import Callable, Iterable, Tuple


class ShaderSurface(Surface):
    shader_folder: str = str(Path(Path(__file__).parent, "shader_surface"))

    def __init__(
            self,
            uv_func: Callable[[float, float], Iterable[float]],
            u_range: tuple[float, float] = (0, 1),
            v_range: tuple[float, float] = (0, 1),
            **kwargs
    ):
        self.passed_uv_func = uv_func
        super().__init__(u_range=u_range, v_range=v_range, **kwargs)

        # 初始化shader uniforms
        self.set_uniform(time=0)

        # 添加时间更新器
        self.add_updater(lambda m, dt: m.increment_time(dt))

    def uv_func(self, u, v):
        return self.passed_uv_func(u, v)

    def increment_time(self, dt):
        self.uniforms["time"] += 1.2 * dt
        return self


class CalabiYauSurface:
    def __init__(self):
        pass  # 构造时不设定参数，延迟到 create_surfaces 时传入

    def z1k(self, x: float, y: float, k: int, n: int) -> complex:
        z = x + 1j * y
        return np.exp(2j * np.pi * k / n) * (np.cos(z) ** (2 / n))
    """
    ℜ((e^(2πik1))^(1/n) * cosh(a + bi)^(2/n))
    """
    def z2k(self, x: float, y: float, k: int, n: int) -> complex:
        z = x + 1j * y
        return np.exp(2j * np.pi * k / n) * (np.sin(z) ** (2 / n))
    """
    ℜ((e^(2πik2))^(1/n) * sin(a + bi)^(2/n))
    """
    def calabi_yau_point(
        self, x: float, y: float, k1: int, k2: int, n: int, alpha: float
    ) -> Tuple[float, float, float]:
        z1 = self.z1k(x, y, k1, n)
        z2 = self.z2k(x, y, k2, n)
        calabi_x = np.real(z1)
        calabi_y = np.real(z2)
        calabi_z = np.cos(alpha) * np.imag(z1) + np.sin(alpha) * np.imag(z2)
        return calabi_x, calabi_y, calabi_z
    """
    ℑ((cos(t)*(e^(2πik1))^(1/n)*cos(a + bi)^(2/n)+sin(t)*(e^(2πik2))^(1/n)*sin(a + bi)^(2/n))
    """
    def create_surfaces(
        self,
        axes: ThreeDAxes,
        n: int = 5,
        alpha: float = np.pi / 4,
        resolution: tuple[int, int] = (51, 51),
        u_range: tuple[float, float] = (0, np.pi / 2),
        v_range: tuple[float, float] = (-1, 1)
    ) -> Group:
        surfaces_group = Group()
        for k1 in range(n):
            for k2 in range(n):
                surface_func = lambda u, v: self.calabi_yau_point(u, v, k1, k2, n, alpha)
                surface = ShaderSurface(
                    lambda u, v: axes.c2p(*surface_func(u, v)),
                    resolution=resolution,
                    u_range=u_range,
                    v_range=v_range,
                )
                surfaces_group.add(surface)
        return surfaces_group



class CalabiYauVisualization(InteractiveScene):
    def construct(self):
        # 设置场景
        run_time = 6
        background = FullScreenRectangle(fill_color=BLACK).fix_in_frame()
        self.add(background)

        # 设置TEXT
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
        # Calabi-Yau 和 equation 公式
        axes = ThreeDAxes()
        cy = CalabiYauSurface()
        calabi_yau = cy.create_surfaces(
            axes=axes,
            n=5,
            alpha=np.pi / 4,
            resolution=(51, 51),
        )
        calabi_yau.rotate(np.pi / 4, axis=OUT)
        calabi_yau.rotate(np.pi / 2, axis=RIGHT)
        calabi_yau.scale(1.5)
        self.add(calabi_yau)
        self.play(self.camera.frame.animate.rotate(np.pi, axis=UP), run_time=run_time)