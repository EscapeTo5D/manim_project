# Checkpoint 系统详解

> ManimGL 交互式开发的核心能力

## 什么是 Checkpoint?

Checkpoint 是 ManimGL 的**增量开发机制**：
- 🎯 **注释行标记**：用注释分隔代码块
- ⚡ **即时执行**：粘贴到预览窗口立即运行
- 🔄 **快速迭代**：修改后重新执行，无需重启
- 🔒 **顺序解锁**：确保场景状态一致性

## 核心概念

### 1. Checkpoint 定义

Checkpoint = **注释行 + 后续代码块**

```python
class MyScene(Scene):
    def construct(self):
        # ✅ 这是一个 checkpoint
        circle = Circle()
        self.add(circle)

        # ✅ 这是另一个 checkpoint
        square = Square()
        self.add(square)
```

### 2. 检测规则

插件检测的注释模式（正则表达式）：
```typescript
/^\s+#\s*.+/  // 缩进的注释行
```

**有效注释**：
```python
        # Checkpoint 1: 添加圆形        ✅
        # 添加方形                       ✅
        # TODO: 实现动画                 ✅
```

**无效注释**：
```python
# 顶级注释（无缩进）                  ❌
class Scene(Scene):
    pass
```

### 3. 代码块范围

每个 checkpoint 的代码块 = **从注释到下一个注释之前**

```python
class MyScene(Scene):
    def construct(self):
        # Checkpoint 1
        circle = Circle()         # ← 代码块开始
        self.add(circle)          #
        self.wait()               # ← 代码块结束

        # Checkpoint 2
        square = Square()         # ← 下一个代码块
        self.add(square)
```

---

## 状态机详解

### 状态流转图

```
┌─────────────────────────────────────────────┐
│ 场景未启动                                   │
│  Checkpoint 0: 🔒 Run Scene                 │
│  Checkpoint 1: 🔒 Run Scene                 │
│  Checkpoint 2: 🔒 Run Scene                 │
└──────────────┬──────────────────────────────┘
               │ Run Scene
               ↓
┌─────────────────────────────────────────────┐
│ 场景已启动                                   │
│  Checkpoint 0: ▶ CheckpointPaste (可执行)    │
│  Checkpoint 1: 🔒 CheckpointPaste (锁定)     │
│  Checkpoint 2: 🔒 CheckpointPaste (锁定)     │
└──────────────┬──────────────────────────────┘
               │ 执行 Checkpoint 0
               ↓
┌─────────────────────────────────────────────┐
│ Checkpoint 0 已执行                          │
│  Checkpoint 0: ✅ CheckpointPaste (已完成)    │
│  Checkpoint 1: ▶ CheckpointPaste (可执行)    │
│  Checkpoint 2: 🔒 CheckpointPaste (锁定)     │
└──────────────┬──────────────────────────────┘
               │ 执行 Checkpoint 1
               ↓
┌─────────────────────────────────────────────┐
│ Checkpoint 0-1 已执行                        │
│  Checkpoint 0: ✅ CheckpointPaste            │
│  Checkpoint 1: ✅ CheckpointPaste            │
│  Checkpoint 2: ▶ CheckpointPaste (可执行)    │
└─────────────────────────────────────────────┘
```

### 状态图标说明

| 图标 | 状态 | 说明 |
|------|------|------|
| 🔒 CheckpointPaste | 锁定 | 需要先执行前一个 checkpoint |
| ▶ CheckpointPaste | 已解锁 | 可以执行 |
| ✅ CheckpointPaste | 已执行 | 已经执行过，可重新执行 |

### 解锁规则

1. **Checkpoint 0**：场景启动后自动解锁
2. **Checkpoint N**：在 Checkpoint N-1 执行后解锁
3. **锁定的 checkpoint**：点击会提示"先执行前一个 checkpoint"

---

## 使用示例

### 场景 1: 基础 Checkpoint 使用

```python
from manim_imports_ext import *

class BasicCheckpointScene(Scene):
    def construct(self):
        # Checkpoint 1: 创建标题
        title = Text("Checkpoint Demo")
        self.add(title)
        self.wait()

        # Checkpoint 2: 创建圆形
        circle = Circle(radius=1.5, color=BLUE)
        self.play(ShowCreation(circle))
        self.wait()

        # Checkpoint 3: 添加方形
        square = Square(side_length=2.0, color=RED)
        self.play(ShowCreation(square))
        self.wait()
```

**工作流程**：
1. 运行 Scene（`▶ Run Scene`）
2. 执行 Checkpoint 2（`▶ CheckpointPaste`）
3. 修改圆形颜色为 `YELLOW`
4. 重新执行 Checkpoint 2（`▶ CheckpointPaste`）
5. 立即看到黄色圆形！

### 场景 2: 手动选区执行

**绕过解锁限制**：

```python
class ManualSelectionScene(Scene):
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

---

## 高级用法

### CheckpointPaste 变体

| 命令 | 快捷键 | 说明 |
|------|--------|------|
| `checkpoint_paste()` | `Alt+Shift+C` | 标准执行 |
| `checkpoint_paste(record=True)` | `Ctrl+Shift+Alt+R` | 录制模式 |
| `checkpoint_paste(skip=True)` | `Ctrl+Shift+Alt+S` | 跳过预渲染 |

### 从注释行运行 Scene

使用 `-se` 参数直接跳转到指定 checkpoint：

```bash
manimgl script.py SceneName -se 15  # 从第 15 行开始运行
```

插件自动处理：点击锁定的 checkpoint 按钮会使用 `-se` 参数。

---

## 插件集成

### CodeLens 显示逻辑

插件根据场景状态动态显示按钮：

```typescript
// 场景未启动
if (!isSceneStarted) {
    title = '▶ Run Scene';
    tooltip = `运行 ${scene.name} 后解锁 checkpoint`;
}
// 场景已启动
else if (isExecuted) {
    title = '✅ CheckpointPaste';
} else if (isUnlocked) {
    title = '▶ CheckpointPaste';
} else {
    title = '🔒 CheckpointPaste';
}
```

### 状态管理

插件使用单例模式管理 checkpoint 状态：

```typescript
interface SceneCheckpointState {
    started: boolean;         // 场景是否已启动
    unlockedIndex: number;     // 已解锁的最大索引
    executedIndex: number;     // 已执行的最大索引
    totalCheckpoints: number;  // checkpoint 总数
}
```

终端关闭时自动重置所有状态。

---

## 最佳实践

### ✅ 推荐做法

```python
class GoodCheckpointScene(Scene):
    def construct(self):
        # 清晰描述每个 checkpoint 的目的
        # Checkpoint 1: 初始化场景
        title = Text("Title")
        self.add(title)

        # Checkpoint 2: 添加主要元素
        circle = Circle()
        self.play(ShowCreation(circle))

        # Checkpoint 3: 添加次要元素
        square = Square()
        self.play(FadeIn(square))
```

### ❌ 避免的做法

```python
class BadCheckpointScene(Scene):
    def construct(self):
        # 避免无意义的注释
        # Step 1
        title = Text("Title")

        # Step 2
        circle = Circle()

        # 避免在一个 checkpoint 中做太多事
        # 这会让增量开发失去意义
        title = Text("Title")
        circle = Circle()
        square = Square()
        # ... 100 行代码
```

---

## 下一步

- 📜 [最佳实践](./best-practices.md) - 命名规范、反例分析
- ⚡ [高级技巧](./advanced-techniques.md) - record/skip 参数、自定义导入
- 🎬 [Scene 模板](../03-scene-templates/index.md) - 可复用的模板
