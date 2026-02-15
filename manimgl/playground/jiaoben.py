import numpy as np

def get_tesseract_vertices(side_length: float = 1000.0):
    """返回边长为 side_length 的超立方体 4D 顶点数组"""
    half = side_length
    vertices = []
    for i in range(16):
        x = half if (i & 1) else -half
        y = half if (i & 2) else -half
        z = half if (i & 4) else -half
        w = half if (i & 8) else -half
        vertices.append([x, y, z, w])
    return np.array(vertices)

def get_tesseract_faces():
    """构造超正方体的二维正方形面（返回顶点索引列表）"""
    faces = []
    for i in range(16):  # 遍历所有 4D 顶点编号（0 到 15）
        for a in range(4):
            for b in range(a + 1, 4):  # 两个方向（a 和 b）决定面所在平面
                # 只考虑固定 i 的其他两个维度不变，a 和 b 两个维度变换
                # 计算面上的四个顶点：i, i^2^a, i^2^b, i^2^a^2^b
                j = i ^ (1 << a)
                k = i ^ (1 << b)
                l = i ^ (1 << a) ^ (1 << b)

                face = [i, j, l, k]  # 注意点的顺序是构成面用的环
                if sorted(face) not in [sorted(f) for f in faces]:  # 避免重复面
                    faces.append(face)
    return faces

def get_tesseract_faces_v2():
    """自动生成 Tesseract 的 2D 面（正方形）"""
    faces = set()
    for i in range(16):
        for j in range(i + 1, 16):
            diff = i ^ j
            if bin(diff).count("1") == 2:
                bit1 = diff & -diff
                bit2 = diff ^ bit1
                k = i ^ bit1
                l = i ^ bit2
                face = tuple(sorted([i, k, j, l]))
                faces.add(face)
    return list(faces)

def get_tesseract_edges():
    """汉明距离判断"""
    edges = []
    for i in range(16):
        for k in range(4):
            j = i ^ (1 << k)
            if i < j:
                edges.append((i, j))
    return edges

def get_tesseract_vertices_v2():
    """初始化顶点"""
    vertices = []
    for i in range(16):
        x = 1 if (i & 1) else -1
        y = 1 if (i & 2) else -1
        z = 1 if (i & 4) else -1
        w = 1 if (i & 8) else -1
        vertices.append([x, y, z, w])
    return np.array(vertices)
faces = get_tesseract_faces()
face = faces[16]  # 例如第一个面: [0, 1, 3, 2]

vertices = get_tesseract_vertices()

print(vertices)


