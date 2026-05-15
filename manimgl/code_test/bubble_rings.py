from manim_imports_ext import *
import numpy as np

class StaticCliffordTorusHD(ThreeDScene):
    def construct(self):
        # === 参数设置 ===
        def inverse_stereographic(p):
            p_dot = np.dot(p, p)
            k = 2.0 / (1.0 + p_dot)
            return np.array([k * p[0], k * p[1], k * p[2], k - 1.0]), k
        def torus_4d(p4):
            xy = np.linalg.norm(p4[:2])
            zw = np.linalg.norm(p4[2:])
            if xy == 0 or zw == 0:
                return 1000.0
            d1 = xy / zw - 1.0
            d2 = zw / xy - 1.0
            return (d2 if d1 >= 0 else -d1) / PI
        def fix_distance(d, k):
            sn = np.sign(d)
            d = abs(d) / k * 1.82 + 1.0
            return (np.sqrt(d) - 1.0) * (5.0 / 3.0) * sn
        def smax(a, b, r):
            u = np.maximum([r + a, r + b], [0, 0])
            return min(-r, max(a, b)) + np.linalg.norm(u)
        def map_sdf(p, t=0.5):
            p4, k = inverse_stereographic(p)
            angle = t * -PI / 2
            c, s = np.cos(angle), np.sin(angle)
            p4[1], p4[2] = c * p4[1] + s * p4[2], c * p4[2] - s * p4[1]  # zy
            p4[0], p4[3] = c * p4[0] + s * p4[3], c * p4[3] - s * p4[0]  # xw
            d = abs(torus_4d(p4)) - 0.2
            return smax(fix_distance(d, k), np.linalg.norm(p) - max_dist, 0.2)
        # === 采样 ===
        cam_pos = np.array([1.8, 5.5, -5.5]) * 1.75
        cam_tar = np.array([0.0, 0.0, 0.0])
        cam_up = np.array([-1.0, 0.0, -1.5])
        forward = normalize(cam_tar - cam_pos)  # Z 轴
        right = normalize(np.cross(forward, cam_up))  # X 轴
        up = np.cross(right, forward)  # Y 轴
        rot_matrix = np.array([right, up, -forward]).T  # 转置形成方向列向量
        rot = Rotation.from_matrix(rot_matrix)
        self.camera.frame.set_orientation(rot)
        cam_pos = np.array([1.8, 5.5, -5.5]) * 1.75
        grid_size = 200  # 降低分辨率，提升性能
        bound = 5
        threshold = 0.008
        max_dist = 1.9
        dot_radius = 0.04
        skip = 30  # 提高跳跃率减少点数
        def get_surface_points(t):
            points = []
            step = 2 * bound / grid_size
            for xi in range(grid_size):
                x = (xi - grid_size / 2) * step
                for yi in range(grid_size):
                    y = (yi - grid_size / 2) * step
                    for zi in range(grid_size):
                        z = (zi - grid_size / 2) * step
                        p = np.array([x, y, z])
                        if np.linalg.norm(p) > max_dist + 0.3:
                            continue
                        d = map_sdf(p, t)
                        if abs(d) < threshold:
                            points.append(p * 1.6)
            return points
        t0 = 0.0
        points = get_surface_points(t0)
        dots = Group()
        for i, p in enumerate(points):
            if i % skip != 0:
                continue
            t = (np.linalg.norm(p - cam_pos) / 10) % 1.0
            color_vec = 0.5 + 0.5 * np.cos(2 * PI * (np.array([1.0, 1.0, 1.0]) * t + [0.0, 0.33, 0.67]))
            dot = DotCloud(p, radius=dot_radius, color=rgb_to_color(np.clip(color_vec, 0, 1)))
            dot.set_opacity(0.6)
            dots.add(dot)
        self.add(dots)
        # 更新
        def update_dots(mob, dt):
            nonlocal t0
            t0 = (t0 + dt * 0.1) % 1.0  # 每秒转一圈
            new_points = get_surface_points(t0)
            mob.submobjects.clear()
            for i, p in enumerate(new_points):
                if i % skip != 0:
                    continue
                t = (np.linalg.norm(p - cam_pos) / 10) % 1.0
                color_vec = 0.5 + 0.5 * np.cos(2 * PI * (np.array([1.0, 1.0, 1.0]) * t + [0.0, 0.33, 0.67]))
                dot = DotCloud(p, radius=dot_radius, color=rgb_to_color(np.clip(color_vec, 0, 1)))
                dot.set_opacity(0.6)
                mob.add(dot)
        # dh
        dots.add_updater(update_dots)
        self.wait(4)  # 播放 8 秒动画

