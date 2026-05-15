# 项目约定

> 项目位置：`D:\GitHub\manim_project\manimgl`

## manim_imports_ext.py

所有 Scene 文件统一使用此导入文件：

```python
from manim_imports_ext import *
```

**内容**：

```python
from manimlib import *
from animations import SpinShowCreation, ShowRotatingCreate, RotatingCreate, SpinInFromNothing
from typing import Callable, Iterable, Tuple, Union
from mobject import ComplexSurfaceWireframe, CalabiYauSurface, Hypercube
from utils import spiral_path, rotation_matrix_4d
```

**设计原则**：
- 统一导入点，避免每个文件重复导入
- 自定义组件（`animations`、`mobject`、`utils`）与 `manimlib` 标准库隔离
- 新增自定义组件只需修改此文件

---

## 自定义 Mobject

| 组件 | 描述 |
|------|------|
| `Hypercube` | 4D 超立方体的 3D 投影可视化 |
| `CalabiYauSurface` | 卡拉比-丘流形（复数曲面） |
| `ComplexSurfaceWireframe` | 自定义曲面的线框渲染 |

## 自定义动画

| 动画 | 描述 |
|------|------|
| `SpinShowCreation` | 旋转创建 |
| `ShowRotatingCreate` | 带旋转的创建显示 |
| `RotatingCreate` | 旋转创建变体 |
| `SpinInFromNothing` | 从无到有旋转出现 |

## 自定义工具函数

| 函数 | 描述 |
|------|------|
| `spiral_path` | 螺旋路径生成 |
| `rotation_matrix_4d` | 4D 旋转矩阵 |

---

## Scene 编写规范

### 标准模板

```python
from manim_imports_ext import *

class PythagoreanTheorem(Scene):
    def construct(self):
        # 标题和公式
        title = Text("勾股定理", font_size=72)
        formula = Tex("a^2 + b^2 = c^2", font_size=48)
        formula.next_to(title, DOWN)
        self.add(title, formula)
        self.wait(1.5)

        # 构建直角三角形并标注边长
        triangle = Polygon(ORIGIN, RIGHT * 3, UP * 4,
            stroke_width=4, fill_color=BLUE, fill_opacity=0.3)
        triangle.shift(LEFT * 2)
        a_label = Tex("a=3", color=RED, font_size=36)
        b_label = Tex("b=4", color=GREEN, font_size=36)
        a_label.next_to(triangle, DOWN, buff=0.3)
        b_label.next_to(triangle, LEFT, buff=0.3)
        self.play(ShowCreation(triangle), Write(a_label), Write(b_label))

        # 在三边上构建正方形，展示面积关系
        square_a = Square(side_length=3, fill_color=RED, fill_opacity=0.3)
        square_b = Square(side_length=4, fill_color=GREEN, fill_opacity=0.3)
        # ...定位逻辑...
        self.play(ShowCreation(square_a), ShowCreation(square_b))

        # 公式验证与总结
        equation = Tex("9 + 16 = 25", font_size=48)
        equation.to_edge(DOWN)
        self.play(Write(equation))
        self.wait(2)
```

### Checkpoint 注释规则

> ⚠️ 每个缩进注释行 = 一个 checkpoint。注释数量直接决定 checkpoint 数量，过多会导致调试碎片化。

**必须遵守**：
1. **用中文**写注释（项目统一语言）
2. **不加序号前缀**（如 `# Checkpoint 1:` 是错误的）
3. **按视觉阶段分组**，不是按代码行分（一个 checkpoint 应对应一个完整的视觉变化）
4. **注释描述视觉目的**，不是代码实现（如"构建直角三角形"而不是"创建 Polygon 对象"）
5. **一般场景 3-5 个 checkpoint 足够**，复杂场景不超过 8 个

**❌ 反模式 1**：注释太碎、英文、带序号

```python
# Checkpoint 1: Title and introduction     ← 英文 + 序号
# Checkpoint 2: Create right triangle      ← 太碎
# Checkpoint 3: Label sides a, b, c        ← 应和三角形合并
```

