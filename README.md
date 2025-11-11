# 🎬 manim_project

## 项目介绍 | Introduction

这是一个基于Manim的数学动画制作项目。Manim是一个由3Blue1Brown创建的动画引擎，用于创建精美的数学解释视频。本项目包含各种数学概念的动画示例和自定义组件。

This is a mathematical animation project based on Manim. Manim is an animation engine created by 3Blue1Brown for creating beautiful math explanation videos. This project contains animation examples and custom components for various mathematical concepts.

## 📁项目结构 | Project Structure

- `manimgl/` - 使用ManimGL库的动画脚本和自定义组件
  - `animations/` - 动画效果模块
  - `mobject/` - 自定义图形对象
  - `code_test/` - 测试脚本
  - `shader_surface/` - 3D着色器表面相关代码
 
- `images/` - 储存的图像资源

## 🚀环境配置 | Setup

### 安装依赖 | Install Dependencies

```bash
# 安装ManimGL
pip install manimgl

# 安装ManimCE
pip install manim
```
### 环境变量
```
Windows:  set PYTHONPATH=项目根目录\manim_project\manimgl
Linux/macOS:  export PYTHONPATH=项目根目录/manim_project/manimgl
```
### 配置文件 | Configuration

## 📚 相关链接
- [ManimGL](https://github.com/3b1b/manim) - 3Blue1Brown的Manim库
- [ManimCE](https://github.com/ManimCommunity/manim) - Manim社区版
- [manimgl_docs](https://manimgl-zh.readthedocs.io/zh-cn/latest/) - manimgl中文文档
- [manimce_docs](https://docs.manim.community/en/stable/) - manimce官方文档


#### 脚本项目使用`manimgl/custom_config.yml`进行自定义配置，可根据需要修改分辨率、帧率等参数。


## 许可证 | License

MIT License