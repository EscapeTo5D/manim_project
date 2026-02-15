# Checkpoint 最佳实践

> 命名规范、组织技巧、反例分析

## 命名规范

### 推荐的注释格式

```python
# ✅ 好的命名 - 清晰描述动作
# Checkpoint: 创建蓝色圆形
circle = Circle(color=BLUE)
self.play(Create(circle))

# ✅ 好的命名 - 包含对象状态
# Checkpoint: 圆形移动到右侧
self.play(circle.animate.shift(RIGHT))

# ✅ 好的命名 - 说明目的
# Checkpoint: 添加标题和副标题
title = Text("Main Title")
subtitle = Text("Subtitle")
self.play(Write(title), FadeIn(subtitle))
```

### 反例：不好的命名

```python
# ❌ 不好的命名 - 过于简略
# 测试
self.play(Create(circle))

# ❌ 不好的命名 - 无意义
# TODO
self.play(circle.animate.shift(LEFT))

# ❌ 不好的命名 - 模糊
# 动画
self.play(Create(square))
```

---

## 组织技巧

### 1. 按功能分组

```python
class OrganizedScene(Scene):
    def construct(self):
        # === 第一部分: 创建对象 ===
        # Checkpoint: 创建所有基本形状
        circle = Circle()
        square = Square()
        triangle = Triangle()
        self.play(Create(circle), Create(square), Create(triangle))

        # === 第二部分: 动画序列 ===
        # Checkpoint: 移动动画
        self.play(circle.animate.shift(LEFT))

        # Checkpoint: 颜色变换
        self.play(circle.animate.set_color(RED))

        # === 第三部分: 清理 ===
        # Checkpoint: 淡出所有对象
        self.play(FadeOut(circle), FadeOut(square), FadeOut(triangle))
```

### 2. 使用缩进表示层级

```python
def create_animated_shape(self):
    # Step 1: 创建
    # Checkpoint: 创建圆形
    circle = Circle()
    self.play(Create(circle))

    # Step 2: 动画
    # Checkpoint: 旋转动画
    self.play(Rotate(circle, angle=PI))

    # Step 3: 清理
    # Checkpoint: 移除圆形
    self.play(FadeOut(circle))
```

### 3. 保持 checkpoint 简短

```python
# ✅ 好的做法 - 每个 checkpoint 职责单一
# Checkpoint: 创建圆形
circle = Circle()

# Checkpoint: 显示圆形
self.play(Create(circle))

# Checkpoint: 移动圆形
self.play(circle.animate.shift(RIGHT))

# ❌ 不好的做法 - 一个 checkpoint 做太多事
# Checkpoint: 创建、显示并移动圆形
circle = Circle()
self.play(Create(circle))
self.play(circle.animate.shift(RIGHT))
self.play(circle.animate.set_color(RED))
```

---

## 反例分析

### 反例 1: Checkpoint 间隔过大

```python
# ❌ 不好的做法 - 代码块太长
# Checkpoint 1: 复杂场景
circle = Circle()
square = Square()
triangle = Triangle()
# ... 50 行代码 ...
self.play(Create(circle), Create(square), Create(triangle))
```

**问题**:
- 一次执行太多代码，难以调试
- 失去了 checkpoint 的灵活性

**改进方案**:
```python
# ✅ 改进 - 分解为小步骤
# Checkpoint 1: 创建圆形
circle = Circle()
self.play(Create(circle))

# Checkpoint 2: 创建方形
square = Square()
self.play(Create(square))

# Checkpoint 3: 创建三角形
triangle = Triangle()
self.play(Create(triangle))
```

### 反例 2: 忘记注释

```python
# ❌ 不好的做法 - 没有 Checkpoint 注释
circle = Circle()
self.play(Create(circle))
self.play(circle.animate.shift(RIGHT))
self.play(circle.animate.set_color(RED))
```

**问题**:
- 无法使用 checkpoint 功能
- CodeLens 不会显示按钮

**改进方案**:
```python
# ✅ 改进 - 添加 Checkpoint 注释
# Checkpoint: 创建并显示圆形
circle = Circle()
self.play(Create(circle))

# Checkpoint: 移动圆形
self.play(circle.animate.shift(RIGHT))

# Checkpoint: 变换颜色
self.play(circle.animate.set_color(RED))
```

### 反例 3: Checkpoint 位置不当

```python
# ❌ 不好的做法 - Checkpoint 在定义之前
# Checkpoint: 移动圆形
self.play(circle.animate.shift(RIGHT))

circle = Circle()  # 定义在后面
```

**问题**:
- 代码执行顺序混乱
- 容易出现 NameError