# class SphereStaticCliffordTorusHD(ThreeDScene):
#     def construct(self):
#         # === 参数设置 ===
#         def inverse_stereographic(p):
#             p_dot = np.dot(p, p)
#             k = 2.0 / (1.0 + p_dot)
#             return np.array([k * p[0], k * p[1], k * p[2], k - 1.0]), k
#         def torus_4d(p4):
#             xy = np.linalg.norm(p4[:2])
#             zw = np.linalg.norm(p4[2:])
#             if xy == 0 or zw == 0:
#                 return 1000.0
#             d1 = xy / zw - 1.0
#             d2 = zw / xy - 1.0
#             return (d2 if d1 >= 0 else -d1) / PI
#         def fix_distance(d, k):
#             sn = np.sign(d)
#             d = abs(d) / k * 1.82 + 1.0
#             return (np.sqrt(d) - 1.0) * (5.0 / 3.0) * sn
#         def smax(a, b, r):
#             u = np.maximum([r + a, r + b], [0, 0])
#             return min(-r, max(a, b)) + np.linalg.norm(u)
#         def map_sdf(p, t=0.5):
#             p4, k = inverse_stereographic(p)
#             angle = t * -PI / 2
#             c, s = np.cos(angle), np.sin(angle)
#             p4[1], p4[2] = c * p4[1] + s * p4[2], c * p4[2] - s * p4[1]  # zy
#             p4[0], p4[3] = c * p4[0] + s * p4[3], c * p4[3] - s * p4[0]  # xw
#             d = abs(torus_4d(p4)) - 0.2
#             return smax(fix_distance(d, k), np.linalg.norm(p) - max_dist, 0.2)
        
#         # === 采样 ===
#         cam_pos = np.array([1.8, 5.5, -5.5]) * 1.75
#         cam_tar = np.array([0.0, 0.0, 0.0])
#         cam_up = np.array([-1.0, 0.0, -1.5])
#         forward = normalize(cam_tar - cam_pos)  # Z 轴
#         right = normalize(np.cross(forward, cam_up))  # X 轴
#         up = np.cross(right, forward)  # Y 轴
#         rot_matrix = np.array([right, up, -forward]).T  # 转置形成方向列向量
#         rot = Rotation.from_matrix(rot_matrix)
#         self.camera.frame.set_orientation(rot)
#         threshold = 0.01
#         max_dist = 1.9
#         dot_radius = 0.02
#         skip = 1
#         def get_surface_points(t):
#             """球坐标采样：更均匀的角度分布"""
#             points = []
#             # 球坐标采样参数
#             r_samples = 100      # 径向采样数
#             theta_samples = 100  # 极角采样数
#             phi_samples = 100    # 方位角采样数
#             # 使用球坐标进行采样
#             for ri in range(r_samples):
#                 r = 0.1 + (max_dist - 0.1) * ri / (r_samples - 1)
#                 for ti in range(theta_samples):
#                     theta = PI * ti / (theta_samples - 1)
#                     for pi in range(phi_samples):
#                         phi = 2 * PI * pi / phi_samples
#                         # 球坐标转笛卡尔坐标
#                         x = r * np.sin(theta) * np.cos(phi)
#                         y = r * np.sin(theta) * np.sin(phi)
#                         z = r * np.cos(theta)
#                         p = np.array([x, y, z])
#                         d = map_sdf(p, t)
#                         if abs(d) < threshold:
#                             points.append(p * 1.6)
#             return points
#         t0 = 0.0
#         points = get_surface_points(t0)
#         dots = Group()
#         for i, p in enumerate(points):
#             if i % skip != 0:
#                 continue
#             t = (np.linalg.norm(p - cam_pos) / 10) % 1.0
#             color_vec = 0.5 + 0.5 * np.cos(2 * PI * (np.array([1.0, 1.0, 1.0]) * t + [0.0, 0.33, 0.67]))
#             dot = DotCloud(p, radius=dot_radius, color=rgb_to_color(np.clip(color_vec, 0, 1)))
#             dot.set_opacity(1)
#             dots.add(dot)
#         self.add(dots)
#         # 更新
#         def update_dots(mob, dt):
#             nonlocal t0
#             t0 = (t0 + dt * 0.1) % 1.0  # 每秒转一圈
#             new_points = get_surface_points(t0)
#             mob.submobjects.clear()
#             for i, p in enumerate(new_points):
#                 if i % skip != 0:
#                     continue
#                 t = (np.linalg.norm(p - cam_pos) / 10) % 1.0
#                 color_vec = 0.5 + 0.5 * np.cos(2 * PI * (np.array([1.0, 1.0, 1.0]) * t + [0.0, 0.33, 0.67]))
#                 dot = DotCloud(p, radius=dot_radius, color=rgb_to_color(np.clip(color_vec, 0, 1)))
#                 dot.set_opacity(1)
#                 mob.add(dot)
        
