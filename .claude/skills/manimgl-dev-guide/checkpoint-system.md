# Checkpoint 系统

> 数据来源：`sceneCodeLensProvider.ts`、`checkpointState.ts`、`runCheckpointFromComment.ts`、`checkpointPaste.ts`

## 检测规则

**注释行检测正则**（`sceneCodeLensProvider.ts`）：

```typescript
const commentRegex = /^\s+#\s*.+/;  // 缩进的注释行（排除顶级注释）
```

**有效 checkpoint**：`construct` 方法内、有缩进的注释行。

**代码块范围**：从注释行开始，到下一个注释行之前。最后一个 checkpoint 的代码块到 Scene 结束前的最后一个非空行（跳过尾部空行）。

```python
class MyScene(Scene):
    def construct(self):
        # Checkpoint 0 ← 注释行，checkpoint 起始
        circle = Circle()        # ← 代码块 0
        self.add(circle)         # ← 代码块 0

        # Checkpoint 1 ← 下一个注释行 = checkpoint 0 结束，checkpoint 1 起始
        square = Square()        # ← 代码块 1
```

---

## 状态机与两步解锁机制

### 状态接口（`checkpointState.ts`）

```typescript
interface SceneCheckpointState {
    started: boolean;         // 场景是否已启动
    unlockedIndex: number;    // 已解锁的最大索引
    executedIndex: number;    // 已执行的最大索引
    totalCheckpoints: number;
}
```

### 解锁判定逻辑

```typescript
// checkpointState.isUnlocked()
return index === 0 || index <= executedIndex + 1 || index <= unlockedIndex;
```

- **Checkpoint 0**：只要 `started === true` 即始终可用
- **Checkpoint N**：当 `N <= executedIndex + 1` 或 `N <= unlockedIndex` 时可用

### CodeLens 按钮状态

| 场景状态 | 图标 | 点击行为 |
|---------|------|---------|
| 场景未启动 | `▶ Run Scene` | 执行 `runScene`（带 `-se` 跳到该 checkpoint 行并解锁到该位置） |
| 已解锁（未执行） | `▶ CheckpointPaste` | 执行 checkpoint 代码块，标记为已执行 |
| 已执行 | `✅ CheckpointPaste` | 重新执行（可反复执行） |
| **锁定** | `🔒 CheckpointPaste` | **第一次点击 = 仅解锁**，弹出提示"已解锁 checkpoint N，再次点击执行"；**第二次点击 = 执行** |

### 状态流转图

```
场景未启动（所有 checkpoint 显示 ▶ Run Scene）
    │ 点击任意 ▶ Run Scene
    ↓
场景已启动
    Checkpoint 0: ▶ CheckpointPaste  ← 始终可用
    Checkpoint 1: 🔒 CheckpointPaste
    Checkpoint 2: 🔒 CheckpointPaste
    │ 执行 Checkpoint 0
    ↓
    Checkpoint 0: ✅ CheckpointPaste
    Checkpoint 1: ▶ CheckpointPaste  ← executedIndex+1 解锁
    Checkpoint 2: 🔒 CheckpointPaste
    │ 点击锁定的 Checkpoint 2
    ↓
    Checkpoint 2: ▶ CheckpointPaste  ← 仅解锁，不执行
    提示: "已解锁 checkpoint 3，再次点击执行"
    │ 再次点击 Checkpoint 2
    ↓
    Checkpoint 2: ✅ CheckpointPaste  ← 已执行
```

### 状态重置

- **终端关闭**：自动调用 `checkpointState.resetAll()`，清空所有场景状态
- **Exit Scene**（`Ctrl+Shift+Q`）：发送 `\x03quit`，延迟 500ms 后关闭终端 → 触发重置

---

## checkpoint_paste() 命令格式

### 由 CodeLens 触发（`runCheckpointFromComment.ts`）

1. 自动选中注释行到代码块结束的范围
2. 过滤空行后复制到剪贴板
3. 发送到终端：`checkpoint_paste() # 注释内容 (N lines)`
4. 清除选区，1 秒后焦点回编辑器

### 由快捷键触发（`checkpointPaste.ts`）

**单行非注释代码**（无选区或选中单行代码）：
- 直接发送该行代码到终端（不包装为 `checkpoint_paste()`）

**多行或注释开头**：
- 格式：`checkpoint_paste([args]) # 注释 (N lines)`
- `args` 可选值：
  - 空（标准执行）→ 快捷键 `Alt+Shift+C`
  - `record=True`（录制模式）→ 快捷键 `Ctrl+Shift+Alt+R`
  - `skip=True`（跳过预渲染）→ 快捷键 `Ctrl+Shift+Alt+S`

### 手动选区执行

选中任意代码后按 `Alt+Shift+C`：
- **绕过解锁限制**，直接执行选中代码
- **不影响** checkpoint 进度状态
- 选中的代码中注释只允许出现在第一行

---

## 从注释行启动 Scene（-se 参数）

当场景未启动时，点击某个 checkpoint 的 `▶ Run Scene` 按钮：

```bash
manimgl "script.py" SceneName -se 行号   # 行号从 1 开始（0-based + 1）
```

同时：
- 标记场景为已启动（`startScene()`）
- 解锁到该 checkpoint 位置（`unlockTo()`）

---

## 编写规范

### ✅ 推荐

```python
class MyScene(Scene):
    def construct(self):
        # 清晰描述目的的注释（会被检测为 checkpoint）
        circle = Circle(color=BLUE)
        self.play(Create(circle))

        # 每个 checkpoint 职责单一
        self.play(circle.animate.shift(RIGHT))
```

### ❌ 避免

- **一个 checkpoint 代码块过长**（失去增量开发优势）
- **顶级注释**（不缩进的注释不会被检测）
- **无意义注释**（如 `# TODO`、`# test`）
- **在 `construct` 方法外的注释**（不会被检测）