**改进方案**:
```python
# ✅ 改进 - Checkpoint 在操作之前
# Checkpoint: 创建圆形
circle = Circle()

# Checkpoint: 移动圆形
self.play(circle.animate.shift(RIGHT))
```

### 反例 4: 顶级注释

```python
# ❌ 不好的做法 - 顶级注释不会被视为 checkpoint
class MyScene(Scene):
    def construct(self):
        circle = Circle()

        # 这个注释是缩进的，会被识别为 checkpoint
        square = Square()

# 这个顶级注释不会被识别
```

**说明**: 插件只检测 `construct` 方法内的缩进注释。

---

## 代码组织原则

### 1. 单一职责

每个 checkpoint 应该只做一件明确的事情：

```python
# ✅ 好的做法
# Checkpoint: 创建标题
title = Text("Title")
self.play(Write(title))

# Checkpoint: 添加作者信息
author = Text("Author: Name")
author.next_to(title, DOWN)
self.play(FadeIn(author))
```

### 2. 逻辑连贯

checkpoint 之间应该有逻辑上的依赖关系：

```python
# ✅ 好的做法 - 前后依赖
# Checkpoint: 初始化场景
camera = Camera()
self.add(camera)

# Checkpoint: 添加对象（依赖相机）
circle = Circle()
self.play(Create(circle))
```

### 3. 可重复执行

每个 checkpoint 应该能够独立执行：

```python
# ❌ 不好的做法 - 依赖前面的状态
# Checkpoint 2: 使用 circle（但 circle 在 Checkpoint 1 创建）
self.play(circle.animate.shift(RIGHT))

# ✅ 好的做法 - 明确依赖
# Checkpoint 1: 创建 circle
circle = Circle()
self.play(Create(circle))

# Checkpoint 2: 移动 circle（明确依赖前面的结果）
self.play(circle.animate.shift(RIGHT))
```

---

## 注释技巧

### 使用 Section 注释

对于较长的场景，可以使用 Section 注释分组：

```python
class SectionedScene(Scene):
    def construct(self):
        # === Section 1: 初始化 ===
        # Checkpoint: 设置背景
        background = Rectangle(fill_opacity=0.3)
        self.add(background)

        # === Section 2: 主要内容 ===
        # Checkpoint: 添加标题
        title = Text("Main Content")
        self.play(Write(title))

        # === Section 3: 结束 ===
        # Checkpoint: 清理
        self.play(FadeOut(background))
```

### 使用 emoji 增强可读性

```python
# ✅ 使用 emoji 使注释更生动
# Checkpoint 🎨: 创建彩色圆形
circle = Circle(color=BLUE)
self.play(Create(circle))

# Checkpoint 🔄: 旋转动画
self.play(Rotate(circle, angle=PI))

# Checkpoint ✨: 添加特效
self.play(circle.animate.set_fill(YELLOW))
```

---

## 调试技巧

### 1. 逐步验证

```python
# Checkpoint 1: 验证对象创建
circle = Circle()
self.add(circle)  # 先添加，不播放动画

# Checkpoint 2: 验证动画
self.play(Create(circle))

# Checkpoint 3: 验证移动
self.play(circle.animate.shift(RIGHT))
```

### 2. 使用 print 调试

```python
# Checkpoint: 调试圆形属性
circle = Circle(radius=1.0)
print(f"Circle radius: {circle.radius}")  # 在终端输出
self.add(circle)
```

### 3. 临时禁用 checkpoint

```python
# Checkpoint 1: 创建对象
circle = Circle()

# ## Checkpoint 2: 暂时跳过
# self.play(Create(circle))

# Checkpoint 3: 继续
self.play(circle.animate.shift(RIGHT))
```

---

## 性能优化

### 1. 预渲染静态对象

```python
# ✅ 好的做法 - 预渲染
# Checkpoint: 创建所有静态对象
background = Rectangle(fill_opacity=0.3)
title = Text("Title")
self.add(background, title)

# Checkpoint: 只播放动态部分
self.play(Write(title))
```

### 2. 使用 updater 代替循环

```python
# ❌ 不好的做法 - 使用循环
# Checkpoint: 循环动画
for i in range(10):
    self.play(circle.animate.shift(0.1 * RIGHT))

# ✅ 好的做法 - 使用 updater
# Checkpoint: 持续动画
circle.add_updater(lambda m, dt: m.shift(0.5 * dt * RIGHT))
self.wait(2)
circle.clear_updaters()
```

---

## 下一步

- ⚡ [高级技巧](./advanced-techniques.md) - record/skip 参数、自定义导入
- 🎬 [Scene 模板](../03-scene-templates/index.md) - 可复用的模板
- 💡 [代码示例](../05-code-examples/index.md) - 实际应用案例