#         dots.add_updater(update_dots)
#         self.wait(20)

# class StaticCliffordTorusHD(ThreeDScene):
#     def construct(self):
#         # === 参数设置 ===
#         def inverse_stereographic(p):
#             p_dot = np.dot(p, p)
#             k = 2.0 / (1.0 + p_dot)
#             return np.array([k * p[0], k * p[1], k * p[2], k - 1.0]), k
#         def torus_4d(p4):
#             xy = np.linalg.norm(p4[:2])
#             zw = np.linalg.norm(p4[2:])
#             if xy == 0 or zw == 0:
#                 return 1000.0
#             d1 = xy / zw - 1.0
#             d2 = zw / xy - 1.0
#             return (d2 if d1 >= 0 else -d1) / PI
#         def fix_distance(d, k):
#             sn = np.sign(d)
#             d = abs(d) / k * 1.82 + 1.0
#             return (np.sqrt(d) - 1.0) * (5.0 / 3.0) * sn
#         def smax(a, b, r):
#             u = np.maximum([r + a, r + b], [0, 0])
#             return min(-r, max(a, b)) + np.linalg.norm(u)
#         def map_sdf(p, t=0.5):
#             p4, k = inverse_stereographic(p)
#             angle = t * -PI / 2
#             c, s = np.cos(angle), np.sin(angle)
#             p4[1], p4[2] = c * p4[1] + s * p4[2], c * p4[2] - s * p4[1]  # zy
#             p4[0], p4[3] = c * p4[0] + s * p4[3], c * p4[3] - s * p4[0]  # xw
#             d = abs(torus_4d(p4)) - 0.2
#             return smax(fix_distance(d, k), np.linalg.norm(p) - max_dist, 0.2)
#         # === 采样 ===
#         cam_pos = np.array([1.8, 5.5, -5.5]) * 1.75
#         cam_tar = np.array([0.0, 0.0, 0.0])
#         cam_up = np.array([-1.0, 0.0, -1.5])
#         forward = normalize(cam_tar - cam_pos)  # Z 轴
#         right = normalize(np.cross(forward, cam_up))  # X 轴
#         up = np.cross(right, forward)  # Y 轴
#         rot_matrix = np.array([right, up, -forward]).T  # 转置形成方向列向量
#         rot = Rotation.from_matrix(rot_matrix)
#         self.camera.frame.set_orientation(rot)
#         bound = 5
#         threshold = 0.01
#         max_dist = 1.9
#         dot_radius = 0.02
#         skip = 1
#         def get_surface_points(t):
#             """混合采样方法：结合多种策略"""
#             points = []
#             # 方法1：基础网格采样（保持原有逻辑）
#             grid_size =200
#             step = 2 * bound / grid_size
#             for xi in range(grid_size):
#                 x = (xi - grid_size / 2) * step
#                 for yi in range(grid_size):
#                     y = (yi - grid_size / 2) * step
#                     for zi in range(grid_size):
#                         z = (zi - grid_size / 2) * step
#                         p = np.array([x, y, z])
#                         if np.linalg.norm(p) > max_dist + 0.3:
#                             continue
#                         d = map_sdf(p, t)
#                         if abs(d) < threshold:
#                             points.append(p * 1.6)
#             # 方法2：边界补强采样
#             # 在max_dist附近增加采样密度
#             boundary_samples = 0
#             for _ in range(boundary_samples):
#                 # 在球面附近随机采样
#                 theta = np.random.uniform(0, PI)
#                 phi = np.random.uniform(0, 2*PI)
#                 r = np.random.uniform(max_dist - 0.4, max_dist + 0.2)
                
