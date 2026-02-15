# 精选代码示例库

> 5 个实用示例，展示常见动画模式和最佳实践

## 示例列表

### 基础示例

1. **基础动画集合** - `basic_animations.py`
   - 创建、变换、移动、旋转、缩放
   - 适合：学习基础操作

2. **文本动画特效** - `text_animations.py`
   - 文本创建、变换、公式动画
   - 适合：教学演示

3. **组合动画** - `composition.py`
   - 多对象协调动画
   - 适合：复杂场景

### 实用模块

4. **Mobject 复用模块** - `mobject_reuse.py`
   - 可复用的样式化图形
   - 适合：项目开发

### 高级示例

5. **交互式控制** - `interactive_control.py`
   - 鼠标/键盘交互
   - 适合：探索性可视化

---

## 使用方法

### 复制到你的项目

```bash
# 复制示例文件到你的项目
cp .claude/skills/manimgl-dev-guide/05-code-examples/mobject_reuse.py \
   D:/GitHub/manim_project/manimgl/mobjects/
```

### 导入使用

```python
# 在你的 Scene 中导入
from mobject.mobject_reuse import StyledCircle, ColorPalette

class MyScene(Scene):
    def construct(self):
        # 使用复用模块
        circle = StyledCircle(color=ColorPalette.PRIMARY)
        self.play(Create(circle))
```

---

## 示例 1: 基础动画集合

**文件**: `basic_animations.py`

```python
from manim_imports_ext import *

class BasicAnimations(Scene):
    def construct(self):
        # Checkpoint 1: 创建动画
        circle = Circle(radius=1.5, color=BLUE)
        self.play(Create(circle), run_time=2)
        self.wait()

        # Checkpoint 2: 移动动画
        self.play(circle.animate.shift(RIGHT * 3), run_time=2)
        self.wait()

        # Checkpoint 3: 旋转动画
        self.play(Rotate(circle, angle=PI), run_time=2)
        self.wait()

        # Checkpoint 4: 缩放动画
        self.play(circle.animate.scale(2), run_time=2)
        self.wait()

        # Checkpoint 5: 颜色动画
        self.play(circle.animate.set_color(RED), run_time=2)
        self.wait()
```

---

## 示例 2: Mobject 复用模块

**文件**: `mobject_reuse.py`

```python
"""
Mobject 复用模块
提供可复用的样式化图形和配置
"""

from manimlib import *
from typing import Optional

class ColorPalette:
    """颜色配置"""
    PRIMARY = BLUE
    SECONDARY = RED
    ACCENT = YELLOW
    SUCCESS = GREEN

class StyledCircle(Circle):
    """样式化圆形"""
    def __init__(
        self,
        radius: float = 1.0,
        color: str = ColorPalette.PRIMARY,
        stroke_width: float = 4.0,
        fill_opacity: float = 0.5,
        **kwargs
    ):
        super().__init__(
            radius=radius,
            color=color,
            stroke_width=stroke_width,
            fill_opacity=fill_opacity,
            **kwargs
        )

# 使用示例
class MobjectReuseExample(Scene):
    def construct(self):
        # Checkpoint: 使用样式化圆形
        circle = StyledCircle(color=ColorPalette.PRIMARY)
        self.play(Create(circle))
```

---

## 扩展指南

### 添加你自己的示例

1. 在 `05-code-examples/` 创建新文件
2. 遵循命名规范（snake_case）
3. 添加详细注释和 Checkpoint
4. 更新本索引文件

### 贡献示例

欢迎提交你的示例到主仓库！

---

## 下一步

- 🎬 [Scene 模板](../03-scene-templates/index.md) - 更多模板
- ✨ [最佳实践](../02-checkpoint-system/best-practices.md) - 编码规范
- 🔧 [插件功能说明](../06-extension-features/codelens-commands.md) - 快捷键
