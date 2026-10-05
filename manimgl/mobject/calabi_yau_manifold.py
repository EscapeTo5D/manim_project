from manimlib import *
from manimlib.renderer.uniform_block import COMMON_UNIFORMS, uniform_block_dtype
from numpy import *
import numpy as np
from typing import Callable, Iterable, Tuple

# 玻璃发光着色（自 shader_surface/*.glsl 移植为 WGSL）
# 注入 finalize_color 上下文：可用变量 color/point/normal、frame.* 、mob.*
# WGSL 不允许函数内定义函数，原 pal/spectrum 调色板已内联展开
GLASS_EFFECT_WGSL = """
// === 玻璃发光核心效果 ===
let n = normalize(normal);
let to_camera = normalize(frame.camera_position - point);

// 1. 边缘发光效果 (Fresnel-like glow)
var fresnel = 1.0 - abs(dot(n, to_camera));
fresnel = pow(fresnel, 2.0); // 强化边缘

// 2. 体积感的内部发光
var inner_glow = 0.3 + 0.7 * sin(mob.time * 2.0 + length(point) * 3.0);
inner_glow *= 0.4; // 控制强度

// 3. 动态颜色波动 - 模拟4D几何的色彩变化
let wave1 = sin(dot(point.xy, vec2f(2.0, 3.0)) + mob.time * 1.5);
let wave2 = cos(dot(point.yz, vec2f(1.5, 2.5)) + mob.time * 2.0);
let wave3 = sin(length(point.xz) * 2.0 - mob.time * 2.5);

let color_shift = (wave1 + wave2 + wave3) * 0.2;
let t = fresnel + color_shift + inner_glow;

// 4. spectrum 调色板（pal 公式内联：0.5 + 0.5*cos(2π(t + (0.0, 0.33, 0.67)))）
var base_color = 0.5 + 0.5 * cos(6.28318 * (t * 0.8 + 0.2 + vec3f(0.0, 0.33, 0.67)));

// 5. 蓝绿色调 (模拟原始效果)
base_color *= vec3f(1.4, 2.1, 1.7) * 0.7;

// 6. 紫色环境光 (模拟体积渲染的紫色辉光)
base_color += vec3f(0.6, 0.25, 0.7) * 0.3 * (0.5 + 0.5 * sin(mob.time + length(point)));

// 7. 强烈的边缘高光
let edge_highlight = pow(fresnel, 0.5) * 2.0;
base_color += vec3f(0.8, 1.0, 1.2) * edge_highlight * 0.4;

// 8. 深度雾化效果
let depth = length(point - frame.camera_position);
let fog_factor = smoothstep(2.0, 8.0, depth);
base_color = mix(base_color, vec3f(0.1, 0.2, 0.4), fog_factor * 0.3);

// 9. 距离衰减 (模拟体积渲染的衰减)
base_color *= 1.0 / (1.0 + depth * 0.1);

// 10. 动态亮度脉冲
let pulse = 0.8 + 0.4 * sin(mob.time * 3.0 + dot(point, vec3f(1.0, 1.3, 0.7)));
base_color *= pulse;

// 11. 最终色彩强化和对比度调整
base_color = pow(base_color, vec3f(0.8)) * 1.5; // 提升亮度
base_color = pow(base_color, vec3f(1.2)); // 增加对比度

// 12. 透明度效果（保留 mobject 自身 alpha，对应原 v_color.a *= rgba.a）
let alpha = 0.7 + 0.3 * fresnel;
color = vec4f(base_color * mob.brightness, alpha * color.a);
"""

class ShaderSurface(Surface):
    # 扩展 uniform 块：shader 中通过 mob.time / mob.brightness 访问
    uniform_dtype: np.dtype = uniform_block_dtype(
        *COMMON_UNIFORMS,
        ("resolution", 2),
        ("time", 1),
        ("brightness", 1),
    )

    def __init__(
            self,
            uv_func: Callable[[float, float], Iterable[float]],
            u_range: tuple[float, float] = (0, 1),
            v_range: tuple[float, float] = (0, 1),
            brightness: float = 1.5,
            **kwargs
    ):
        self.passed_uv_func = uv_func
        # 关闭 manim 内置光照（shading=0），原 GLSL 效果自带光照模拟
        kwargs.setdefault("shading", (0.0, 0.0, 0.0))
        super().__init__(u_range=u_range, v_range=v_range, **kwargs)

        # 注入自定义着色（替代旧 shader_folder 的 GLSL）
        self.set_color_by_code(GLASS_EFFECT_WGSL)

        # 初始化shader uniforms
        self.set_uniform(time=0.0)
        self.set_uniform(brightness=brightness)

        # 添加时间更新器
        self.add_updater(lambda m, dt: m.increment_time(dt))

    def uv_func(self, u, v):
        return self.passed_uv_func(u, v)

    def increment_time(self, dt):
        self.uniforms["time"] += dt
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
