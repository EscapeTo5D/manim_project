# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

这是一个基于 Manim 的数学动画制作项目，同时使用 ManimGL 和 ManimCE 两个版本：
- **ManimGL** (manimgl/) - 3Blue1Brown 的原始版本，支持交互式开发和 Checkpoint 系统
- **ManimCE** (manimce/) - Manim Community Edition，用于高质量视频渲染

## 核心架构

### 统一导入系统

项目使用 `manimgl/manim_imports_ext.py` 作为所有场景文件的统一导入点：

```python
from manim_imports_ext import *
```

该文件集中管理所有依赖，包括：
- 标准 ManimGL 导入 (`from manimlib import *`)
- 自定义动画类
- 自定义 Mobject
- 工具函数
- 类型提示

**重要**: 创建新场景时始终使用 `from manim_imports_ext import *`，不要直接导入 `manimlib`。

### 模块化设计

项目采用三层模块化架构：

1. **animations/** - 自定义动画效果
   - `RotatingCreate` - 旋转创建动画
   - `SpinShowCreation` - 旋转显示创建
   - `ShowRotatingCreate` - 显示旋转创建
   - `SpinInFromNothing` - 从无旋转进入

2. **mobject/** - 自定义数学对象
   - `Hypercube` - 4D 超立方体的 3D 投影可视化
   - `CalabiYauSurface` - 卡拉比-丘流形（复数曲面）
   - `ComplexSurfaceWireframe` - 自定义曲面的线框渲染

3. **utils/** - 工具函数
   - `spiral_path` - 螺旋路径生成
   - `rotation_matrix_4d` - 4D 旋转矩阵计算

所有模块通过 `__init__.py` 导出，可直接通过 `manim_imports_ext.py` 使用。

## 常用命令

### ManimGL (交互式开发)

```bash
# 基础运行
manimgl <script.py> <SceneName>

# 示例：运行超立方体场景
manimgl manimgl/playground/Hypercube.py HypercubeScene

# 在指定场景文件中运行
cd manimgl
manimgl scenes/logo.py LogoScene
```

**ManimGL 特点**：
- 交互式预览窗口
- 支持 Checkpoint 增量开发
- 实时编辑和快速迭代
- 按 `q` 退出，`Ctrl+Shift+Q` 强制退出

### ManimCE (高质量渲染)

```bash
# 基础命令
manim [选项] <script.py> <SceneName>

# 常用选项
# -p : 预览视频 (自动打开视频播放器)
# -ql : 低质量 (480p, 15fps) - 快速预览
# -qh : 高质量 (1080p, 60fps) - 最终渲染
# -k : 保留中间文件
# -s : 跳过动画 (只显示最后一帧)

# 示例：低质量预览洛伦兹变换
manim -pql manimce/scene/Lorentz/Lorentz_factor.py LorentzFactorScene

# 示例：高质量渲染地球运动
manim -pqh manimce/scene/earth/earth_motion.py EarthMotionScene
```

### 环境配置

**Windows**:
```bash
# 设置 PYTHONPATH
set PYTHONPATH=D:\GitHub\manim_project\manimgl

# 或在 PowerShell 中
$env:PYTHONPATH = "D:\GitHub\manim_project\manimgl"
```

**Linux/macOS**:
```bash
# 设置 PYTHONPATH
export PYTHONPATH=$(pwd)/manimgl

# 添加到 ~/.bashrc 或 ~/.zshrc
echo 'export PYTHONPATH=$(pwd)/manimgl' >> ~/.bashrc
```

### 依赖安装

```bash
# 使用 uv (推荐)
cd manimgl
uv sync

# 或使用 pip
pip install manimgl>=1.7.2 pyperclip>=1.11.0
```

## 交互式开发工作流

### Checkpoint 系统

ManimGL 支持通过 Checkpoint 进行增量开发，这是快速迭代的关键：

1. **在注释行标记 Checkpoint**:
   ```python
   def construct(self):
       # Checkpoint 1: 创建标题
       title = Text("Hello ManimGL")
       self.add(title)

       # Checkpoint 2: 添加圆形
       circle = Circle()
       self.play(Create(circle))
   ```

2. **使用 VS Code 扩展**:
   - 点击注释行上方的 `▶ CheckpointPaste` 按钮
   - 或使用快捷键 `Alt+Shift+C` (Windows) / `Cmd+Shift+C` (Mac)

3. **Checkpoint 状态流转**:
   ```
   🔒 锁定 → ▶ 已解锁 → ✅ 已执行
     ↓         ↓           ↓
   首次运行   点击解锁   点击执行
   ```

4. **快速迭代**:
   - 修改 Checkpoint 后的代码
   - 重新点击 `▶ CheckpointPaste`
   - 立即看到变化，无需重新运行整个场景

### VS Code 扩展功能

项目包含自定义的 ManimGL Interactive VS Code 扩展，提供：

1. **Scene 检测** - 自动识别 Scene 类，显示 `▶ Run Scene` 按钮
2. **Checkpoint 系统** - 在注释行显示 Checkpoint 按钮
3. **终端集成** - 自动管理 ManimGL 终端
4. **快捷键支持**:
   - `Ctrl+Shift+R` - 运行 Scene
   - `Alt+Shift+C` - Checkpoint Paste
   - `Ctrl+Alt+C` - 复制相机状态
   - `Ctrl+Shift+Q` - 退出 Scene

详细说明见 `.claude/skills/manimgl-dev-guide/`。

## 创建新场景

### ManimGL 场景模板

```python
from manim_imports_ext import *

class MyScene(Scene):
    def construct(self):
        # Checkpoint 1: 初始化
        title = Text("My Animation", font_size=72)
        self.add(title)
        self.wait()

        # Checkpoint 2: 添加动画
        circle = Circle(radius=2.0, color=BLUE)
        self.play(RotatingCreate(circle))
        self.wait()

        # Checkpoint 3: 清理
        self.clear()
```

### 使用自定义组件

```python
from manim_imports_ext import *

class CustomMobjectScene(Scene):
    def construct(self):
        # 使用自定义 Hypercube
        hypercube = Hypercube()
        self.add(hypercube)

        # 使用自定义动画
        self.play(RotatingCreate(hypercube))
        self.wait()

        # 使用工具函数
        path = spiral_path(radius=2.0, coils=3)
        self.play(MoveAlongPath(hypercube, path))
```

## 配置文件

### ManimGL 配置 (manimgl/custom_config.yml)

关键配置项：
```yaml
directories:
  base: "D:/GitHub/manim_project/manimgl"
  subdirs:
    output: "D:/GitHub/manim_project/videos"
    raster_images: "../images/raster_image"
    vector_images: "../images/vector_images"

camera:
  resolution: (1920, 1080)
  background_color: "#000000"
  fps: 30

text:
  font: "CMU Serif"

embed:
  autoreload: True
```

## 开发最佳实践

1. **始终使用统一导入**
   ```python
   from manim_imports_ext import *  # ✅ 正确
   from manimlib import *            # ❌ 避免
   ```

2. **使用 Checkpoint 加速开发**
   - 在关键逻辑处添加 Checkpoint 注释
   - 利用增量迭代减少等待时间

3. **复用现有组件**
   - 优先使用 `animations/` 中的自定义动画
   - 复用 `mobject/` 中的数学对象
   - 参考 `playground/` 中的示例代码

4. **模块化新功能**
   - 新动画类放入 `animations/`
   - 新数学对象放入 `mobject/`
   - 新工具函数放入 `utils/`
   - 更新相应 `__init__.py` 导出

5. **场景文件组织**
   - 正式场景放入 `manimgl/scenes/`（按主题子目录组织）
   - 实验/测试场景放入 `manimgl/playground/`
   - 使用清晰的命名约定

## 扩展阅读

- `.claude/skills/manimgl-dev-guide/` - 完整的 ManimGL 开发指南
- [ManimGL 官方文档](https://github.com/3b1b/manim)
- [ManimCE 官方文档](https://docs.manim.community/en/stable/)
- `manimgl/playground/` - 实验场景和测试用例