#                 x = r * np.sin(theta) * np.cos(phi)
#                 y = r * np.sin(theta) * np.sin(phi)
#                 z = r * np.cos(theta)
#                 p = np.array([x, y, z])
#                 d = map_sdf(p, t)
#                 if abs(d) < threshold:
#                     points.append(p * 1.6)
#             # 方法3：曲率敏感采样
#             # 基于SDF变化率增加采样点
#             curvature_samples = 1800
#             for _ in range(curvature_samples):
#                 # 随机选择一个已有点的邻域
#                 if len(points) > 10:
#                     base_point = np.random.choice(len(points))
#                     base_pos = points[base_point] / 1.6
#                     # 在其周围采样
#                     for _ in range(5):
#                         offset = np.random.normal(0, 0.1, 3)
#                         p = base_pos + offset
#                         if np.linalg.norm(p) > max_dist + 0.3:
#                             continue
#                         d = map_sdf(p, t)
#                         if abs(d) < threshold:
#                             points.append(p * 1.6)
#             return points
#         t0 = 0.0
#         points = get_surface_points(t0)
#         dots = Group()
#         for i, p in enumerate(points):
#             if i % skip != 0:
#                 continue
#             t = (np.linalg.norm(p - cam_pos) / 10) % 1.0
#             color_vec = 0.5 + 0.5 * np.cos(2 * PI * (np.array([1.0, 1.0, 1.0]) * t + [0.0, 0.33, 0.67]))
#             dot = DotCloud(p, radius=dot_radius, color=rgb_to_color(np.clip(color_vec, 0, 1)))
#             dot.set_opacity(1)
#             dots.add(dot)
#         self.add(dots)
        
#         def update_dots(mob, dt):
#             nonlocal t0
#             t0 = (t0 + dt * 0.1) % 1.0  # 每秒转一圈
#             new_points = get_surface_points(t0)
#             mob.submobjects.clear()
#             for i, p in enumerate(new_points):
#                 if i % skip != 0:
#                     continue
#                 t = (np.linalg.norm(p - cam_pos) / 10) % 1.0
#                 color_vec = 0.5 + 0.5 * np.cos(2 * PI * (np.array([1.0, 1.0, 1.0]) * t + [0.0, 0.33, 0.67]))
#                 dot = DotCloud(p, radius=dot_radius, color=rgb_to_color(np.clip(color_vec, 0, 1)))
#                 dot.set_opacity(1)
#                 mob.add(dot)
        
#         dots.add_updater(update_dots)
#         self.wait(20)

