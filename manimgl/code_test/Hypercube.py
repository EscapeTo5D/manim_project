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



class VHypercube(VGroup):
    def __init__(
        self,
        t_tracker: ValueTracker = None,
        side_length: float = 1.0,
        fill_color: ManimColor = BLUE,
        fill_opacity: float = 0.7,
        stroke_width: float = 0.1,
        angle_xw=0.3,
        angle_yw=0.0,
        angle_zw=0.0,
        angle_xy=0.3,
        angle_yz=0.0,
        angle_xz=0.0,
        distance: float = 3.0,
        **kwargs,
    ):
        super().__init__(**kwargs)

        self.vertices_4d = get_tesseract_vertices(side_length)
        self.faces = get_tesseract_faces()
        self.t_tracker = t_tracker or ValueTracker(0)

        self.fill_color = fill_color
        self.fill_opacity = fill_opacity
        self.stroke_width = stroke_width
        self.distance = distance

        self.angle_params = dict(
            angle_xw=angle_xw,
            angle_yw=angle_yw,
            angle_zw=angle_zw,
            angle_xy=angle_xy,
            angle_yz=angle_yz,
            angle_xz=angle_xz,
        )

        self.add(self._build_faces())

    def _build_faces(self):
        return always_redraw(lambda: self._get_faces_at_t(self.t_tracker.get_value()))

    def _get_faces_at_t(self, t):
        R = rotation_matrix_4d(**{k: v * t for k, v in self.angle_params.items()})
        rotated = self.vertices_4d @ R.T
        projected = project_4d_to_3d(rotated, distance=self.distance)

        group = VGroup()
        for indices in self.faces:
            pts = [projected[i] for i in indices]
            poly = Polygon(
                *pts,
                fill_color=self.fill_color,
                fill_opacity=self.fill_opacity,
                stroke_width=self.stroke_width,
            )
            group.add(poly)
        return group


class HypercubeScene(Scene):
    def construct(self):
        # 初始化
        frame = self.camera.frame
        frame.set_euler_angles(
            theta=-30 * DEGREES,
            phi=70 * DEGREES,
        )
        vertices_4d = get_tesseract_vertices()
        faces = get_tesseract_faces()
        t_tracker = ValueTracker(0)
        def get_edges_group(t):
            R = rotation_matrix_4d(
                angle_zw=-t * 0.3,
                angle_xy=t * 0.3,
            )
            rotated = vertices_4d @ R.T
            projected = project_4d_to_3d(rotated, distance=3.0)
            faces_group = VGroup()
            for face_indices in faces:
                points = [projected[i] for i in face_indices]
                polygon = Polygon(*points, fill_color=BLUE_D, fill_opacity=0.5, stroke_color=YELLOW_C, stroke_width=0)
                faces_group.add(polygon)
            return faces_group
        speed = 1
        t_tracker.add_updater(lambda m, dt: m.increment_value(speed * dt))
        lines = always_redraw(lambda: get_edges_group(t_tracker.get_value()),)
        self.add(lines, t_tracker)
        self.wait(5*PI)

class ShowHypercube(ThreeDScene):
    def construct(self):
        # 初始化
        frame = self.camera.frame
        frame.set_euler_angles(
            theta=-30 * DEGREES,
            phi=70 * DEGREES,
        )
        hypercube = Hypercube().move_to(LEFT * 2)
        self.play(
            hypercube.animate.rotate_in_plane(PI / 2, "xw"),
            run_time=2
        )
        self.add(VCube(side_length=3).next_to(hypercube, RIGHT*2))

class TestScene(ThreeDScene):
    def construct(self):
        # test
        vertices = get_tesseract_vertices(2)
        faces = get_tesseract_faces()
        face = faces[0]
        face_points = [project_4d_to_3d(vertices)[i] for i in face]
        poly = Polygon(*face_points, fill_color=BLUE, fill_opacity=0.8,
                       stroke_color=YELLOW, stroke_width=2)
        self.add(poly)
        self.wait()
