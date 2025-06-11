from manimlib import *


class TestGlsl(Scene):
    def construct(self):
        square = Square(side_length=4)
        square.set_color_by_code(f"""
            vec3 blue = vec3{tuple(hex_to_rgb(BLUE))};
            vec3 red = vec3{tuple(hex_to_rgb(RED))};
            color.rgb = mix(blue, red, (point.x + 1.5) / 3);
        """)
        self.add(square)

        # hex_to_rgb 会将 16 进制颜色字符串转变为 RGB 三元列表，其值范围均为 [0,1]
        # 利用 tuple 将它们用圆括号括起来，翻译后的字符串就变为（这里仅展示一部分）
        # vec3 blue = vec3(0.345, 0.769, 0.867);

