# Obsidian 知识库 AI 操作指南

> **AI 角色**：你是知识库的协作者，不是管理员。结构性变更必须先提案、等确认、再执行。
> 完整规范手册见 [[9 - SYSTEM/知识库操作规范]]，本文件仅包含 AI 操作所需的速查信息。

## 📁 知识库速览

```
收集（0 - INBOX）
  → 处理（1 - JOURNAL / 2 - ACTION / 3 - KNOWLEDGE）
       ├── 1 - JOURNAL/YYYY-MM/ ← 日记按月份归档
       ├── 2 - ACTION/1-Career/  ← 事业、副业、教学
       ├── 2 - ACTION/2-Learning/ ← 课程、读书、技能学习
       ├── 2 - ACTION/3-Life/    ← 财务、健康、日常
       └── 2 - ACTION/9-someday/ ← 孵化池
    → 归档（5 - ARCHIVE）
         ↕
   配置（9 - SYSTEM）
   素材（6 - ATTACHMENTS）
   资源（7 - RESOURCE）
```

## 🏷 type 与模板速查

AI 创建笔记时必须设置正确的 `type`。使用 Templater 插入模板。

| type | 模板文件 | 专属字段 |
|------|---------|---------|
| `diary` | [[9 - SYSTEM/Templates/日记模板]] | mood, weather |
| `project` | [[9 - SYSTEM/Templates/项目笔记模板]] | status, progress, startDate, deadline, links |
| `book` | [[9 - SYSTEM/Templates/读书笔记模板]] | author, cover, progress, links, aliases |
| `course` | [[9 - SYSTEM/Templates/课程笔记模板]] | platform, instructor, url, progress, links, aliases |
| `article` | [[9 - SYSTEM/Templates/文章笔记模板]] | author, url, links, aliases |
| `llm` | [[对话日志模板]] | model, links, aliases |
| `atomic` | [[原子笔记模板]] | source, links, aliases |
| `dashboard` | — | — |
| `system` | — | — |

> `aliases` = 笔记别名，用于搜索，数组格式如 `["Agent课程", "吴恩达Agent课"]`。

## ⚠️ 三条铁律

编写 frontmatter 时必须遵守，详细规则见操作规范。

1. **tags 只写主题**：填 `AI`、`学习`、`数学` 这类跨领域主题词。**不填**类型词（`book`、`course`）——type 字段已经表达了。
2. **links 只写笔记名**：`[[项目笔记]]` 而非 `[[2 - ACTION/项目笔记]]`。优先用于连接 ACTION ↔ KNOWLEDGE。
3. **atomic 的 source**：从文献提炼时填 `[[文献名]]`，纯个人洞察留空即可。

## 🔌 已安装插件

- **Templater** ✅ — 模板插入（路径：`9 - SYSTEM/Templates/`）
- **Dataview** ✅ — 数据查询
- **Calendar** ✅ — 日历导航
- **Remotely Save** ✅ — 多端同步
- **Weread** ✅ — 微信读书笔记自动导入

## 🧩 可用 Skill

| Skill | 触发场景 |
|-------|---------|
| `conversation-log` | "保存这段对话"、"把聊天记录结构化" |
| `weread-book-note` | "整理读书笔记"、"处理微信读书笔记" |
| `consistency-check` | "知识库一致性检测"、"知识库体检" |
| `english-pdf-vocab` | "翻译关键词"、"中英对照"、"帮我读这个PDF"、"提取术语" |
| `bilibili-course` | "B站课程创建学习计划"、"拆解课程任务"、"把这个视频做成学习项目" |

## 🛠 AI 操作规则

0. **先提案再执行**：创建、修改、删除任何 vault 文件前，先说明计划，等你确认后再动手。纯查询/检索不受此限。
1. **路径**：始终使用 vault 相对路径（不要以 `/` 或 `D:\` 开头）
2. **引用**：使用 `[[wikilink]]` 格式，图片用 `![[image.png]]`
3. **创建文件**：按 [[9 - SYSTEM/知识库操作规范#文件命名规则\|命名规则]] 命名，用 Templater 插入模板，设完整 frontmatter + 正确 type
4. **正文 wikilink**：inline 优先，栏目只做补充
5. **系统变更后**：提醒用户可运行一致性检测（`consistency-check`）
6. **有疑问先查** [[9 - SYSTEM/知识库操作规范]]
7. **了解 Hook 系统**：以下 hooks 在对应时机自动运行，AI 应在首轮回复时报告 SessionStart 的输出：

| 时机                   | Hook 脚本                     | 功能                            |
| -------------------- | --------------------------- | ----------------------------- |
| `SessionStart`       | `check-inbox.sh`            | 统计 INBOX 待处理文件                |
| `SessionStart`       | `check-consistency-need.sh` | 检测系统文件自上次一致性检测以来是否有变更         |
| `PreToolUse → Bash`  | `block-dangerous.sh`        | 拦截危险命令（`rm -rf /` 等），输出警告或阻断  |
| `PreToolUse → Write` | `validate-frontmatter.sh`   | 对照模板校验新建笔记的 frontmatter 字段一致性 |
