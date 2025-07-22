from __future__ import annotations
from manim_imports_ext import *
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Callable
    from manimlib.typing import Vect3, Vect3Array
def rotation_matrix_4d(angle_xw=0, angle_yw=0.0, angle_zw=0, angle_xy=0, angle_yz=0, angle_xz=0,):
    r_xw = np.array([
        [np.cos(angle_xw), 0, 0, np.sin(angle_xw)],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [-np.sin(angle_xw), 0, 0, np.cos(angle_xw)]
    ])
    r_yw = np.array([
        [1, 0, 0, 0],
        [0, np.cos(angle_yw), 0, -np.sin(angle_yw)],
        [0, 0, 1, 0],
        [0, np.sin(angle_yw), 0, np.cos(angle_yw)]
    ])
    r_zw = np.array([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, np.cos(angle_zw), -np.sin(angle_zw)],
        [0, 0, np.sin(angle_zw), np.cos(angle_zw)]
    ])
    r_xy = np.array([
        [np.cos(angle_xy), np.sin(angle_xy), 0, 0],
        [-np.sin(angle_xy), np.cos(angle_xy), 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ])
    r_yz = np.array([
        [1, 0, 0, 0],
        [0, np.cos(angle_yz), np.sin(angle_yz), 0],
        [0, -np.sin(angle_yz), np.cos(angle_yz), 0],
        [0, 0, 0, 1]
    ])
    r_xz = np.array([
        [np.cos(angle_xz), 0, -np.sin(angle_xz), 0],
        [0, 1, 0, 0],
        [np.sin(angle_xz), 0, np.cos(angle_xz), 0],
        [0, 0, 0, 1]
    ])
    return r_xw @ r_yw @ r_zw @ r_xy @ r_yz @ r_xz
def project_4d_to_3d(vertices_4d, distance=1.0):
    """透视投影公式: scale = d/(d+w)"""
    vertices_3d = []
    for vertex in vertices_4d:
        x, y, z, w = vertex
        scale = distance / (distance + w)
        vertices_3d.append([x * scale, y * scale, z * scale])
    return np.array(vertices_3d)

def get_tesseract_vertices(side_length: float = 2.0):
    """返回边长为 side_length 的超立方体 4D 顶点数组"""
    half = side_length / 2
    vertices = []
    for i in range(16):
        x = half if (i & 1) else -half
        y = half if (i & 2) else -half
        z = half if (i & 4) else -half
        w = half if (i & 8) else -half
        vertices.append([x, y, z, w])
    return np.array(vertices)


def get_tesseract_edges():
    """汉明距离判断"""
    edges = []
    for i in range(16):
        for k in range(4):
            j = i ^ (1 << k)
            if i < j:
                edges.append((i, j))
    return edges

def get_tesseract_faces():
    """
    返回 tesseract 的所有面，每个面是由 4 个顶点组成的列表 [i, j, k, l]。
    顶点编号为 0~15。
    """
    faces = []
    for base in range(16):
        for i in range(4):
            for j in range(i + 1, 4):
                a = base
                b = base ^ (1 << i)
                c = base ^ (1 << j)
                d = base ^ (1 << i) ^ (1 << j)

                # 为避免重复，只在 base 是四个点中最小的情况下添加
                if base < min(b, c, d):
                    faces.append([a, b, d, c])  # 顺序：a → b → d → c 构成正方形
    return faces

class Hypercube(VGroup3D):
    def __init__(
            self,
            side_length: float = 2,
            distance: float = 3.0,
            fill_color: ManimColor = BLUE_D,
            stroke_color: ManimColor = YELLOW_C,
            fill_opacity: float = 1,
            stroke_width: float = 0,

            **kwargs
    ):
        self.side_length = side_length
        self.distance = distance
        self.vertices_4d = get_tesseract_vertices(side_length)
        self.faces = get_tesseract_faces()
        self.R = rotation_matrix_4d()
        self.style = dict(
            fill_color=fill_color,
            fill_opacity=fill_opacity,
            stroke_width=stroke_width,
            stroke_color=stroke_color,
            **kwargs
        )
        super().__init__(*self.get_polygons(), **self.style)

    def get_polygons(self,):
        rotated = self.vertices_4d @ self.R.T
        projected_vertices = project_4d_to_3d(rotated, distance=self.distance)
        polygons = VGroup()
        for face_indices in self.faces:
            face_vertices = [projected_vertices[i] for i in face_indices]
            polygon = Polygon(*face_vertices, **self.style)
            polygons.add(polygon)
        return polygons

    def apply_4d_rotation(self, rotation_matrix):
        """应用4D旋转矩阵并更新显示"""
        self.R = rotation_matrix
        # 清除现有的多边形
        self.clear()
        # 添加新的多边形
        self.add(*self.get_polygons())
        return self

    def rotate_4d(
            self,
            angle_xw: float = 0.0,
            angle_yw: float = 0.0,
            angle_zw: float = 0.0,
            angle_xy: float = 0.0,
            angle_yz: float = 0.0,
            angle_xz: float = 0.0,
            **kwargs
    ):
        """
        4D旋转方法，类似于Manim的rotate方法
        """
        rotation = rotation_matrix_4d(
            angle_xw, angle_yw, angle_zw,
            angle_xy, angle_yz, angle_xz
        )
        new_R = self.R @ rotation
        return self.apply_4d_rotation(new_R)

    def rotate_in_plane(self, angle: float, plane: str = "xw", **kwargs):
        """
        在指定平面内旋转，类似于3D的rotate方法

        Args:
            angle: 旋转角度
            plane: 旋转平面，可选: "xw", "yw", "zw", "xy", "yz", "xz"
        """
        angles = {f"angle_{plane}": angle}
        return self.rotate_4d(**angles, **kwargs)