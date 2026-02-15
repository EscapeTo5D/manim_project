# 交互式场景模板

> 鼠标交互、键盘事件、实时控制

## InteractiveScene 基础

### 适用场景
- 需要鼠标交互
- 探索性可视化
- 演示和教学

### 完整代码

```python
from manim_imports_ext import *

class InteractiveDemo(InteractiveScene):
    def construct(self):
        # Checkpoint 1: 添加固定标题
        title = Text(
            "Interactive Demo",
            font_size=48
        )
        title.to_edge(UP)
        title.fix_in_frame()  # 固定在屏幕上
        self.add(title)

        # Checkpoint 2: 添加可交互圆形
        circle = Circle(
            radius=1.5,
            color=BLUE,
            fill_opacity=0.5,
            stroke_width=5
        )
        self.add(circle)

        # Checkpoint 3: 添加多个对象
        square = Square(
            side_length=2.0,
            color=RED,
            fill_opacity=0.5
        )
        square.next_to(circle, RIGHT)
        self.add(square)

        # Checkpoint 4: 进入交互模式
        self.wait()  # 在预览窗口中可以拖拽对象
```

### 关键特性

**固定对象**:
```python
obj.fix_in_frame()  # 固定在屏幕上，不受相机影响
```

**交互提示**:
```python
obj.add_tooltip("Drag me!")  # 悬停提示
```

---

## 鼠标交互

### 基础鼠标交互

```python
from manim_imports_ext import *

class MouseInteractionScene(InteractiveScene):
    def construct(self):
        # Checkpoint 1: 创建可点击对象
        square = Square(
            side_length=2.0,
            color=BLUE,
            fill_opacity=0.5
        )
        square.add_updater(lambda m: m.set_color(
            RED if self.mouse_point.get_value()[0] > 0 else BLUE
        ))
        self.add(square)

        # Checkpoint 2: 进入交互
        self.wait()
```

### 拖拽对象

```python
class DraggableObjectScene(InteractiveScene):
    def construct(self):
        # Checkpoint 1: 创建可拖拽对象
        circle = Circle(
            radius=1.0,
            color=YELLOW,
            fill_opacity=0.8
        )
        self.add(circle)

        # Checkpoint 2: 添加拖拽逻辑
        def update_circle(m):
            if self.mouse_point.is_pressed():
                m.move_to(self.mouse_point.get_point())

        circle.add_updater(update_circle)

        # Checkpoint 3: 进入交互
        self.wait(10)  # 可以拖拽圆形
        circle.clear_updaters()
```

---

## 键盘交互

### 基础键盘事件

```python
class KeyboardInteractionScene(InteractiveScene):
    def construct(self):
        # Checkpoint 1: 创建对象
        circle = Circle(radius=1.0, color=BLUE)
        self.add(circle)

        # Checkpoint 2: 添加键盘响应
        def on_key(event):
            if event.key == "r":
                circle.set_color(RED)
            elif event.key == "g":
                circle.set_color(GREEN)
            elif event.key == "b":
                circle.set_color(BLUE)

        self.on_key_press = on_key

        # Checkpoint 3: 进入交互
        self.wait()
```

### 参数控制

```python
class ParameterControlScene(InteractiveScene):
    def construct(self):
        # Checkpoint 1: 创建可控制对象
        tracker = ValueTracker(1.0)
        circle = Circle(radius=1.0)

        def update_circle(m):
            m.become(Circle(radius=tracker.get_value()))

        circle.add_updater(update_circle)
        self.add(circle, tracker)

        # Checkpoint 2: 添加键盘控制
        def on_key(event):
            if event.key == "up":
                tracker.increment_value(0.1)
            elif event.key == "down":
                tracker.increment_value(-0.1)

        self.on_key_press = on_key

        # Checkpoint 3: 进入交互
        self.wait()
```

---

## 实时更新

### 使用 Updater

```python
class RealtimeUpdateScene(InteractiveScene):
    def construct(self):
        # Checkpoint 1: 创建旋转对象
        square = Square(side_length=2.0, color=BLUE)
        self.add(square)

        # Checkpoint 2: 添加旋转动画
        square.add_updater(lambda m, dt: m.rotate(2 * dt))

        # Checkpoint 3: 进入交互
        self.wait(5)  # 持续旋转5秒
        square.clear_updaters()
```

### ValueTracker 应用

```python
class ValueTrackerScene(InteractiveScene):
    def construct(self):
        # Checkpoint 1: 创建参数化对象
        freq_tracker = ValueTracker(1.0)
        circle = Circle()

        def update_circle(m):
            freq = freq_tracker.get_value()
            # 根据频率调整对象
            m.become(Circle(radius=1.0 / freq))

        circle.add_updater(update_circle)
        self.add(circle, freq_tracker)

        # Checkpoint 2: 添加控制
        def on_key(event):
            if event.key == "up":
                freq_tracker.increment_value(0.5)
            elif event.key == "down":
                freq_tracker.increment_value(-0.5)

        self.on_key_press = on_key

        # Checkpoint 3: 进入交互
        self.wait()
```

---

## 使用技巧

### 1. 固定 UI 元素

```python
# UI 元素应该固定在屏幕上
title.fix_in_frame()
subtitle.fix_in_frame()
```

### 2. 分离交互对象

```python
# 交互对象不应该固定
interactive_obj = Circle()
# 不调用 fix_in_frame()
```

### 3. 清理 Updater

```python
# 交互结束后清理
obj.clear_updaters()
```

---

## 下一步

- 💡 [代码示例](../05-code-examples/index.md) - 更多交互式示例
- 🔧 [插件功能说明](../06-extension-features/codelens-commands.md) - 快捷键和命令
- ✨ [最佳实践](../02-checkpoint-system/best-practices.md) - 代码组织技巧
