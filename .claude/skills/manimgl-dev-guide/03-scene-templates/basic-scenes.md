# 基础 Scene 模板

> 2D 场景、简单动画、文本特效

## 模板 1: 几何图形动画

### 适用场景
- 学习基本图形
- 测试动画效果
- 简单演示

### 完整代码

```python
from manim_imports_ext import *

class GeometryScene(Scene):
    def construct(self):
        # Checkpoint 1: 创建基本图形
        circle = Circle(radius=1.0, color=BLUE)
        square = Square(side_length=2.0, color=RED)
        triangle = RegularPolygon(n=3, color=YELLOW)

        # Checkpoint 2: 显示图形
        self.play(
            Create(circle),
            Create(square),
            Create(triangle),
            run_time=2
        )
        self.wait()

        # Checkpoint 3: 排列图形
        circle.move_to(LEFT * 3)
        square.center()
        triangle.move_to(RIGHT * 3)

        self.play(
            circle.animate.move_to(LEFT * 3),
            square.animate.center(),
            triangle.animate.move_to(RIGHT * 3),
            run_time=2
        )
        self.wait()

        # Checkpoint 4: 添加标签
        circle_label = Text("Circle").next_to(circle, DOWN)
        square_label = Text("Square").next_to(square, DOWN)
        triangle_label = Text("Triangle").next_to(triangle, DOWN)

        self.play(
            Write(circle_label),
            Write(square_label),
            Write(triangle_label),
            run_time=2
        )
```

### 关键元素

**常用 2D Mobject**:
```python
Circle(radius=1.0)              # 圆形
Square(side_length=2.0)         # 正方形
Rectangle(width=3, height=2)    # 矩形
Triangle()                       # 三角形
RegularPolygon(n=5)             # 正五边形
```

**常用动画**:
```python
Create(mobject)                 # 描边显示
FadeIn(mobject)                 # 淡入
ShowCreation(mobject)           # 边创建边显示
```

---

## 模板 2: 文本动画

### 适用场景
- 标题动画
- 列表展示
- 公式推导

### 完整代码

```python
from manim_imports_ext import *

class TextAnimationScene(Scene):
    def construct(self):
        # Checkpoint 1: 创建标题
        title = Text("Text Animation", font_size=64)
        title.to_edge(UP)
        self.play(Write(title), run_time=2)
        self.wait()

        # Checkpoint 2: 添加副标题
        subtitle = Text("Interactive Development", font_size=36)
        subtitle.next_to(title, DOWN, buff=0.5)
        self.play(FadeIn(subtitle, shift=UP), run_time=1)
        self.wait()

        # Checkpoint 3: 高亮关键词
        highlighted_title = title.copy()
        highlighted_title.set_color(YELLOW)
        self.play(Transform(title, highlighted_title), run_time=1)
        self.wait()
```

### 关键元素

**文本创建**:
```python
Text("Hello", font_size=48)              # 英文
Text("你好", font="SimHei", font_size=48)  # 中文
Tex(r"E = mc^2")                        # LaTeX 公式
```

**文本动画**:
```python
Write(text)                    # 逐字显示
FadeIn(text)                   # 淡入
AddTextLetterByLetter(text)    # 字母动画
```

---

## 模板 3: 变换动画

### 适用场景
- 形状变换
- 颜色变化
- 位置移动

### 完整代码

```python
from manim_imports_ext import *

class TransformScene(Scene):
    def construct(self):
        # Checkpoint 1: 创建初始对象
        circle = Circle(radius=1.5, color=BLUE)
        self.add(circle)
        self.wait()

        # Checkpoint 2: 变换为方形
        square = Square(side_length=2.5, color=RED)
        self.play(Transform(circle, square), run_time=2)
        self.wait()

        # Checkpoint 3: 变换为三角形
        triangle = Triangle(color=GREEN)
        self.play(Transform(circle, triangle), run_time=2)
        self.wait()

        # Checkpoint 4: 位置和颜色动画
        self.play(
            circle.animate.shift(UP * 2),
            circle.animate.set_fill(YELLOW, opacity=0.8),
            run_time=2
        )
        self.wait()
```

### 变换类型对比

| 变换类型 | 效果 | 适用场景 |
|---------|------|----------|
| `Transform` | 形状变换 | 保留部分特征的变形 |
| `ReplacementTransform` | 替换 | 完全替换对象 |
| `FadeTransform` | 淡入淡出 | 无关联的切换 |

