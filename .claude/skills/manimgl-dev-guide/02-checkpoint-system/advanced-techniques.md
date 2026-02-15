# Checkpoint 高级技巧

> record/skip 参数、自定义导入、组合使用

## record 参数 - 录制动画

### 用途
在 checkpoint 执行时录制动画，可用于生成 GIF/视频

### 使用方法

**方式 1: 快捷键**
- 选中代码
- 按 `Ctrl+Shift+Alt+R` (Windows) 或 `Cmd+Shift+Alt+R` (Mac)

**方式 2: CodeLens 按钮**
- 点击 checkpoint 按钮时选择 "Record" 选项（如果支持）

### 示例

```python
class RecordingScene(Scene):
    def construct(self):
        # Checkpoint 1: 创建并录制文本
        text = Text("Hello ManimGL")
        self.play(Write(text))
        # 使用 Ctrl+Shift+Alt+R (record=True)

        # Checkpoint 2: 变换并录制
        self.play(text.animate.scale(2))
        # 使用 Ctrl+Shift+Alt+R
```

### 应用场景
- 创建演示 GIF
- 记录复杂动画序列
- 生成教学视频

---

## skip 参数 - 跳过预渲染

### 用途
跳过 checkpoint 的动画渲染，直接跳到最终状态

### 使用方法

**方式 1: 快捷键**
- 选中代码
- 按 `Ctrl+Shift+Alt+S` (Windows) 或 `Cmd+Shift+Alt+S` (Mac)

**方式 2: CodeLens 按钮**
- 点击 checkpoint 按钮时选择 "Skip" 选项（如果支持）

### 示例

```python
class SkipDemo(Scene):
    def construct(self):
        # Checkpoint 1: 创建复杂图形（不需要看到动画）
        complex_shape = self.create_complex_shape()
        # 使用 Ctrl+Shift+Alt+S (skip=True)

        # Checkpoint 2: 从这里开始正常播放
        self.play(Create(complex_shape))
```

### 应用场景
- 创建复杂对象时不需要看创建过程
- 快速跳到感兴趣的动画部分
- 调试后期动画效果

---

## 自定义导入

### manim_imports_ext.py 设计思想

**文件位置**: `D:\GitHub\manim_project\manimgl\manim_imports_ext.py`

```python
from manimlib import *
from animations import SpinShowCreation, ShowRotatingCreate, RotatingCreate, SpinInFromNothing
from typing import Callable, Iterable, Tuple, Union
from mobject import ComplexSurfaceWireframe, CalabiYauSurface, Hypercube
from utils import spiral_path, rotation_matrix_4d
```

**设计优势**：
1. **统一导入点**：所有场景文件只需 `from manim_imports_ext import *`
2. **命名空间隔离**：自定义组件与标准库清晰分离
3. **类型支持**：显式导入 typing 类型，增强 IDE 提示
4. **可维护性**：新增组件只需修改一个文件

### 使用方式

在所有场景脚本中统一使用：

```python
from manim_imports_ext import *

class MyScene(Scene):
    def construct(self):
        # 直接使用自定义组件，无需额外导入
        hypercube = Hypercube()
        self.play(SpinInFromNothing(hypercube))
```

---

## 组合使用技巧

### 技巧 1: skip + record 组合

```python
class CombinedScene(Scene):
    def construct(self):
        # Phase 1: 初始化（skip）
        # Checkpoint: 初始化所有对象
        objects = self.init_objects()
        # 使用 skip 参数快速跳过

        # Phase 2: 核心动画（record）
        # Checkpoint: 主要动画序列
        self.play_sequence(objects)
        # 使用 record 参数录制

        # Phase 3: 交互（正常）
        # Checkpoint: 启用交互
        self.enable_interaction(objects)
        # 正常执行，手动调试
```

### 技巧 2: 手动选区绕过限制

```python
class BypassScene(Scene):
    def construct(self):
        # Checkpoint 1
        circle = Circle()

        # Checkpoint 2
        square = Square()

        # Checkpoint 3
        triangle = Triangle()
```

**直接跳到 Checkpoint 3**：
1. 选中 `# Checkpoint 3` 及其代码
2. 按 `Alt+Shift+C`
3. 立即执行（无需先执行 1 和 2）

**注意**：手动选区执行不影响 checkpoint 进度状态。