# class StaticCliffordTorusHDi(ThreeDScene):
#     def construct(self):
#         # 精确的相机设置 - 完全匹配shader
#         cam_pos = np.array([1.8, 5.5, -5.5]) * 1.75
#         def create_volumetric_surface():
#             def inverse_stereographic(p):
#                 p_dot = np.dot(p, p)
#                 k = 2.0 / (1.0 + p_dot)
#                 return np.array([k * p[0], k * p[1], k * p[2], k - 1.0]), k
#             def torus_4d(p4):
#                 xy = np.linalg.norm(p4[:2])
#                 zw = np.linalg.norm(p4[2:])
#                 if xy == 0 or zw == 0:
#                     return 1000
#                 d1 = xy / zw - 1.0
#                 d2 = zw / xy - 1.0
#                 d = -d1 if d1 < 0 else d2
#                 return d / PI
#             def fix_distance(d, k):
#                 sn = np.sign(d)
#                 d = abs(d) / k * 1.82 + 1.0
#                 d = np.power(d, 0.5) - 1.0
#                 return d * 5.0 / 3.0 * sn
#             def smax(a, b, r):
#                 u = np.maximum([r + a, r + b], [0, 0])
#                 return min(-r, max(a, b)) + np.linalg.norm(u)
#             def map_sdf(p, t=0.5):
#                 p4, k = inverse_stereographic(p)
#                 angle = t * -PI / 2
#                 c, s = np.cos(angle), np.sin(angle)
#                 p4[1], p4[2] = c * p4[1] + s * p4[2], c * p4[2] - s * p4[1]
#                 p4[0], p4[3] = c * p4[0] + s * p4[3], c * p4[3] - s * p4[0]
#                 d = abs(torus_4d(p4)) - 0.2
#                 d = fix_distance(d, k)
#                 return smax(d, np.linalg.norm(p) - 1.85, 0.2)
#             def spectrum_color(t):
#                 a = np.array([0.5, 0.5, 0.5])
#                 b = np.array([0.5, 0.5, 0.5])
#                 c = np.array([1.0, 1.0, 1.0])
#                 d = np.array([0.0, 0.33, 0.67])
#                 return a + b * np.cos(6.28318 * (c * t + d))
#             def smooth_step(edge0, edge1, x):
#                 t = np.clip((x - edge0) / (edge1 - edge0), 0.0, 1.0)
#                 return t * t * (3.0 - 2.0 * t)
#             surface_points = []
#             surface_colors = []
#             surface_opacities = []
#             grid_size = 100  # 增加精度
#             bound = 2.8
#             print("生成超高精度Clifford环面...")
#             for i in range(grid_size):
#                 for j in range(grid_size):
#                     for k in range(grid_size):
#                         x = (i / grid_size - 0.5) * 2 * bound
#                         y = (j / grid_size - 0.5) * 2 * bound
#                         z = (k / grid_size - 0.5) * 2 * bound
#                         p = np.array([x, y, z])
#                         distance = map_sdf(p)
#                         # 只保留接近表面的点 - 更精确的阈值
#                         if abs(distance) < 0.05:
#                             surface_points.append(p)
#                             # 完整的shader着色计算
#                             ray_pos = p
#                             ray_length = np.linalg.norm(ray_pos - cam_pos)
#                             # 表面发光 - 精确复制shader逻辑
#                             surface_glow = max(0.0, 0.01 - abs(distance)) * 20 +0.02
#                             c = np.array([surface_glow, surface_glow, surface_glow])
#                             c *= np.array([2.8, 4.2, 3.4])
#                             # 累积紫色辉光 - FUDGE_FACTORR / 160
#                             FUDGE_FACTORR = 2.0
#                             c += np.array([0.6, 0.25, 0.7]) * FUDGE_FACTORR / 160.0
#                             # 距离衰减 - smoothstep(20., 7., length(rayPosition))
#                             pos_length = np.linalg.norm(ray_pos)
#                             c *= smooth_step(25.0, 5.0, pos_length)
#                             # 射线长度衰减 - smoothstep(MAX_DIST, .1, rayLength)
#                             MAX_DIST = 20.0
#                             rl = smooth_step(MAX_DIST, 0.1, ray_length)
#                             c *= rl
#                             # 光谱色彩变化 - spectrum(rl * 6. - .6)
#                             spectrum_t = rl * 6.0 - 0.6
#                             spectrum_rgb = spectrum_color(spectrum_t)
#                             c *= spectrum_rgb
#                             # 色调映射和伽马校正 - 精确复制shader
#                             # color = pow(color, vec3(1. / 1.8)) * 2.;
#                             c = np.power(np.maximum(c, 0), 1.0 / 1.8) * 2.0
#                             # color = pow(color, vec3(2.)) * 3.;
#                             c = np.power(np.maximum(c, 0), 2.0) * 3.0
#                             # color = pow(color, vec3(1. / 2.2));
#                             c = np.power(np.maximum(c, 0), 1.0 / 2.2) * 1.5
#                             # 限制颜色范围
#                             c = np.clip(c, 0, 1)
#                             surface_colors.append(c)
#                             # 透明度基于表面接近度和发光强度
#                             opacity = min(1.0, surface_glow * 10.0 + 0.2)
#                             surface_opacities.append(opacity)
#             return surface_points, surface_colors, surface_opacities
#         surface_points, surface_colors, surface_opacities = create_volumetric_surface()
#         # 创建可视化
#         if surface_points:
#             dots = Group()
#             print(f"渲染 {len(surface_points)} 个表面点...")
#             step = 1
#             for i in range(0, len(surface_points), step):
#                 point = surface_points[i]
#                 color = surface_colors[i]
#                 opacity = surface_opacities[i]
#                 if np.sum(color) > 0.0001:  # 过滤掉黑色或接近黑的点
#                     dot = DotCloud(
#                         points=np.array([point]),  # ✅ 注意是 points，不是 point
#                         radius=0.012,
#                         color=rgb_to_color(color)
#                     )
#                     dot.set_opacity(opacity)
#                     dots.add(dot)
#             self.add(dots)
