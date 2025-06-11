from manimlib import *
from typing import Callable
class RotatingCreate(Animation):
    """
    同时整体创建整体旋转
    """

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
    按顺序逐渐创建整体旋转
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


class ShowRotatingCreate(ShowCreation):
    """
    按顺序逐渐创建单体旋转
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