---

## 模板 4: 组合动画

### 适用场景
- 多个对象同时动画
- 交错动画
- 序列动画

### 完整代码

```python
from manim_imports_ext import *

class CompositionScene(Scene):
    def construct(self):
        # Checkpoint 1: 创建组
        shapes = VGroup(
            Circle(color=RED),
            Square(color=GREEN),
            Triangle(color=BLUE)
        )
        shapes.arrange(RIGHT, buff=1.0)

        # Checkpoint 2: 同时创建
        self.play(LaggedStart(
            Create(shapes[0]),
            Create(shapes[1]),
            Create(shapes[2]),
            lag_ratio=0.2
        ), run_time=2)
        self.wait()

        # Checkpoint 3: 整体动画
        self.play(
            shapes.animate.scale(1.5),
            run_time=2
        )
        self.wait()

        # Checkpoint 4: 分别动画
        self.play(
            shapes[0].animate.shift(UP),
            shapes[1].animate.shift(DOWN),
            shapes[2].animate.rotate(PI),
            run_time=2
        )
        self.wait()
```

### 组合技巧

**VGroup 使用**:
```python
# 垂直排列
group = VGroup(obj1, obj2, obj3)
group.arrange(DOWN, buff=0.5)

# 水平排列
group = VGroup(obj1, obj2, obj3)
group.arrange(RIGHT, buff=1.0)
```

**动画组合**:
```python
# 同时播放
self.play(anim1, anim2)

# 交错播放
self.play(LaggedStart(anim1, anim2, lag_ratio=0.3))

# 序列播放
self.play(AnimationGroup(anim1, anim2))
```

---

## 模板 5: 函数可视化

### 适用场景
- 数学函数绘图
- 数据可视化
- 科学演示

### 完整代码

```python
from manim_imports_ext import *
import numpy as np

class FunctionGraphScene(Scene):
    def construct(self):
        # Checkpoint 1: 创建坐标轴
        axes = Axes(
            x_range=(-5, 5, 1),
            y_range=(-2, 2, 0.5),
            x_length=10,
            y_length=6,
            color=WHITE
        )
        self.add(axes)
        self.wait()

        # Checkpoint 2: 绘制正弦函数
        def sin_func(x):
            return np.sin(x)

        sin_graph = axes.plot(
            sin_func,
            color=BLUE,
            x_range=(-5, 5)
        )
        self.play(Create(sin_graph), run_time=3)
        self.wait()

        # Checkpoint 3: 绘制余弦函数
        def cos_func(x):
            return np.cos(x)

        cos_graph = axes.plot(
            cos_func,
            color=RED,
            x_range=(-5, 5)
        )
        self.play(Create(cos_graph), run_time=3)
        self.wait()

        # Checkpoint 4: 添加标签
        sin_label = axes.get_graph_label(
            sin_graph,
            "y = sin(x)",
            x_val=-4,
            direction=LEFT,
            color=BLUE
        )
        cos_label = axes.get_graph_label(
            cos_graph,
            "y = cos(x)",
            x_val=4,
            direction=RIGHT,
            color=RED
        )

        self.play(
            FadeIn(sin_label),
            FadeIn(cos_label),
            run_time=1
        )
```

### 关键元素

**坐标轴创建**:
```python
Axes(
    x_range=(min, max, step),
    y_range=(min, max, step),
    x_length=10,
    y_length=6,
)
```

**函数绘图**:
```python
axes.plot(
    func,                  # 函数 f(x)
    color=BLUE,
    x_range=(-5, 5),
)
```

---

## 使用建议

### 1. 从简单开始

- 先使用 **模板 1** 练习基本图形
- 然后尝试 **模板 2** 添加文本
- 最后使用 **模板 5** 可视化函数

### 2. 修改参数

- 修改颜色：`color=BLUE` → `color=RED`
- 修改大小：`radius=1.0` → `radius=2.0`
- 修改时长：`run_time=2` → `run_time=3`

### 3. 组合元素

- 从不同模板复制代码片段
- 组合成你自己的场景
- 添加 checkpoint 分隔

---

## 下一步

- 🎮 [交互式场景模板](./interactive-scenes.md) - 添加鼠标/键盘交互
- 💡 [代码示例](../05-code-examples/index.md) - 更多实际应用案例
- ✨ [最佳实践](../02-checkpoint-system/best-practices.md) - 编码规范
