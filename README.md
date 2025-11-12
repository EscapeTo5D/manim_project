# Manim 数学动画项目

基于Manim的数学动画制作项目，包含各种数学概念的动画示例和自定义组件。

## 项目结构

- `manimgl/` - ManimGL库的动画脚本和自定义组件
  - `animations/` - 自定义动画效果
  - `mobject/` - 自定义图形对象 (超立方体、卡拉比-丘流形等)
  - `code_test/` - 测试脚本
  - `einstein_scene/` - 爱因斯坦主题场景

- `manimce/` - ManimCE库的场景
  - `Lorentz/` - 洛伦兹变换
  - `Fourier/` - 傅里叶级数
  - `Gauss/` - 高斯几何
  - `earth/` - 地球运动

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

### 运行示例

```bash
# ManimGL - 超立方体动画
manimgl manimgl/code_test/Hypercube.py HypercubeScene

# ManimCE - 洛伦兹变换 (预览+低质量)
manim -pql manimce/scene/Lorentz/Lorentz_factor.py LorentzFactorScene
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

- **动画类**: RotatingCreate, SpinShowCreation
- **数学对象**: Hypercube, CalabiYauSurface
- **工具函数**: rotation_matrix_4d(), spiral_path()

## 配置文件

- `manimgl/custom_config.yml` - ManimGL配置
- `pyproject.toml` - 项目依赖

## 相关链接

- [ManimGL](https://github.com/3b1b/manim) - 3Blue1Brown的Manim库
- [ManimCE](https://github.com/ManimCommunity/manim) - Manim社区版
- [ManimGL中文文档](https://manimgl-zh.readthedocs.io/zh-cn/latest/)
- [ManimCE官方文档](https://docs.manim.community/en/stable/)

## 许可证

MIT License