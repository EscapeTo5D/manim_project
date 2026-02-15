# Scene 创建模板库

> 从基础到高级的 Scene 模板，快速开始你的动画项目

## 模板分类

### 按难度分类

- 🔰 **基础模板** - 2D 场景、简单动画
- 🎯 **进阶模板** - 3D 场景、相机控制
- 🚀 **高级模板** - 交互式场景、自定义 Mobject

### 按场景类型分类

- 教学演示类
- 数据可视化类
- 数学概念类
- 物理模拟类

---

## 快速开始

### 最小化模板

```python
from manim_imports_ext import *

class MinimalScene(Scene):
    def construct(self):
        # Checkpoint: 创建对象
        circle = Circle()

        # Checkpoint: 显示动画
        self.play(Create(circle))
```

### 标准模板

```python
from manim_imports_ext import *

class StandardScene(Scene):
    def construct(self):
        # Checkpoint: 初始化
        title = Text("Title")
        self.add(title)

        # Checkpoint: 主要内容
        circle = Circle()
        self.play(ShowCreation(circle))

        # Checkpoint: 结束
        self.wait()
```

---

## 可用模板

### 1. 基础动画场景
→ [查看详细模板](./basic-scenes.md)

**包含**:
- 几何图形创建
- 文本动画
- 变换动画
- 组合动画

**适用**:
- 快速验证想法
- 学习基础概念
- 简单演示

### 2. 交互式场景
→ [查看详细模板](./interactive-scenes.md)

**包含**:
- 鼠标交互
- 键盘交互
- 拖拽对象
- 参数调整

**适用**:
- 需要用户交互
- 探索性可视化
- 演示和教学

---

## Scene 基类对比

| 基类 | 特点 | 适用场景 | 模板 |
|------|------|----------|------|
| **Scene** | 基础场景类 | 简单动画、2D 图形 | [基础模板](./basic-scenes.md) |
| **MovingCameraScene** | 可移动相机 | 缩放、平移视图 | 进阶模板 |
| **InteractiveScene** | 支持交互 | 鼠标/键盘事件 | [交互式模板](./interactive-scenes.md) |
| **ThreeDScene** | 3D 场景 | 3D 对象、空间可视化 | 进阶模板 |

---

## 使用方法

### 方式 1: 复制粘贴

从模板文件复制代码到新文件。

### 方式 2: VS Code 代码片段（推荐）

在 VS Code 中配置用户代码片段：

**文件**: `~/.vscode/snippets/python.json`

```json
{
  "Manim Basic Scene": {
    "prefix": "manim-basic",
    "body": [
      "from manim_imports_ext import *",
      "",
      "class ${1:SceneName}(Scene):",
      "    def construct(self):",
      "        # Checkpoint: 初始化",
      "        pass",
      "",
      "        # Checkpoint: 主要内容",
      "        pass",
      "$0"
    ]
  },
  "Manim Interactive Scene": {
    "prefix": "manim-interactive",
    "body": [
      "from manim_imports_ext import *",
      "",
      "class ${1:SceneName}(InteractiveScene):",
      "    def construct(self):",
      "        # Checkpoint: 初始化",
      "        pass",
      "",
      "        # Checkpoint: 交互",
      "        self.wait()  # 进入交互模式",
      "$0"
    ]
  }
}
```

**使用**:
1. 输入 `manim-basic` 或 `manim-interactive`
2. 按 `Tab`
3. 填写场景名称

---

## 模板规范

### 命名规范

```python
class DescriptiveName(Scene):      # ✅ 清晰描述内容
class MyScene(Scene):              # ❌ 太泛
class Scene1(Scene):               # ❌ 无意义
```

### 文件组织

```
project/
├── scenes/
│   ├── basic/
│   │   ├── text_animation.py
│   │   └── shape_transform.py
│   ├── advanced/
│   │   ├── interactive.py
│   │   └── shader_effects.py
├── mobjects/
│   ├── custom_shapes.py
│   └── utils.py
└── output/
    ├── videos/
    └── images/
```

---

## 最佳实践

### 1. 使用 checkpoint 分隔

```python
class GoodScene(Scene):
    def construct(self):
        # Checkpoint: 初始化场景
        self.setup_scene()

        # Checkpoint: 添加主要元素
        self.add_main_elements()

        # Checkpoint: 添加动画
        self.animate_elements()
```

### 2. 保持简洁

```python
# ✅ 好的做法 - 每个 Scene 专注一个演示
class CircleTransform(Scene):
    """演示圆形变换"""
    pass

# ❌ 不好的做法 - 一个 Scene 做太多事
class EverythingScene(Scene):
    """演示所有功能"""
    pass
```

### 3. 复用自定义模块

```python
from manim_imports_ext import *
from mobject import CustomShape

class ReusableScene(Scene):
    def construct(self):
        # Checkpoint: 使用自定义 mobject
        obj = CustomShape()
        self.play(SpinInFromNothing(obj))
```

---

## 下一步

- 📝 [基础场景模板](./basic-scenes.md) - 详细的模板代码
- 🎮 [交互式场景模板](./interactive-scenes.md) - 交互功能实现
- 💡 [代码示例](../05-code-examples/index.md) - 完整应用案例
