# Manim 数学动画项目

基于 Manim 的数学动画制作项目，包含各种数学概念的动画示例和自定义组件。

| 版本 | 用途 | 特点 |
|------|------|------|
| **ManimGL** (`manimgl/`) | 交互式开发 | Checkpoint 增量迭代、实时预览、VS Code 插件支持 |
| **ManimCE** (`manimce/`) | 高质量渲染 | 批量渲染、`-pql`/`-pqh` 质量选项 |

## 项目结构

```
manim_project/
├── manimgl/
│   ├── manim_imports_ext.py   # 统一导入（所有 Scene 使用 from manim_imports_ext import *）
│   ├── animations/            # 自定义动画（RotatingCreate, SpinInFromNothing 等）
│   ├── mobject/               # 自定义 Mobject（Hypercube, CalabiYauSurface 等）
│   ├── utils/                 # 工具函数（spiral_path, rotation_matrix_4d）
│   ├── scenes/                # 正式场景（按主题子目录组织）
│   ├── playground/            # 实验/测试场景
│   ├── shader_surface/        # GLSL 着色器
│   └── custom_config.yml      # ManimGL 配置
└── manimce/
    └── scene/                 # ManimCE 场景（Fourier, Gauss, Lorentz 等）
```

## 快速开始

### 安装依赖

```bash
# 使用 uv（推荐）
cd manimgl
uv sync

# 或使用 pip
pip install manimgl>=1.7.2 pyperclip>=1.11.0
```

### 环境配置

```bash
# Windows (PowerShell)
$env:PYTHONPATH = "D:\GitHub\manim_project\manimgl"

# Windows (cmd)
set PYTHONPATH=D:\GitHub\manim_project\manimgl

# Linux/macOS
export PYTHONPATH=$(pwd)/manimgl
```

### 运行场景

```bash
# ManimGL（交互式）
manimgl manimgl/playground/Hypercube.py HypercubeScene
manimgl manimgl/scenes/logo.py LogoScene

# ManimCE（渲染）
manim -pql manimce/scene/Lorentz/Lorentz_factor.py LorentzFactorScene   # 低质量预览
manim -pqh manimce/scene/Fourier/fourier_series.py FourierSeriesScene   # 高质量渲染
```

## 交互式开发（VS Code 插件）

项目包含自定义的 **ManimGL Interactive** VS Code 扩展，支持 Checkpoint 增量开发：

```python
from manim_imports_ext import *

class MyScene(Scene):
    def construct(self):
        # 创建标题 ← 插件检测为 Checkpoint，显示 CodeLens 按钮
        title = Text("Hello ManimGL", font_size=72)
        self.add(title)

        # 添加动画 ← 第二个 Checkpoint，可独立执行
        circle = Circle(radius=2.0, color=BLUE)
        self.play(RotatingCreate(circle))
```

**工作流**：点击 `▶ Run Scene` 启动 → 修改代码 → 点击 `▶ CheckpointPaste` 重新执行该段 → 立即看到变化

### 快捷键

| 操作 | Windows/Linux | macOS |
|------|--------------|-------|
| 运行 Scene | `Ctrl+Shift+R` | `Cmd+Shift+R` |
| Checkpoint Paste | `Alt+Shift+C` | `Cmd+Shift+C` |
| 复制相机状态 | `Ctrl+Alt+C` | `Cmd+Alt+C` |
| 退出 Scene | `Ctrl+Shift+Q` | `Cmd+Shift+Q` |

### 预览窗口操作

- 拖拽鼠标 — 旋转视角
- 滚轮 — 缩放
- `q` — 退出预览
- `r` — 重置相机

## 配置文件

### ManimGL 配置（`manimgl/custom_config.yml`）

```yaml
directories:
  base: "D:/GitHub/manim_project/manimgl"
  subdirs:
    output: "D:/GitHub/manim_project/videos"
    raster_images: "../images/raster_image"

camera:
  resolution: (1920, 1080)
  background_color: "#000000"
  fps: 30

text:
  font: "CMU Serif"

embed:
  autoreload: True
```

## 常见问题

**Q: Checkpoint 按钮显示 🔒 锁定？**
先点击 `▶ Run Scene` 启动场景，checkpoint 才会解锁。锁定的 checkpoint 第一次点击解锁，第二次点击执行。

**Q: 运行时提示找不到模块？**
确保已设置 `PYTHONPATH` 环境变量指向 `manimgl/` 目录。

**Q: VS Code 不显示 CodeLens 按钮？**
确认：已安装 ManimGL Interactive 扩展、文件为 `.py`、包含 `class XXX(Scene):` 定义。

**Q: ManimGL vs ManimCE 怎么选？**
快速迭代用 ManimGL（交互式预览 + Checkpoint），最终输出用 ManimCE（高质量渲染）。

## 相关链接

- [ManimGL Interactive](https://github.com/EscapeTo5D/maningl-interactive) — 本项目配套的 VS Code 扩展
- [ManimGL](https://github.com/3b1b/manim) — 3Blue1Brown 的 Manim 库
- [ManimCE](https://github.com/ManimCommunity/manim) — Manim 社区版
- [ManimCE 官方文档](https://docs.manim.community/en/stable/)

## 许可证

MIT License