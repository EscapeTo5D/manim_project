from manim import *


class Chaos(ThreeDScene):
    def construct(self):
        # 轨迹颜色定义
        self.colors = ["#FFFF00", "#FF7F00", "#00FF00", "#0000FF", "#00FFFF", "#FF0000", "#8B00FF"]

        # 三维坐标系
        axes = self.axes = ThreeDAxes(
            x_range=[-50, 50, 20],
            y_range=[-50, 50, 20],
            z_range=[-10, 110, 20],
        )

        # 初始化摄像头角度
        self.set_camera_orientation(phi=65 * DEGREES,
                                    theta=110 * DEGREES,
                                    frame_center=OUT * 1.6,
                                    zoom=1.2)

        # 初始化迭代用的小球的VGroup
        self.add_bodies()
        # 准备小球的轨迹，放入场景
        self.add_trajectories()
        #
        # # 先迭代运行5000次，让轨迹呈现出蝴蝶效果
        # for i in range(100):
        #     self.update_bodies(self.bodies, 0.01)  # 球的步长
        #     self.update_trajectorys(self.trajs, 0.01)  # 轨迹的更新步长

        # 将小球放入场景
        self.bodies.add_updater(self.update_bodies)
        self.add(self.bodies)

        self.wait(3)
        # 开始动画，主要是晃动摄像头，调整摄像头位置
        self.move_camera(phi=110 * DEGREES, theta=190 * DEGREES, run_time=3, rate_func=smooth)
        self.wait(0.5)
        self.move_camera(phi=65 * DEGREES, theta=110 * DEGREES, zoom=2, run_time=6, rate_func=smooth)
        self.wait(1)
        self.move_camera(phi=260 * DEGREES, theta=460 * DEGREES, run_time=10, rate_func=smooth)
        self.wait(1)
        self.move_camera(zoom=3, run_time=5, rate_func=smooth)
        self.move_camera(phi=550 * DEGREES, theta=470 * DEGREES, run_time=10, rate_func=smooth)
        self.wait(1)
        self.move_camera(phi=100 * DEGREES, theta=550 * DEGREES, run_time=10, zoom=4, rate_func=smooth)
        self.wait(1)

        self.move_camera(phi=65 * DEGREES, theta=110 * DEGREES, run_time=6.5, zoom=1,
                         rate_func=smooth)
        self.wait(3)

    # 初始化迭代用的小球
    def add_bodies(self):
        # 三个不同颜色的小球，放在相邻位置
        colors = self.colors
        bodies = self.bodies = VGroup()
        centers = self.get_initial_positions()

        for color, center in zip(colors, centers):
            body = Sphere(radius=0.01)
            body.set_color(color)
            body.set_opacity(0.75)
            body.pos = center
            body.move_to(self.axes.coords_to_point(*(body.pos)))
            bodies.add(body)

    # 三个小球初始位置只相隔一点点
    def get_initial_positions(self):
        return [
            [0.0, 1.0, 0.0],
            [0.0, 1.01, 0.0],
            [0.0, 1.02, 0.0],
            [0.0, 1.03, 0.0],
            [0.0, 1.04, 0.0],
            [0.0, 1.05, 0.0],
            [0.0, 1.06, 0.0],
        ]

    # 准备轨迹
    def add_trajectories(self):
        trajs = self.trajs = VGroup()

        # 轨迹描绘的就是：小球每次迭代的位置的连线
        def update_trajectory(traj):
            new_point = traj.body.get_center()
            # 找到前一轮轨迹的终端，判断：如果本次小球移动的距离太小，就不更新了
            if np.linalg.norm(new_point - traj.get_points()[-1]) > 0.01:
                traj.add_smooth_curve_to(new_point)

        # 每个小球对应一条轨迹
        for body in self.bodies:
            traj = VMobject()
            traj.body = body
            traj.start_new_path(body.get_center())
            traj.set_stroke(body.get_color(), 1, opacity=0.75)
            traj.add_updater(update_trajectory)
            trajs.add(traj)
            self.add(traj)

    # 三条轨迹更新，用于开头5000次迭代，后续动画过程中的轨迹更新，就靠轨迹自己的updater了
    def update_trajectorys(self, trajs, dt):
        for traj in self.trajs:
            new_point = traj.body.get_center()
            if np.linalg.norm(new_point - traj.get_points()[-1]) > 0.001:
                traj.add_smooth_curve_to(new_point)

    # 三个小球位置更新
    def update_bodies(self, bodies, dt):
        # 为洛伦兹方程选取以下三个参数
        paramSigma = 10.0
        paramR = 28.0
        paramB = 8.0 / 3.0

        # 迭代计算洛伦兹方程，得到新的小球位置坐标
        for body in bodies:
            x, y, z = body.pos
            dx = paramSigma * (y - x)
            dy = paramR * x - y - x * z
            dz = x * y - paramB * z
            delta = np.array([dx, dy, dz])
            body.pos += delta * 0.01

            body.move_to(self.axes.coords_to_point(*(body.pos)))
        return bodies
