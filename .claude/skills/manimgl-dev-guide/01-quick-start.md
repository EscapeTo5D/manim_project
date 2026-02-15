# 5分钟快速入门 ManimGL

> 目标：5分钟内运行第一个 ManimGL 场景

## 前置条件检查

### 1. 确认环境

打开 VS Code，确保：
- ✅ 已安装 Python 3.10+
- ✅ 已安装 ManimGL (`pip install manimgl`)
- ✅ 已安装 "ManimGL Interactive" 扩展

验证安装：
```bash
# 在终端运行
manimgl --version
```

### 2. 打开 ManimGL 项目

```bash
# 打开你的 manimgl 项目目录
code D:\GitHub\manim_project\manimgl
```

---

## 第一个 Scene (3分钟)

### 步骤 1: 创建 Python 文件

创建 `hello_scene.py`:

```python
from manim_imports_ext import *

class HelloScene(Scene):
    def construct(self):
        # 创建文本对象
        text = Text("Hello ManimGL!", font_size=72)

        # 添加到场景
        self.add(text)

        # 等待
        self.wait()
```

### 步骤 2: 运行 Scene

**方式 1: 使用 CodeLens**
1. 打开 `hello_scene.py`
2. 找到 `def construct(self):` 行
3. 点击 `▶ Run Scene` 按钮

**方式 2: 使用快捷键**
1. 光标放在 Scene 类内
2. 按 `Ctrl+Shift+R` (Windows) 或 `Cmd+Shift+R` (Mac)

### 步骤 3: 交互式预览

终端会启动预览窗口：
- 拖拽鼠标旋转视角
- 滚轮缩放
- 按 `q` 退出

---

## Checkpoint 初体验 (2分钟)

### 什么是 Checkpoint?

Checkpoint 是 ManimGL 的**增量开发神器**：
- 🎯 在注释行标记代码块
- ⚡ 即时粘贴执行
- 🔄 快速迭代修改
- 🔒 顺序解锁确保状态一致

### 基础用法

创建 `checkpoint_demo.py`:

```python
from manim_imports_ext import *

class CheckpointDemo(Scene):
    def construct(self):
        # Checkpoint 1: 添加标题
        title = Text("Checkpoint Demo")
        self.add(title)
        self.wait()

        # Checkpoint 2: 创建圆形
        circle = Circle(radius=1.0, color=BLUE)
        self.play(ShowCreation(circle))
        self.wait()

        # Checkpoint 3: 添加方形
        square = Square(side_length=1.5, color=RED)
        self.play(ShowCreation(square))
        self.wait()
```

### 使用 Checkpoint

1. **运行 Scene**: 点击 `▶ Run Scene`
2. **执行 Checkpoint 2**:
   - 找到 `# Checkpoint 2:` 注释行
   - 点击 `▶ CheckpointPaste` 按钮
3. **修改并重新执行**:
   - 修改圆形颜色为 `YELLOW`
   - 再次点击 `▶ CheckpointPaste`
   - 立即看到变化！

### Checkpoint 状态流转

```
🔒 锁定 → ▶ 已解锁 → ✅ 已执行
  ↓         ↓           ↓
首次运行   点击解锁   点击执行
```

---

## 下一步

- 📖 [插件功能详解](06-extension-features/codelens-commands.md)
- 🎬 [创建第一个动画](03-scene-templates/basic-scenes.md)
- 🔧 [Checkpoint 深度教程](02-checkpoint-system/index.md)

---

## 常见问题

**Q: 运行时提示找不到 manimgl?**
A: 检查 Python 环境，确保在虚拟环境中安装了 manimgl

**Q: CodeLens 不显示?**
A: 确认文件是 `.py` 后缀，且包含 `class XXX(Scene):`

**Q: Checkpoint 按钮是锁定的?**
A: 先运行 `▶ Run Scene`，checkpoint 才会解锁

**Q: 如何使用自定义的 mobject?**
A: 参考 [Mobject 复用模块](05-code-examples/mobject_reuse.py)