### 技巧 3: 使用 -se 参数跳转

**命令行方式**：
```bash
manimgl script.py SceneName -se 15  # 从第 15 行开始运行
```

**插件自动处理**：
- 点击锁定的 checkpoint 按钮时
- 插件会使用 `-se` 参数从该行开始运行
- 然后解锁到该位置

---

## 高级场景模式

### 模式 1: 交互式开发循环

```python
class InteractiveDevScene(Scene):
    def construct(self):
        # Checkpoint 1: 基础设置
        self.setup_camera()
        self.add_axes()

        # === 开发循环 ===
        # Checkpoint 2: 添加对象（反复执行）
        obj = self.create_object()
        self.play(Create(obj))

        # 修改代码后重新执行 Checkpoint 2
        # 立即看到变化

        # Checkpoint 3: 调整动画（反复执行）
        self.play(Animate(obj))
```

### 模式 2: 分阶段渲染

```python
class PhasedScene(Scene):
    def construct(self):
        # Phase 1: 预渲染（skip）
        # Checkpoint: 预渲染所有对象
        all_objects = self.create_all_objects()
        # skip 模式快速跳过

        # Phase 2: 动画序列（record）
        # Checkpoint: 主要动画
        self.play_animation_sequence(all_objects)
        # record 模式录制

        # Phase 3: 最终调整（正常）
        # Checkpoint: 微调
        self.final_adjustments(all_objects)
```

### 模式 3: 调试特定部分

```python
class DebugScene(Scene):
    def construct(self):
        # Checkpoint 1: 设置场景
        self.setup_scene()

        # Checkpoint 2: 要调试的部分
        # 选中这部分代码，手动执行
        debug_obj = self.create_debug_object()
        self.debug_animation(debug_obj)

        # Checkpoint 3: 验证修复
        self.verify_fix(debug_obj)
```

---

## 性能优化

### 优化 1: 减少重复创建

```python
# ❌ 不好的做法 - 每次都创建新对象
# Checkpoint: 每次创建新圆
self.play(Create(Circle()))

# ✅ 好的做法 - 复用对象
# Checkpoint: 创建一次，多次使用
circle = Circle()
self.play(Create(circle))
self.play(circle.animate.shift(RIGHT))
self.play(circle.animate.set_color(RED))
```

### 优化 2: 预计算复杂值

```python
# ✅ 好的做法 - 预计算
# Checkpoint: 预计算复杂函数
points = [self.complex_calculation(i) for i in range(100)]

# Checkpoint: 使用预计算的值
for point in points:
    self.add(Dot(point))
```

### 优化 3: 使用配置对象

```python
# ✅ 好的做法 - 使用 CONFIG
class OptimizedScene(Scene):
    CONFIG = {
        "circle_config": {
            "radius": 1.0,
            "color": BLUE,
            "fill_opacity": 0.5
        }
    }

    def construct(self):
        # Checkpoint: 使用配置
        circle = Circle(**self.CONFIG["circle_config"])
        self.play(Create(circle))
```

---

## 故障排查

### 问题 1: Checkpoint 不执行

**症状**: 点击 checkpoint 按钮没有反应

**可能原因**:
1. 场景未启动（先运行 `▶ Run Scene`）
2. checkpoint 被锁定（先执行前一个）
3. 代码有语法错误

**解决方案**:
```python
# 1. 确保场景已启动
# 点击 ▶ Run Scene

# 2. 检查代码语法
# python -m py_compile your_scene.py

# 3. 查看终端错误信息
# 在预览窗口中查看错误堆栈
```

### 问题 2: 状态不正确

**症状**: checkpoint 显示的状态与实际不符

**解决方案**:
```python
# 重置状态
# 关闭终端（Ctrl+Shift+Q）
# 重新运行 Scene
```

### 问题 3: 代码块范围错误

**症状**: checkpoint 包含了不应该包含的代码

**检查**:
```python
# 确保注释行在 construct 方法内
# 确保有缩进（在 construct 方法内）
# 确保下一个注释行正确标记了边界
```

---

## 下一步

- 🎬 [Scene 模板库](../03-scene-templates/index.md) - 应用这些技巧
- 💡 [代码示例](../05-code-examples/index.md) - 实际应用案例
- 🔧 [插件功能说明](../06-extension-features/codelens-commands.md) - 更多高级功能