**❌ 反模式 2**：把 checkpoint 代码提取到方法中（**会导致 checkpoint 系统完全失效**）

```python
# ❌ 严重错误！checkpoint_paste 只会把 self.show_title() 发到终端，
# 终端的 IPython 环境没有这个方法定义，直接报错！
class MyScene(Scene):
    def construct(self):
        # 显示标题
        self.show_title()        # ← checkpoint_paste 只发送这一行
        # 构建三角形
        self.build_triangle()    # ← 终端不知道这个方法，报错

    def show_title(self):        # ← 这个方法定义不会被发到终端
        title = Text("标题")
        self.play(Write(title))
```

> **原理**：`checkpoint_paste` 会把两个注释之间的代码复制到剪贴板，然后在终端的 IPython 中执行。它只发送 `construct` 方法内注释之间的代码行，不会发送其他方法的定义。所以所有动画代码**必须直接写在 `construct` 方法内**。

**❌ 反模式 3**：多余的 Config 类

```python
# ❌ 不需要，增加复杂度但没有实际收益
class Config:
    A = 3
    B = 4
    COLOR_A = RED
```

**✅ 正确写法**（所有代码内联在 `construct` 中）：

```python
# 标题和公式               ← 一个完整的视觉阶段
# 构建直角三角形并标注边长   ← 三角形 + 标注 = 一个阶段
# 在三边上构建正方形        ← 一个阶段
# 公式验证与总结            ← 一个阶段
```

### Scene 基类选择

| 基类 | 用途 |
|------|------|
| `Scene` | 基础 2D 场景 |
| `MovingCameraScene` | 需要移动/缩放相机 |
| `InteractiveScene` | 需要鼠标/键盘交互 |
| `ThreeDScene` | 3D 场景 |

所有包含 `Scene` 的基类都会被插件检测。

---

## 项目目录结构

```
D:\GitHub\manim_project\manimgl\
├── manim_imports_ext.py    # 统一导入文件
├── animations/             # 自定义动画类
├── mobject/                # 自定义 Mobject 类
├── utils/                  # 工具函数
├── custom_config.yml       # ManimGL 配置文件
├── scenes/                 # 正式场景（按主题子目录组织）
├── playground/             # 实验/测试场景
└── shader_surface/         # GLSL 着色器
```

`custom_config.yml` 的位置决定了 `projectRoot`，插件从文件目录向上搜索该文件。

---

## ManimGL vs ManimCE API 差异（易混淆项）

> ⚠️ 生成 ManimGL 代码时，**必须使用左列**，不要用右列的 ManimCE API

| ManimGL ✅ | ManimCE ❌ | 说明 |
|-----------|-----------|------|
| `from manimlib import *` | `from manim import *` | 导入包名不同 |
| `ShowCreation(obj)` | `Create(obj)` | 创建动画名不同 |
| `Uncreate(obj)` | `Uncreate(obj)` | 相同 |
| `Write(text)` | `Write(text)` | 相同 |
| `self.camera.frame` | `self.camera` | 相机访问方式不同 |
| `frame.set_euler_angles(theta, phi)` | `self.set_camera_orientation(theta, phi)` | 3D 相机旋转 |
| `frame.reorient(θ, φ, γ)` | 无 | ManimGL 独有 |
| `self.embed()` | 无 | ManimGL 交互式断点 |
| `self.wait()` | `self.wait()` | 相同 |
| `obj.animate.shift(RIGHT)` | `obj.animate.shift(RIGHT)` | 相同 |
| `always_redraw(lambda: ...)` | `always_redraw(lambda: ...)` | 相同 |
| `ValueTracker(0)` | `ValueTracker(0)` | 相同 |
| `Text("hi", font_size=48)` | `Text("hi", font_size=48)` | 相同 |
| `Tex(r"\int")` | `MathTex(r"\int")` | LaTeX 类名不同 |
| `TexText("text")` | `Tex("text")` | 文本 LaTeX 类名不同 |
| `SurfaceMesh` | 无 | ManimGL 独有 |
| `InteractiveScene` | 无 | ManimGL 独有交互场景 |
| `checkpoint_paste()` | 无 | ManimGL 插件独有 |
