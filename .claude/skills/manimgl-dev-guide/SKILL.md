---
name: manimgl-dev-guide
description: ManimGL Interactive VS Code 扩展开发指南。仅在 manimgl/ 目录（非 manimce/）工作时应用，或涉及 manimgl 插件、checkpoint_paste、maningl-preview 插件开发时应用。不适用于 ManimCE（manimce/）项目。包含 checkpoint 系统规则、插件架构、命令参考、项目约定。
---

# ManimGL Development Skill

> ManimGL Interactive VS Code 扩展（`maningl-preview`）的精准参考手册

## 文件导航

| 文件 | 内容 |
|------|------|
| [checkpoint-system.md](checkpoint-system.md) | Checkpoint 检测规则、两步解锁机制、状态机、`checkpoint_paste()` 命令格式 |
| [extension-architecture.md](extension-architecture.md) | 插件源码架构、命令注册表、CodeLens 生成逻辑、终端管理、ManimGL 路径解析 |
| [project-conventions.md](project-conventions.md) | `manim_imports_ext.py` 导入约定、自定义 Mobject、Scene 编写规范 |

---

## 快捷键完整参考

> 以下数据精确提取自 `package.json` keybindings

| 快捷键（Windows） | 快捷键（macOS） | 命令 | 触发条件 |
|----|----|----|---|
| `Ctrl+Shift+R` | `Cmd+Shift+R` | Run Scene | `editorLangId == python` |
| `Alt+Shift+C` | `Cmd+Shift+C` | CheckpointPaste | `editorLangId == python` |
| `Ctrl+Shift+Alt+R` | `Cmd+Shift+Alt+R` | CheckpointPaste (record) | `editorLangId == python` |
| `Ctrl+Shift+Alt+S` | `Cmd+Shift+Alt+S` | CheckpointPaste (skip) | `editorLangId == python` |
| `Ctrl+Shift+Q` | `Cmd+Shift+Q` | Exit Scene | `terminalFocus` |
| `Ctrl+C` | `Cmd+C` | Interrupt Scene | `terminalFocus && terminalName =~ /^ManimGL/` |
| `Ctrl+Alt+C` | `Cmd+Alt+C` | Copy Camera State | `terminalFocus` |
| `Ctrl+Alt+F` | `Cmd+Alt+F` | Comment Fold | `editorLangId == python && editorHasSelection` |

---

## VS Code 配置项

> 配置前缀：`maningl.*`，来源：`configuration.ts`

```json
{
  "maningl.manimglPath": "manimgl",
  "maningl.terminalName": "ManimGL Terminal",
  "maningl.autoSave": true,
  "maningl.copyCommandToClipboard": true,
  "maningl.projectRoot": "",
  "maningl.pythonPath": ""
}
```

| 配置项 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| `manimglPath` | string | `"manimgl"` | ManimGL 可执行文件名（自动定位）或绝对路径 |
| `terminalName` | string | `"ManimGL Terminal"` | 终端名称（复用同名终端） |
| `autoSave` | boolean | `true` | Run Scene 前自动保存文件 |
| `copyCommandToClipboard` | boolean | `true` | 运行时复制命令到剪贴板（附带 `--finder -w`） |
| `projectRoot` | string | `""` | `custom_config.yml` 所在目录。留空则自动向上搜索 |
| `pythonPath` | string | `""` | 设置 `PYTHONPATH` 环境变量 |

---

## 核心概念速查

- **Scene 检测**：正则 `/^(\s*)class\s+(\w+)\s*\(([^)]*Scene[^)]*)\)\s*:/` 匹配所有 Scene 子类
- **Checkpoint 检测**：正则 `/^\s+#\s*.+/` 匹配 `construct` 方法内的缩进注释行
- **代码块范围**：从注释行到下一个注释行之前（最后一个 checkpoint 到 Scene 结束前最后非空行）
- **终端关闭时**：自动重置所有 checkpoint 状态（`checkpointState.resetAll()`）
- **Windows 终端**：强制使用 `cmd.exe`（`shellPath: 'cmd.exe'`）
