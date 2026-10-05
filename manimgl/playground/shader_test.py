from manim_imports_ext import *


class TestGlsl(Scene):
    def construct(self):
        # 正方形
        square = Square(side_length=4)
        b_r, b_g, b_b = list(hex_to_rgb(BLUE))
        r_r, r_g, r_b = list(hex_to_rgb(RED))
        square.set_color_by_code(f"""
            let blue = vec3f({b_r}, {b_g}, {b_b});
            let red = vec3f({r_r}, {r_g}, {r_b});

            // 混合颜色（WGSL 不支持 color.rgb = ... 的 swizzle 赋值，须整体赋值）
            let mixed = mix(blue, red, (point.x + 1.5) / 3.0);
            color = vec4f(mixed, color.a);
        """)
        self.add(square)

        # hex_to_rgb 会将 16 进制颜色字符串转变为 RGB 三元列表，其值范围均为 [0,1]
        # 利用 f-string 将它们填进 WGSL 代码，翻译后的字符串变为（这里仅展示一部分）
        # let blue = vec3f(0.345, 0.769, 0.867);
        self.wait()
