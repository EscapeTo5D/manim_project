from typing import Callable, Tuple
from  manim_imports_ext import *


class ImplicitSurface(Surface):
    def __init__(
            self,
            implicit_func: Callable[[float, float, float], float],
            x_range: Tuple[float, float] = (-2, 2),
            y_range: Tuple[float, float] = (-2, 2),
            z_range: Tuple[float, float] = (-2, 2),
            resolution: Tuple[int, int, int] = (50, 50, 50),
            iso_value: float = 0.0,
            **kwargs
    ):
        self.implicit_func = implicit_func
        self.x_range = x_range
        self.y_range = y_range
        self.z_range = z_range
        self.volume_resolution = resolution
        self.iso_value = iso_value

        # 转换为参数化表面
        super().__init__(**kwargs)

    def init_points(self):
        """使用 Marching Cubes 算法生成表面"""
        vertices, faces = self.marching_cubes()

        # 设置顶点
        self.set_points(vertices)

        # 计算法向量所需的偏导数点
        self.compute_gradient_points(vertices)

        # 设置三角形索引
        self.triangle_indices = faces.flatten()

    def marching_cubes(self) -> Tuple[np.ndarray, np.ndarray]:
        """简化版 Marching Cubes 实现"""
        nx, ny, nz = self.volume_resolution

        # 创建3D网格
        x = np.linspace(*self.x_range, nx)
        y = np.linspace(*self.y_range, ny)
        z = np.linspace(*self.z_range, nz)

        # 计算每个网格点的函数值
        volume = np.zeros((nx, ny, nz))
        for i in range(nx):
            for j in range(ny):
                for k in range(nz):
                    volume[i, j, k] = self.implicit_func(x[i], y[j], z[k])

        vertices = []
        faces = []
        vertex_map = {}

        # 遍历每个立方体
        for i in range(nx - 1):
            for j in range(ny - 1):
                for k in range(nz - 1):
                    # 获取立方体8个顶点的值
                    cube_values = [
                        volume[i, j, k],  # 0
                        volume[i + 1, j, k],  # 1
                        volume[i + 1, j + 1, k],  # 2
                        volume[i, j + 1, k],  # 3
                        volume[i, j, k + 1],  # 4
                        volume[i + 1, j, k + 1],  # 5
                        volume[i + 1, j + 1, k + 1],  # 6
                        volume[i, j + 1, k + 1]  # 7
                    ]

                    cube_coords = [
                        [x[i], y[j], z[k]],
                        [x[i + 1], y[j], z[k]],
                        [x[i + 1], y[j + 1], z[k]],
                        [x[i], y[j + 1], z[k]],
                        [x[i], y[j], z[k + 1]],
                        [x[i + 1], y[j], z[k + 1]],
                        [x[i + 1], y[j + 1], z[k + 1]],
                        [x[i], y[j + 1], z[k + 1]]
                    ]

                    # 生成该立方体的三角形
                    cube_faces = self.process_cube(
                        cube_values, cube_coords, vertices, vertex_map
                    )
                    faces.extend(cube_faces)

        return np.array(vertices), np.array(faces)

    def process_cube(self, values, coords, vertices, vertex_map):
        """处理单个立方体，生成三角形面片"""
        # 判断每个顶点是否在表面内部
        inside = [v < self.iso_value for v in values]

        # 如果所有点都在内部或外部，无交点
        if all(inside) or not any(inside):
            return []

        # 简化：只处理基本情况
        # 实际实现需要完整的 Marching Cubes 查找表
        edge_vertices = []

        # 检查12条边是否与表面相交
        edges = [
            (0, 1), (1, 2), (2, 3), (3, 0),  # 底面
            (4, 5), (5, 6), (6, 7), (7, 4),  # 顶面
            (0, 4), (1, 5), (2, 6), (3, 7)  # 竖直边
        ]

        for i, (v1, v2) in enumerate(edges):
            if inside[v1] != inside[v2]:  # 边跨越表面
                # 线性插值找交点
                t = (self.iso_value - values[v1]) / (values[v2] - values[v1])
                intersection = [
                    coords[v1][j] + t * (coords[v2][j] - coords[v1][j])
                    for j in range(3)
                ]

                edge_key = (v1, v2) if v1 < v2 else (v2, v1)

                if edge_key not in vertex_map:
                    vertex_map[edge_key] = len(vertices)
                    vertices.append(intersection)

                edge_vertices.append(vertex_map[edge_key])

        # 根据交点生成三角形（简化版）
        # 实际需要使用完整的三角形查找表
        faces = []
        if len(edge_vertices) >= 3:
            # 简单三角剖分
            for i in range(1, len(edge_vertices) - 1):
                faces.append([edge_vertices[0], edge_vertices[i], edge_vertices[i + 1]])

        return faces

    def compute_gradient_points(self, vertices):
        """计算梯度点用于法向量计算"""
        epsilon = 1e-6
        n_vertices = len(vertices)

        self.data = {
            'du_point': np.zeros((n_vertices, 3)),
            'dv_point': np.zeros((n_vertices, 3)),
        }

        for i, point in enumerate(vertices):
            x, y, z = point

            # 计算数值梯度
            grad_x = (self.implicit_func(x + epsilon, y, z) -
                      self.implicit_func(x - epsilon, y, z)) / (2 * epsilon)
            grad_y = (self.implicit_func(x, y + epsilon, z) -
                      self.implicit_func(x, y - epsilon, z)) / (2 * epsilon)
            grad_z = (self.implicit_func(x, y, z + epsilon) -
                      self.implicit_func(x, y, z - epsilon)) / (2 * epsilon)

            # 法向量归一化
            normal = np.array([grad_x, grad_y, grad_z])
            norm = np.linalg.norm(normal)
            if norm > 1e-10:
                normal /= norm
            else:
                normal = np.array([0.0, 0.0, 1.0])  # 默认法向量

            # 构造两个切向量
            if abs(normal[0]) < 0.9:
                tangent1 = np.cross(normal, [1, 0, 0])
            else:
                tangent1 = np.cross(normal, [0, 1, 0])
            tangent1 /= np.linalg.norm(tangent1)
            tangent2 = np.cross(normal, tangent1)

            self.data['du_point'][i] = point + epsilon * tangent1
            self.data['dv_point'][i] = point + epsilon * tangent2


class ImplicitSurfaceScene(Scene):
    def construct(self):
        def sphere_implicit(x, y, z):
            """球面: x² + y² + z² - r² = 0"""
            return x ** 2 + y ** 2 + z ** 2 - 1.0

        sphere_surface = ImplicitSurface(
            sphere_implicit,
            x_range=(-1.5, 1.5),
            y_range=(-1.5, 1.5),
            z_range=(-1.5, 1.5),
            resolution=(30, 30, 30)
        )
        self.add(sphere_surface)
        self.wait()