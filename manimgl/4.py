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

class SpinShowCreation(Animation):
    """
    逐渐创建整体旋转
    """
    def __init__(
        self,
        mobject: VMobject,
        angle: float = PI,
        axis: np.ndarray = OUT,
        about_point: np.ndarray | None = None,
        about_edge: np.ndarray | None = None,
        lag_ratio: float = 1.0,
        rate_func: Callable[[float], float] = linear,
        **kwargs
    ):
        self.angle = angle
        self.axis = axis
        self.about_point = about_point or mobject.get_center()
        self.about_edge = about_edge

        super().__init__(
            mobject,
            lag_ratio=lag_ratio,
            rate_func=rate_func,
            **kwargs
        )

    def interpolate_submobject(
        self,
        submob: VMobject,
        start_submob: VMobject,
        alpha: float
    ) -> None:
        # 使用 rate_func 控制绘制比例
        submob.pointwise_become_partial(start_submob, 0, self.rate_func(alpha))

    def interpolate(self, alpha: float) -> None:
        # 执行绘制
        super().interpolate(alpha)

        # 添加整体旋转
        angle = self.rate_func(alpha) * self.angle
        self.mobject.rotate(
            angle,
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

class RotatingShowCreateV2(Animation):

    def __init__(
            self,
            mobject: VMobject,
            angle: float = PI,
            axis: np.ndarray = OUT,
            about_point: np.ndarray | None = None,
            about_edge: np.ndarray | None = None,
            lag_ratio: float = 1.0,
            rate_func: Callable[[float], float] = linear,
            **kwargs
    ):
        self.angle = angle
        self.axis = axis
        self.about_point = about_point
        self.about_edge = about_edge

        self.original_mobject = mobject.copy()

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
        create_alpha = self.rate_func(alpha)
        submob.pointwise_become_partial(start_submob, 0, create_alpha)

    def interpolate(self, alpha: float) -> None:
        super().interpolate(alpha)
        self._apply_rotation_effect(alpha)

    def _apply_rotation_effect(self, alpha: float) -> None:
        rotation_alpha = self.rate_func(alpha)
        current_angle = rotation_alpha * self.angle
        self.mobject.rotate(
            current_angle,
            axis=self.axis,
            about_point=self.about_point,
            about_edge=self.about_edge,
        )


    def begin(self) -> None:
        super().begin()

        if not hasattr(self, 'starting_mobject') or self.starting_mobject is None:
            self.starting_mobject = self.mobject.copy()


class RotatingShowCreateV3(ShowCreation):
    """
    继承ShowCreate并添加旋转效果
    """
    def __init__(
        self,
        mobject: VMobject,
        angle: float = PI,
        axis: np.ndarray = OUT,
        about_point: np.ndarray | None = None,
        about_edge: np.ndarray | None = None,
        **kwargs
    ):
        self.angle = angle
        self.axis = axis
        self.about_point = about_point or mobject.get_center()
        self.about_edge = about_edge
        
        super().__init__(mobject, **kwargs)
    
    def interpolate_submobject(
        self,
        submob: VMobject,
        start_submob: VMobject,
        alpha: float
    ) -> None:
        # 先应用ShowCreate的效果
        super().interpolate_submobject(submob, start_submob, alpha)
        
        # 然后应用旋转到这个submobject
        # 注意：这里仍然是对submobject旋转，如果要整体旋转需要用其他方法
        rotation_angle = self.rate_func(alpha) * self.angle
        submob.rotate(
                rotation_angle,
                axis=self.axis,
                about_point=self.about_point,
                about_edge=self.about_edge,
            )



class RotatingShowCreateV4(Animation):

    def __init__(
        self,
        mobject: VMobject,
        angle: float = PI,
        axis: np.ndarray = OUT,
        about_point: np.ndarray | None = None,
        about_edge: np.ndarray | None = None,
        lag_ratio: float = 1.0,
        rate_func: Callable[[float], float] = linear,
        **kwargs
    ):
        self.angle = angle
        self.axis = axis
        self.about_point = about_point or mobject.get_center()
        self.about_edge = about_edge

        super().__init__(
            mobject,
            lag_ratio=lag_ratio,
            rate_func=rate_func,
            **kwargs
        )

    def interpolate_submobject(
        self,
        submob: VMobject,
        start_submob: VMobject,
        alpha: float
    ) -> None:
        # 使用 rate_func 控制绘制比例
        submob.pointwise_become_partial(start_submob, 0, self.rate_func(alpha))

    def interpolate(self, alpha: float) -> None:
        # 执行绘制
        super().interpolate(alpha)

        # 添加整体旋转
        angle = self.rate_func(alpha) * self.angle
        self.mobject.rotate(
            angle,
            axis=self.axis,
            about_point=self.about_point,
            about_edge=self.about_edge,
        )


class RotateShowCreation(InteractiveScene):
    def construct(self):
        # roate
        logo_green = "#87c2a5"
        logo_blue = "#525893"
        logo_red = "#e07a5f"
        logo_black = WHITE
        ds_m = Tex(r"\mathbb{M}", fill_color=logo_black).scale(7)
        ds_m.shift(2.25 * LEFT + 1.5 * UP)
        circle = Circle(color=logo_green, fill_opacity=1).shift(LEFT)
        square = Square(color=logo_blue, fill_opacity=1).shift(UP)
        triangle = Triangle(color=logo_red, fill_opacity=1).shift(RIGHT)
        circle.set_stroke(width=0)
        square.set_stroke(width=0)
        triangle.set_stroke(width=0)
        logo = VGroup(triangle, square, circle, ds_m)
        logo.move_to(ORIGIN)
        self.play(SpinShowCreation(logo,axis=UP,angle=2*PI, run_time=6))
        self.wait()
        # test
        self.play(RotatingShowCreateV3(Circle(),axis=UP,run_time=6, rate_func=linear))


