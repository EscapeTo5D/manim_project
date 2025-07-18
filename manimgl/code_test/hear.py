from manim_imports_ext import *
import random
from math import sin, cos, pi, log
import numpy as np

class HeartAnimation(Scene):
    def construct(self):
        # 创建Heart对象
        heart = Heart()
        
        # 创建动画
        self.play_heart_animation(heart)
    
    def play_heart_animation(self, heart):
        """播放心形动画"""
        # 总帧数
        total_frames = heart.generate_frame
        
        for frame in range(total_frames * 3):  # 循环播放3次
            current_frame = frame % total_frames
            
            # 获取当前帧的所有点
            points_data = heart.all_points[current_frame]
            
            # 创建点的集合
            dots = VGroup()
            
            for x, y, size in points_data:
                # 将坐标转换为manim坐标系（原点在中心，y轴向上）
                manim_x = (x - 320) / 80  # 缩放到合适大小
                manim_y = -(y - 240) / 80  # 翻转y轴并缩放
                
                # 创建点，大小根据原始size调整
                dot = Dot(
                    point=[manim_x, manim_y, 0],
                    radius=size * 0.01,
                    color=PINK
                )
                dots.add(dot)
            
            # 如果是第一帧，直接显示
            if frame == 0:
                self.add(dots)
                current_dots = dots
            else:
                # 用新的点替换旧的点
                self.remove(current_dots)
                self.add(dots)
                current_dots = dots
            
            # 等待一小段时间
            self.wait(0.16)


class Heart:
    """心形类，生成动态心形效果的所有帧数据"""
    
    def __init__(self, generate_frame=20):
        self.CANVAS_WIDTH = 640
        self.CANVAS_HEIGHT = 480
        self.CANVAS_CENTER_X = self.CANVAS_WIDTH / 2
        self.CANVAS_CENTER_Y = self.CANVAS_HEIGHT / 2
        self.IMAGE_ENLARGE = 11
        
        self._points = set()  # 原始爱心坐标集合
        self._edge_diffusion_points = set()  # 边缘扩散效果点坐标集合
        self._center_diffusion_points = set()  # 中心扩散效果点坐标集合
        self.all_points = {}  # 每帧动态点坐标
        
        self.build(2000)
        self.random_halo = 1000
        self.generate_frame = generate_frame
        
        # 生成所有帧的数据
        for frame in range(generate_frame):
            self.calc(frame)

    def heart_function(self, t, shrink_ratio=None):
        """心形函数"""
        if shrink_ratio is None:
            shrink_ratio = self.IMAGE_ENLARGE
            
        x = 16 * (sin(t) ** 3)
        y = -(13 * cos(t) - 5 * cos(2 * t) - 2 * cos(3 * t) - cos(4 * t))

        x *= shrink_ratio
        y *= shrink_ratio

        x += self.CANVAS_CENTER_X
        y += self.CANVAS_CENTER_Y

        return int(x), int(y)

    def scatter_inside(self, x, y, beta=0.15):
        """内部散射效果"""
        ratio_x = - beta * log(random.random())
        ratio_y = - beta * log(random.random())

        dx = ratio_x * (x - self.CANVAS_CENTER_X)
        dy = ratio_y * (y - self.CANVAS_CENTER_Y)

        return x - dx, y - dy

    def shrink(self, x, y, ratio):
        """收缩效果"""
        force = -1 / (((x - self.CANVAS_CENTER_X) ** 2 + (y - self.CANVAS_CENTER_Y) ** 2) ** 0.6)
        dx = ratio * force * (x - self.CANVAS_CENTER_X)
        dy = ratio * force * (y - self.CANVAS_CENTER_Y)
        return x - dx, y - dy

    def curve(self, p):
        """曲线函数"""
        return 2 * (2 * sin(4 * p)) / (2 * pi)

    def build(self, number):
        """构建心形的基本点集"""
        # 生成原始心形点
        for _ in range(number):
            t = random.uniform(0, 2 * pi)
            x, y = self.heart_function(t)
            self._points.add((x, y))

        # 生成边缘扩散点
        for _x, _y in list(self._points):
            for _ in range(3):
                x, y = self.scatter_inside(_x, _y, 0.05)
                self._edge_diffusion_points.add((x, y))

        # 生成中心扩散点
        point_list = list(self._points)
        for _ in range(4000):
            x, y = random.choice(point_list)
            x, y = self.scatter_inside(x, y, 0.17)
            self._center_diffusion_points.add((x, y))

    def calc_position(self, x, y, ratio):
        """计算动态位置"""
        force = 1 / (((x - self.CANVAS_CENTER_X) ** 2 + (y - self.CANVAS_CENTER_Y) ** 2) ** 0.520)

        dx = ratio * force * (x - self.CANVAS_CENTER_X) + random.randint(-1, 1)
        dy = ratio * force * (y - self.CANVAS_CENTER_Y) + random.randint(-1, 1)

        return x - dx, y - dy

    def calc(self, generate_frame):
        """计算指定帧的所有点位置"""
        ratio = 10 * self.curve(generate_frame / 10 * pi)  # 圆滑的周期的缩放比例

        halo_radius = int(4 + 6 * (1 + self.curve(generate_frame / 10 * pi)))
        halo_number = int(3000 + 4000 * abs(self.curve(generate_frame / 10 * pi) ** 2))

        all_points = []

        # 生成光晕点
        heart_halo_point = set()
        for _ in range(halo_number):
            t = random.uniform(0, 2 * pi)
            x, y = self.heart_function(t, shrink_ratio=11.6)
            x, y = self.shrink(x, y, halo_radius)
            if (x, y) not in heart_halo_point:
                heart_halo_point.add((x, y))
                x += random.randint(-14, 14)
                y += random.randint(-14, 14)
                size = random.choice((1, 2, 2))
                all_points.append((x, y, size))

        # 处理主心形点
        for x, y in self._points:
            x, y = self.calc_position(x, y, ratio)
            size = random.randint(1, 3)
            all_points.append((x, y, size))

        # 处理边缘扩散点
        for x, y in self._edge_diffusion_points:
            x, y = self.calc_position(x, y, ratio)
            size = random.randint(1, 2)
            all_points.append((x, y, size))

        # 处理中心扩散点
        for x, y in self._center_diffusion_points:
            x, y = self.calc_position(x, y, ratio)
            size = random.randint(1, 2)
            all_points.append((x, y, size))

        self.all_points[generate_frame] = all_points


