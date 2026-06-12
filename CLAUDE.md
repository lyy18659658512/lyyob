# Obsidian 知识库 AI 操作指南

> 完整规范手册见 [[9 - SYSTEM/知识库操作规范]]，本文件仅包含 AI 操作所需的速查信息。

## 📁 知识库速览

```
收集（0 - INBOX）
  → 处理（1 - JOURNAL / 2 - ACTION / 3 - KNOWLEDGE）
       ├── 2 - ACTION/1-Career/  ← 事业、副业、教学
       ├── 2 - ACTION/2-Learning/ ← 课程、读书、技能学习
       ├── 2 - ACTION/3-Life/    ← 财务、健康、日常
       └── 2 - ACTION/9-someday/ ← 孵化池
    → 归档（5- ARCHIVE）
         ↕
   配置（9 - SYSTEM）
   素材（6 - ATTACHMENTS）
   资源（7 - RESOURCE）
   等待孵化（4 - CREATION）
```

## 🏷 type 与模板速查

AI 创建笔记时必须设置正确的 `type`。使用 Templater 插入模板。

| type | 模板文件 | 专属字段 |
|------|---------|---------|
| `diary` | [[9 - SYSTEM/Templates/日记模板]] | mood, weather |
| `project` | [[9 - SYSTEM/Templates/项目笔记模板]] | status, progress, startDate, deadline, links |
| `book` | [[9 - SYSTEM/Templates/读书笔记模板]] | author, cover, progress, links, aliases |
| `course` | [[9 - SYSTEM/Templates/课程笔记模板]] | platform, instructor, url, progress, links, aliases |
| `article` | [[9 - SYSTEM/Templates/文章笔记模板]] | author, url, aliases |
| `llm` | [[9 - SYSTEM/Templates/对话日志模板]] | source, aliases |
| `atomic` | [[9 - SYSTEM/Templates/原子笔记模板]] | source, aliases |
| `dashboard` | — | — |
| `system` | — | — |

## 🔌 已安装插件

- **Templater** ✅ — 模板插入（路径：`9 - SYSTEM/Templates/`）
- **Dataview** ✅ — 数据查询
- **Calendar** ✅ — 日历导航
- **Remotely Save** ✅ — 多端同步
- **Weread** ✅ — 微信读书笔记自动导入

## 🛠 AI 操作规则

1. **文件路径**：始终使用 vault 相对路径（不要以 `/` 或 `D:\` 开头）
2. **文件引用**：使用 `[[wikilink]]` 格式，图片用 `![[image.png]]`
3. **创建文件时**：按命名规则命名，设置完整 YAML frontmatter + 正确的 type
4. **模板优先**：使用 Templater 模板创建笔记（路径 `9 - SYSTEM/Templates/`）
5. **有疑问先查 [[9 - SYSTEM/知识库操作规范]]**
