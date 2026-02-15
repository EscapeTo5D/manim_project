---
name: manimgl-dev-guide
description: ManimGL 交互式开发指南。在 manimgl/ 目录工作或提到 "manimgl"、"scene"、"动画"、"checkpoint_paste" 时应用。包含 checkpoint 系统、Scene 创建模板、代码示例、最佳实践、插件功能说明。
---

# ManimGL Development Skill

> 基于 ManimGL Interactive VS Code 扩展的交互式开发指南

[![Version](https://img.shields.io/badge/version-0.1.0-blue.svg)](https://github.com/EscapeTo5D/maningl-preview)
[![ManimGL](https://img.shields.io/badge/ManimGL-compatible-green.svg)](https://github.com/3b1b/manim)

---

## 🎯 快速导航

### 场景感知入口

根据你的当前任务选择入口：

- 🔥 **刚开始学习？** → [5分钟快速开始](01-quick-start.md)
- 🎯 **想快速创建 Scene？** → [Scene 模板库](03-scene-templates/index.md)
- 🔧 **遇到 Checkpoint 问题？** → [Checkpoint 深度教程](02-checkpoint-system/index.md)
- 💡 **寻找代码示例？** → [精选代码示例库](05-code-examples/index.md)
- ⚡ **优化工作流程？** → [插件功能说明](06-extension-features/codelens-commands.md)

---

## 📚 核心概念速查

| 概念 | 说明 | 深入学习 |
|------|------|----------|
| **Scene** | ManimGL 的核心类，定义动画场景 | [Scene 创建模板](03-scene-templates/index.md) |
| **Checkpoint** | 交互式调试点，支持分段执行动画 | [Checkpoint 系统](02-checkpoint-system/index.md) |
| **Mobject** | 可动画的数学对象（图形、文字等） | [Mobject 复用模块](05-code-examples/mobject_reuse.py) |
| **CodeLens** | VS Code 中的可交互按钮 | [扩展功能说明](06-extension-features/codelens-commands.md) |

---

## ⚡ 一分钟速览

### 基础工作流程

```python
from manim_imports_ext import *

class MyScene(Scene):
    def construct(self):
        # Checkpoint 1: 创建对象
        circle = Circle()

        # Checkpoint 2: 显示动画
        self.play(Create(circle))
        # 👆 点击注释行上方的 ▶ CheckpointPaste 按钮执行
```

### 核心快捷键

| 操作 | Windows/Linux | macOS |
|------|--------------|-------|
| 运行 Scene | `Ctrl+Shift+R` | `Cmd+Shift+R` |
| Checkpoint Paste | `Alt+Shift+C` | `Cmd+Shift+C` |
| 复制相机状态 | `Ctrl+Alt+C` | `Cmd+Alt+C` |
| 退出 Scene | `Ctrl+Shift+Q` | `Cmd+Shift+Q` |

---

## 🔌 扩展功能概览

### VS Code 扩展提供的功能

1. **Scene 检测** - 自动识别 Scene 类，在 `construct` 方法显示 `▶ Run Scene` 按钮
2. **Checkpoint 系统** - 在注释行显示 Checkpoint 按钮，支持状态锁定/解锁/执行
3. **终端集成** - 自动管理 ManimGL 终端，支持环境变量配置
4. **相机状态复制** - 一键复制 `frame.reorient(...)` 代码

详细说明：[扩展功能指南](06-extension-features/)

---

## 🎓 进阶学习路径

### 路径 1：交互式动画开发
1. [Checkpoint 深度教程](02-checkpoint-system/index.md) - 掌握状态机规则
2. [交互式 Scene 模板](03-scene-templates/interactive-scenes.md) - 鼠标/键盘事件
3. [插件功能说明](06-extension-features/) - 提升开发效率

### 路径 2：复杂场景构建
1. [Scene 创建模板库](03-scene-templates/index.md) - 选择合适的基础模板
2. [Mobject 复用模块](05-code-examples/mobject_reuse.py) - 避免重复代码
3. [最佳实践指南](02-checkpoint-system/best-practices.md) - 代码规范

---

## 🔍 常见问题快速链接

### Checkpoint 相关
- **Checkpoint 不执行？** → [Checkpoint 状态机规则](02-checkpoint-system/index.md#状态流转)
- **如何使用 record/skip？** → [高级技巧](02-checkpoint-system/advanced-techniques.md)
- **Checkpoint 命名规范？** → [最佳实践](02-checkpoint-system/best-practices.md)

### Scene 相关
- **如何选择 Scene 基类？** → [Scene 模板选择指南](03-scene-templates/index.md)
- **如何添加鼠标交互？** → [交互式 Scene 模板](03-scene-templates/interactive-scenes.md)

---

## 💾 自定义模块说明

### manim_imports_ext.py

项目使用的自定义导入文件，集中管理所有依赖：

```python
from manimlib import *
from animations import SpinShowCreation, ShowRotatingCreate, RotatingCreate, SpinInFromNothing
from typing import Callable, Iterable, Tuple, Union
from mobject import ComplexSurfaceWireframe, CalabiYauSurface, Hypercube
from utils import spiral_path, rotation_matrix_4d
```

**设计思想**：
- ✅ 统一导入点，所有场景文件只需 `from manim_imports_ext import *`
- ✅ 命名空间隔离，自定义组件与标准库清晰分离
- ✅ 可维护性强，新增组件只需修改一个文件

详细说明：[自定义导入配置](06-extension-features/custom-imports.md)

---

## 📦 Mobject 复用模块

项目包含以下可复用的高级组件：

- **Hypercube** - 4D 超立方体的 3D 投影可视化
- **CalabiYauSurface** - 卡拉比-丘流形（复数曲面）
- **ComplexSurfaceWireframe** - 自定义曲面的线框渲染

使用示例：[Mobject 复用模块示例](05-code-examples/mobject_reuse.py)

---

## 📖 参考资源

- [ManimGL 官方文档](https://github.com/3b1b/manim)
- [3Blue1Brown 的视频教程](https://www.youtube.com/c/3blue1brown)
- [VS Code 扩展仓库](https://github.com/EscapeTo5D/maningl-preview)

---

## 🛠️ 技术支持

- **问题反馈** → [GitHub Issues](https://github.com/EscapeTo5D/maningl-preview/issues)
- **功能建议** → [GitHub Discussions](https://github.com/EscapeTo5D/maningl-preview/discussions)

---

**版本**: 0.1.0
**最后更新**: 2026-02-15
**维护者**: EscapeTo5D
