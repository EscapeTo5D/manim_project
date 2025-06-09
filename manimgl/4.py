from manimlib import *
from typing import Callable
import numpy as np


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


class RotateShowCreation(Scene):
    def construct(self):
        # roate
        logo_green = "#87c2a5"
        logo_blue = "#525893"
        logo_red = "#e07a5f"
        logo_black = "#343434"
        ds_m = Tex(r"\mathbb{M}", fill_color=logo_black).scale(7)
        ds_m.shift(2.25 * LEFT + 1.5 * UP)
        circle = Circle(color=logo_green, fill_opacity=1).shift(LEFT)
        square = Square(color=logo_blue, fill_opacity=1).shift(UP)
        triangle = Triangle(color=logo_red, fill_opacity=1).shift(RIGHT)
        logo = VGroup(triangle, square, circle, ds_m)  # order matters
        logo.move_to(ORIGIN)
        self.add(logo)
        # 方法1: 壳体引导
        self.play(RotatingCreate(shapes, angle=PI, axis=UP,run_time=4))
        self.wait()


