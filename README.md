# Manim 数学动画项目

基于Manim的数学动画制作项目，包含各种数学概念的动画示例和自定义组件。本项目同时使用 ManimGL 和 ManimCE 两个版本：
- **ManimGL** - 3Blue1Brown 的原始版本，支持交互式开发和 Checkpoint 系统
- **ManimCE** - Manim Community Edition，用于高质量视频渲染

## 核心架构

### 统一导入系统

项目使用 `manimgl/manim_imports_ext.py` 作为所有场景文件的统一导入点，这是项目的核心设计模式：

```python
from manim_imports_ext import *
```

该文件集中管理所有依赖，包括：
- 标准 ManimGL 导入 (`from manimlib import *`)
- 自定义动画类 (RotatingCreate, SpinShowCreation, ShowRotatingCreate, SpinInFromNothing)
- 自定义 Mobject (Hypercube, CalabiYauSurface, ComplexSurfaceWireframe)
- 工具函数 (spiral_path, rotation_matrix_4d)
- 类型提示 (Callable, Iterable, Tuple, Union)

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

## 交互式开发工作流

### Checkpoint 系统

ManimGL 支持通过 Checkpoint 进行增量开发，这是快速迭代的关键特性：

**基本用法**：

```python
from manim_imports_ext import *

class MyScene(Scene):
    def construct(self):
        # Checkpoint 1: 创建标题
        title = Text("Hello ManimGL")
        self.add(title)
        self.wait()

        # Checkpoint 2: 添加圆形
        circle = Circle(radius=1.0, color=BLUE)
        self.play(ShowCreation(circle))
        self.wait()

        # Checkpoint 3: 添加方形
        square = Square(side_length=1.5, color=RED)
        self.play(ShowCreation(square))
        self.wait()
```

**Checkpoint 状态流转**：

```
🔒 锁定 → ▶ 已解锁 → ✅ 已执行
  ↓         ↓           ↓
首次运行   点击解锁   点击执行
```

**快速迭代流程**：
1. 运行 Scene 后，Checkpoint 从锁定变为解锁状态
2. 修改 Checkpoint 后的代码
3. 点击 `▶ CheckpointPaste` 按钮重新执行该 Checkpoint
4. 立即看到变化，无需重新运行整个场景

### VS Code 扩展

项目包含自定义的 **ManimGL Interactive** VS Code 扩展，支持 Scene 检测、Checkpoint 系统和终端集成。

**快捷键支持**：

| 操作 | Windows/Linux | macOS |
|------|--------------|-------|
| 运行 Scene | `Ctrl+Shift+R` | `Cmd+Shift+R` |
| Checkpoint Paste | `Alt+Shift+C` | `Cmd+Shift+C` |
| 复制相机状态 | `Ctrl+Alt+C` | `Cmd+Alt+C` |
| 退出 Scene | `Ctrl+Shift+Q` | `Cmd+Shift+Q` |

**交互式预览窗口操作**：
- 拖拽鼠标 - 旋转视角
- 滚轮 - 缩放
- 按 `q` - 退出预览
- 按 `r` - 重置相机

## 快速开始

### 安装依赖

```bash
# 使用uv (推荐)
uv sync

# 或使用pip
pip install manim>=0.19.0 manimgl>=1.7.2
```

### 环境配置

```bash
# Windows
set PYTHONPATH=%cd%\manimgl

# Linux/macOS
export PYTHONPATH=$(pwd)/manimgl
```

### 创建第一个场景

创建 `my_first_scene.py`：

```python
from manim_imports_ext import *

class MyFirstScene(Scene):
    def construct(self):
        # Checkpoint 1: 创建文本
        title = Text("Hello ManimGL!", font_size=72)
        self.add(title)
        self.wait()

        # Checkpoint 2: 添加圆形
        circle = Circle(radius=2.0, color=BLUE)
        self.play(RotatingCreate(circle))
        self.wait()

        # Checkpoint 3: 添加方形
        square = Square(side_length=2.0, color=RED)
        self.play(ShowCreation(square))
        self.wait()
```

**运行场景的三种方式**：

1. **使用 CodeLens 按钮** - 点击 `▶ Run Scene` 按钮
2. **使用快捷键** - `Ctrl+Shift+R` (Windows) 或 `Cmd+Shift+R` (Mac)
3. **使用命令行** - `manimgl my_first_scene.py MyFirstScene`

### 运行示例场景

```bash
# ManimGL - 超立方体动画 (交互式)
manimgl manimgl/code_test/Hypercube.py HypercubeScene

# ManimGL - Logo 动画 (交互式)
manimgl manimgl/code_test/logo.py LogoScene

# ManimGL - Shader 测试 (交互式)
manimgl manimgl/code_test/shader_test.py ShaderTest

# ManimCE - 洛伦兹变换 (预览+低质量)
manim -pql manimce/scene/Lorentz/Lorentz_factor.py LorentzFactorScene

# ManimCE - 傅里叶级数 (高质量渲染)
manim -pqh manimce/scene/Fourier/fourier_series.py FourierSeriesScene
```

## 常用命令

```bash
# ManimGL
manimgl <script.py> <SceneName>

# ManimCE
manim [选项] <script.py> <SceneName>

# 选项:
# -p : 预览视频
# -ql : 低质量 (快速)
# -qh : 高质量
# -k : 保留中间文件
```

## 主要组件

