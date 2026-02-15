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

class DescriptiveName(Scene):
    def construct(self):
        # 描述该步骤目的的注释（会被插件检测为 checkpoint）
        obj = Circle(color=BLUE)
        self.play(Create(obj))

        # 下一个 checkpoint
        self.play(obj.animate.shift(RIGHT))
```

### 与 Checkpoint 系统配合的要点

1. **注释行必须缩进**：顶级注释不会被检测
2. **每个注释行 = 一个 checkpoint**：注释之间的代码构成一个可独立执行的代码块
3. **保持代码块短小**：每个 checkpoint 对应一个逻辑步骤
4. **注释要有描述性**：避免 `# TODO`、`# test` 等无意义注释
5. **注意执行顺序**：checkpoint 2 的代码可能引用 checkpoint 1 中创建的变量，这在增量执行时是正常的

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
