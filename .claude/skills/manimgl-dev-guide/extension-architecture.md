# 插件架构

> 插件源码位置：`D:\hong_projects\maningl-preview`

## 源码结构

```
src/
├── extension.ts                  # 入口，注册所有命令和 CodeLens Provider
├── commands/
│   ├── runScene.ts               # ▶ Run Scene - 构建并发送 manimgl 命令
│   ├── checkpointPaste.ts        # 快捷键触发的 checkpoint paste（Alt+Shift+C 等）
│   ├── runCheckpointFromComment.ts  # CodeLens 点击触发的 checkpoint paste（含两步解锁）
│   ├── copyCameraState.ts        # 复制相机状态（通过临时 Python 脚本 + pyperclip）
│   ├── commentFold.ts            # 注释折叠（模仿 Sublime Text CommentFold）
│   ├── exitScene.ts              # 退出/中断 Scene
│   └── index.ts                  # 命令导出
├── providers/
│   └── sceneCodeLensProvider.ts  # CodeLens 按钮生成（Scene 检测 + checkpoint 状态）
├── state/
│   └── checkpointState.ts        # Checkpoint 状态管理器（单例，Map<sceneName, state>）
├── terminal/
│   └── terminalManager.ts        # 终端管理器（单例，创建/复用/关闭终端）
├── config/
│   └── configuration.ts          # 配置读取（ManimConfig 接口）
├── python/
│   ├── sceneDetector.ts          # Scene 类检测（正则匹配 class 定义和 construct 方法）
│   └── pythonEnvironment.ts      # Python 环境检测（VS Code Python Extension API）
└── types/
    └── manim.ts                  # 类型定义（SceneInfo, RunSceneOptions, CheckpointPasteOptions）
```

---

## 命令注册表

> 来源：`extension.ts`，共 9 个命令

| 命令 ID | 实现 | 功能 |
|---------|------|------|
| `maningl-preview.runScene` | `runScene.ts` | 运行当前 Scene |
| `maningl-preview.checkpointPaste` | `checkpointPaste.ts` | 快捷键 checkpoint paste |
| `maningl-preview.checkpointPasteRecorded` | `checkpointPaste.ts` | checkpoint paste (record=True) |
| `maningl-preview.checkpointPasteSkipped` | `checkpointPaste.ts` | checkpoint paste (skip=True) |
| `maningl-preview.runCheckpointFromComment` | `runCheckpointFromComment.ts` | CodeLens 点击 checkpoint |
| `maningl-preview.exitScene` | `exitScene.ts` | 退出 Scene（`\x03quit` + 关闭终端） |
| `maningl-preview.interruptScene` | `exitScene.ts` | 中断动画（`\x03`） |
| `maningl-preview.commentFold` | `commentFold.ts` | 注释折叠 |
| `maningl-preview.copyCameraState` | `copyCameraState.ts` | 复制相机 reorient 代码 |

---

## 关键模块详解

### Scene 检测（`sceneDetector.ts`）

```typescript
// 匹配所有 Scene 子类
const classRegex = /^(\s*)class\s+(\w+)\s*\(([^)]*Scene[^)]*)\)\s*:/;
// 匹配 construct 方法
const constructRegex = /^\s*def\s+construct\s*\(\s*self\s*\)\s*:/;
```

**返回值**：`SceneInfo { name, lineNumber, constructLineNumber, baseClass }`

**检测逻辑**：
1. 逐行扫描匹配 `classRegex`
2. 从类定义行向下搜索 `construct` 方法
3. 遇到同级或更低级别缩进时停止搜索

### CodeLens Provider（`sceneCodeLensProvider.ts`）

**为每个 Scene 生成的按钮**：
1. `construct` 方法行上方 → `▶ Run Scene` 按钮
2. 每个缩进注释行 → checkpoint 按钮（状态取决于 `checkpointState`）

**checkpoint 代码块范围计算**：
- 起始行：注释行
- 结束行：下一个注释行前一行，或 Scene 末尾最后一个非空行

**场景未启动时**：所有 checkpoint 按钮显示为 `▶ Run Scene`，点击时：
- 传递参数 `[startLine, sceneName, checkpointIndex, totalCheckpoints]`
- `runScene` 使用 `-se startLine+1` 从该行启动并解锁到该位置

### 终端管理器（`terminalManager.ts`）

**生命周期**：
1. 首次 Run Scene → 创建终端（名称来自 `config.terminalName`，工作目录 = `projectRoot`）
2. 后续命令 → 复用同名终端（检查 `exitStatus === undefined`）
3. 终端关闭事件 → `checkpointState.resetAll()` 重置所有状态

**Windows 特性**：
- 终端强制使用 `cmd.exe`（`shellPath: 'cmd.exe'`）
- 新终端延迟 300ms 后发送命令

### ManimGL 路径解析（`pythonEnvironment.ts`）

**优先级**（3 级降级策略）：

1. **用户配置绝对路径**：`path.isAbsolute(configManimglPath)` → 直接使用
2. **终端自动激活**：`python.terminal.activateEnvironment === true`（默认） → 使用配置的名称（如 `manimgl`），依赖 VS Code 自动激活虚拟环境
3. **Python Extension API**：获取活动环境的 `executable.uri`，拼接 manimgl 路径（Windows 加 `.exe`），检查文件存在
4. **以上都失败** → 提示用户选择"打开设置"或"选择 Python 环境"

### Run Scene 命令（`runScene.ts`）

**项目根目录解析**：
1. 优先使用 `config.projectRoot`
2. 否则从文件目录向上搜索 `custom_config.yml`
3. 都没有则使用工作区根目录

**生成的命令格式**：
```bash
manimgl "文件路径" SceneName [-se 行号]
```

**剪贴板内容**（如果 `copyCommandToClipboard` 启用）：
```bash
manimgl "文件路径" SceneName [-se 行号] --finder -w
```

### Copy Camera State（`copyCameraState.ts`）

1. 写入临时 Python 脚本到 `os.tmpdir()/manim_preview_copy_cam.py`
2. 脚本通过 `exec(open(...).read())` 在 ManimGL IPython 环境中执行
3. 读取 `self.camera.frame` 的欧拉角、中心、高度
4. 格式化为 `reorient(θ, φ, γ, (x, y, z), h)` 并通过 `pyperclip` 复制
5. 使用 ANSI 转义序列清除终端中的命令行显示

### Comment Fold（`commentFold.ts`）

1. 在选中区域内找到同级缩进的注释行（跳过连续注释行）
2. 每两个注释行之间的代码折叠为一个区域
3. 从后往前折叠（避免行号偏移）
4. 使用 VS Code 内置 `editor.createFoldingRangeFromSelection`