### 自定义动画类 (animations/)
- **RotatingCreate** - 旋转创建动画
- **SpinShowCreation** - 旋转显示创建
- **ShowRotatingCreate** - 显示旋转创建
- **SpinInFromNothing** - 从无旋转进入

### 自定义数学对象 (mobject/)
- **Hypercube** - 4D 超立方体的 3D 投影可视化
- **CalabiYauSurface** - 卡拉比-丘流形（复数曲面）
- **ComplexSurfaceWireframe** - 自定义曲面的线框渲染

### 工具函数 (utils/)
- **spiral_path()** - 螺旋路径生成
- **rotation_matrix_4d()** - 4D 旋转矩阵计算

## 配置文件

### ManimGL 配置 (manimgl/custom_config.yml)

关键配置项说明：

```yaml
# 目录配置
directories:
  base: "D:/GitHub/manim_project/manimgl"      # 项目基础目录
  subdirs:
    output: "D:/GitHub/manim_project/videos"   # 视频输出目录
    raster_images: "../images/raster_image"    # 位图资源目录
    vector_images: "../images/vector_images"   # 矢量图资源目录

# 窗口配置
window:
  position_string: UR                           # 窗口位置 (右上角)
  monitor_index: 1                              # 显示器索引
  full_screen: False                            # 全屏模式

# 相机配置
camera:
  resolution: (1920, 1080)                      # 分辨率
  background_color: "#000000"                   # 背景颜色
  fps: 30                                       # 帧率
  background_opacity: 1.0                       # 背景不透明度

# 文本配置
text:
  font: "CMU Serif"                             # 默认字体
  alignment: "CENTER"                           # 文本对齐

# LaTeX 配置
tex:
  template: "default"                           # LaTeX 模板

# 开发模式配置
embed:
  autoreload: True                              # 自动重载模块
```

### 项目依赖 (pyproject.toml)

```toml
[project]
name = "manimgl_animation"
version = "0.1.0"
requires-python = ">=3.10"
dependencies = [
    "manimgl",              # ManimGL 核心库
    "pyperclip>=1.11.0",    # 剪贴板支持 (Checkpoint 功能)
    "setuptools<70",        # 打包工具
]
```

## 开发资源

### 项目内部资源

- **`.claude/skills/manimgl-dev-guide/`** - 完整的 ManimGL 开发指南
  - 5分钟快速入门
  - Checkpoint 深度教程
  - Scene 创建模板
  - 精选代码示例
  - 插件功能说明

- **`manimgl/code_test/`** - 各种示例场景和测试用例
  - `Hypercube.py` - 超立方体动画
  - `logo.py` - Logo 动画
  - `shader_test.py` - Shader 测试
  - `calabi_eq.py` - 卡拉比-丘成桐方程

### 外部资源

## 相关链接

- [ManimGL](https://github.com/3b1b/manim) - 3Blue1Brown的Manim库
- [ManimCE](https://github.com/ManimCommunity/manim) - Manim社区版
- [ManimGL中文文档](https://manimgl-zh.readthedocs.io/zh-cn/latest/)
- [ManimCE官方文档](https://docs.manim.community/en/stable/)
- [3Blue1Brown教程](https://www.youtube.com/c/3blue1brown) - 优秀的数学可视化视频

## 常见问题

### Q: Checkpoint 按钮是锁定的？
A: 先运行 `▶ Run Scene`，checkpoint 才会解锁。Checkpoint 需要在场景运行后才能使用。

### Q: 运行时提示找不到模块？
A: 确保已设置 PYTHONPATH 环境变量，或在 manimgl/ 目录下运行命令。

### Q: VS Code 扩展不显示 CodeLens？
A: 确认：
1. 已安装 "ManimGL Interactive" 扩展
2. 文件是 `.py` 后缀
3. 文件包含 `class XXX(Scene):` 定义
4. 在 manimgl/ 目录下工作

### Q: 如何使用自定义的 mobject？
A: 参考 `.claude/skills/manimgl-dev-guide/05-code-examples/mobject_reuse.py` 和 `manimgl/code_test/` 中的示例。

### Q: ManimGL 和 ManimCE 有什么区别？
A:
- **ManimGL** - 交互式开发，支持 Checkpoint，适合快速迭代
- **ManimCE** - 批量渲染，质量更高，适合最终输出

## 故障排除

### Windows 环境变量设置

**临时设置** (当前终端会话)：
```cmd
set PYTHONPATH=D:\GitHub\manim_project\manimgl
```

**永久设置**：
1. 右键"此电脑" → "属性" → "高级系统设置"
2. "环境变量" → "系统变量" → "新建"
3. 变量名：`PYTHONPATH`
4. 变量值：`D:\GitHub\manim_project\manimgl`

### 依赖安装问题

如果遇到依赖安装问题，尝试：
```bash
# 升级 pip
python -m pip install --upgrade pip

# 清理缓存
pip cache purge

# 重新安装
cd manimgl
uv sync
```

## 贡献指南

欢迎贡献！请遵循以下步骤：

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

**代码规范**：
- 使用 `from manim_imports_ext import *` 导入
- 添加 Checkpoint 注释以便交互式开发
- 在 `code_test/` 中提供示例代码
- 更新相关文档

## 许可证

MIT License

## 联系方式

- 问题反馈：[GitHub Issues](https://github.com/yourusername/manim_project/issues)
- 功能建议：[GitHub Discussions](https://github.com/yourusername/manim_project/discussions)

---

**项目状态**: 活跃开发中

**最后更新**: 2026-02-15