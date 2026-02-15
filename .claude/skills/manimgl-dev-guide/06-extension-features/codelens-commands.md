# VS Code 扩展功能说明

> Scene 检测、Checkpoint 系统、终端集成、CodeLens 按钮

## 核心功能

### 1. Scene 检测

#### 自动识别 Scene 类

插件自动检测所有 Scene 子类：

```python
from manim_imports_ext import *

class MyScene(Scene):              # ✅ 自动检测
    def construct(self):
        pass

class MovingCameraScene(MovingCameraScene):  # ✅ 自动检测
    def construct(self):
        pass
```

#### CodeLens 显示

在 `def construct(self):` 行显示 `▶ Run Scene` 按钮

---

## 2. Checkpoint 系统

### 核心概念

Checkpoint 是**注释行标记的代码块**，支持：
- 🔒 顺序解锁（必须按顺序执行）
- 📋 粘贴到交互窗口执行
- 🔄 快速迭代修改

### CodeLens 按钮状态

| 状态 | 图标 | 说明 |
|------|------|------|
| 场景未启动 | 🔒 Run Scene | 需要先运行场景 |
| 已解锁 | ▶ CheckpointPaste | 可以执行 |
| 已执行 | ✅ CheckpointPaste | 可以重新执行 |

### 使用流程

```
1. 运行 Scene (▶ Run Scene)
   ↓
2. Checkpoint 0 解锁 (▶ CheckpointPaste)
   ↓
3. 执行 Checkpoint 0 (✅ CheckpointPaste)
   ↓
4. Checkpoint 1 解锁 (▶ CheckpointPaste)
   ↓
5. 继续执行...
```

---

## 3. 终端集成

### 自动管理

- **自动创建**: 首次运行时创建终端
- **复用终端**: 使用固定名称的终端
- **环境变量**: 自动配置 PYTHONPATH

### 终端生命周期

```
扩展激活 → 创建 TerminalManager 单例
    ↓
运行 Scene → 获取/创建终端 → 发送命令
    ↓
终端关闭 → 自动重置所有 checkpoint 状态
```

---

## 4. 快捷键参考

### 编辑器操作

| 快捷键 | 功能 | 说明 |
|--------|------|------|
| `Ctrl+Shift+R` | Run Scene | 运行当前场景 |
| `Alt+Shift+C` | CheckpointPaste | 执行选区/当前 checkpoint |
| `Ctrl+Alt+F` | Comment Fold | 折叠选中的注释区域 |

### 终端操作

| 快捷键 | 功能 | 说明 |
|--------|------|------|
| `Ctrl+Shift+Q` | Exit Scene | 退出交互窗口 |
| `Ctrl+C` | Interrupt | 中断当前运行 |
| `Ctrl+Alt+C` | Copy Camera | 复制相机状态到剪贴板 |

---

## 5. 配置选项

### VS Code 设置

打开设置 (JSON):

```json
{
  // ManimGL 可执行文件路径
  "maningl.manimglPath": "manimgl",

  // 终端名称
  "maningl.terminalName": "ManimGL Terminal",

  // 运行前自动保存
  "maningl.autoSave": true,

  // 复制命令到剪贴板
  "maningl.copyCommandToClipboard": true,

  // 项目根目录（custom_config.yml 所在）
  "maningl.projectRoot": "",

  // PYTHONPATH 设置
  "maningl.pythonPath": ""
}
```

---

## 6. 实用技巧

### 快速切换 Scene

```python
class Scene1(Scene):
    def construct(self):
        # [▶ Run Scene] Scene1
        pass

class Scene2(Scene):
    def construct(self):
        # [▶ Run Scene] Scene2
        pass
```

### 选择性执行

手动选区执行：
1. 选中代码块
2. 按 `Alt+Shift+C`
3. 绕过 checkpoint 限制

### 相机状态复用

```bash
# 在终端中
>>> self.camera.frame.get_euler_angles()
# 输出: array([-0.52359878,  1.22173048,  0.        ])

# 按 Ctrl+Alt+C 复制
# 粘贴到代码:
frame.set_euler_angles(theta=-30*DEGREES, phi=70*DEGREES)
```

---

## 下一步

- 📖 [Checkpoint 深度教程](../02-checkpoint-system/index.md) - 详细使用说明
- 🎬 [Scene 模板库](../03-scene-templates/index.md) - 快速开始
- 💡 [代码示例](../05-code-examples/index.md) - 实际应用案例
