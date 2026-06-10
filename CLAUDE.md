# Obsidian 知识库 AI 操作指南

> 完整规范手册见 [[9 - SYSTEM/知识库操作规范]]，本文件仅包含 AI 操作所需的速查信息。

## 📁 知识库速览

```
收集（0 - INBOX / 0 - FLEETING）
  → 处理（1 - LIFE / 2 - WORK / 3 - KNOWLEDGE）
    → 归档（5- ARCHIVE）
         ↕
   配置（9 - SYSTEM）
   素材（6 - ATTACHMENTS）
   等待孵化（4 - CREATION）
```

## 🏷 type 与模板速查

AI 创建笔记时必须设置正确的 `type`。使用 Templater 插入模板。

| type | 模板文件 | 专属字段 |
|------|---------|---------|
| `fleeting` | [[9 - SYSTEM/Templates/闪念笔记模板]] | — |
| `diary` | [[9 - SYSTEM/Templates/日记模板]] | mood, weather |
| `goal` | [[9 - SYSTEM/Templates/目标模板]] | year, quarter |
| `project` | [[9 - SYSTEM/Templates/项目笔记模板]] | deadline |
| `meeting` | [[9 - SYSTEM/Templates/会议记录模板]] | attendees, project |
| `work-note` | [[9 - SYSTEM/Templates/工作杂记模板]] | — |
| `book` | [[9 - SYSTEM/Templates/读书笔记模板]] | author, cover, progress, links, aliases |
| `course` | [[9 - SYSTEM/Templates/课程笔记模板]] | platform, instructor |
| `article` | [[9 - SYSTEM/Templates/文章笔记模板]] | author, url |
| `llm` | [[9 - SYSTEM/Templates/对话日志模板]] | source, aliases |
| `atomic` | [[9 - SYSTEM/Templates/原子笔记模板]] | source |
| `dashboard` | — | — |
| `system` | — | — |

## 🔌 已安装插件

- **Templater** ✅ — 模板插入（路径：`9 - SYSTEM/Templates/`）
- **Dataview** ✅ — 数据查询
- **Calendar** ✅ — 日历导航
- **Remotely Save** ✅ — 多端同步
- **Weread** ✅ — 微信读书笔记自动导入
- _待安装：Quick Add、Omnisearch、Periodic Notes_

## 🛠 AI 操作规则

1. **文件路径**：始终使用 vault 相对路径（不要以 `/` 或 `D:\` 开头）
2. **文件引用**：使用 `[[wikilink]]` 格式，图片用 `![[image.png]]`
3. **创建文件时**：按命名规则命名，设置完整 YAML frontmatter + 正确的 type
4. **模板优先**：使用 Templater 模板创建笔记（路径 `9 - SYSTEM/Templates/`）
5. **有疑问先查 [[9 - SYSTEM/知识库操作规范]]**
