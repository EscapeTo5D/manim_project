from manim_imports_ext import *
import numpy as np
from collections import defaultdict
# ———— 配置参数 ————
sphere_radius = 3.0
offset = 0.0
ribbon_width = 0.05
filepath = r"D:\\manim_project\\manimgl\\einstein_scene\\constellation_star\bound_in_20.txt"

class ConstellationVisualization(ThreeDScene):
    def construct(self):
        def sph_xyz(ra_h, dec_d, radius=3):
            ra = math.radians(ra_h * 15.0)
            dec = math.radians(dec_d)
            x = radius * np.cos(dec) * math.cos(ra)
            y = radius * np.cos(dec) * math.sin(ra)
            z = radius * math.sin(dec)
            return np.array([x, y, z])
        def load_constellation_data(target_constellation=None):
            segments = defaultdict(list)
            with open(filepath, 'r', encoding='utf-8') as f:
                for lineno, line in enumerate(f, 1):
                    line = line.strip()
                    if not line:
                        continue
                    parts = line.split()
                    if len(parts) >= 3:
                        ra_h, dec_d, constellation = parts[0], parts[1], parts[2]
                        if target_constellation and constellation != target_constellation:
                            continue
                        segments[constellation].append((float(ra_h), float(dec_d)))
            return segments
        # 读取并按星座名分组
        constellation_lines = {}
        all_constellations_lines = VGroup()
        segments = load_constellation_data()
        for constellation, boundary_points in segments.items():
            points = [sph_xyz(ra, dec) for ra, dec in boundary_points]
            line = VMobject()
            line.set_points_as_corners(points)
            line.close_path()
            line.set_stroke(WHITE, width=1)
            constellation_lines[constellation] = line
            all_constellations_lines.add(line)
        sphere = Sphere(radius=3, resolution=(50, 100))
        milky_way = (TexturedSurface(sphere, "D:\\manim_project\\images\\raster_image\\milky_way.png", ))
        self.add(milky_way)
        self.play(Rotating(milky_way, axis=OUT, angle=PI)
            ,run_time=8)
        self.play(Transform(milky_way, milky_way.scale(2)))