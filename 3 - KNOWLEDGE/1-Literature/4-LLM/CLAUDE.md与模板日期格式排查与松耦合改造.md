---
title: "CLAUDE.md与模板日期格式排查与松耦合改造"
type: llm
model: ""
created: 2026-06-07
updated: 2026-06-07
tags: [配置, Templater, 工作流, CLAUDE.md, 设计模式]
links: []
aliases: []
---

# CLAUDE.md与模板日期格式排查与松耦合改造

> **对话背景**：用户发现对话日志模板和闪念笔记模板生成的文件名日期格式不同，疑为全局设置问题。经排查发现根源在于 CLAUDE.md 使用 `YYYY-MM-DD`（带 `-`），而 Templater 模板使用 `YYYYMMDD`（无 `-`），Claude 按 CLAUDE.md 直接写文件、用户通过 Templater 创建文件，两套路径用了不同格式。第一轮将 CLAUDE.md 硬编码为 `YYYYMMDD`；用户指出若日后改模板格式仍会脱钩，第二轮改为 CLAUDE.md 引用模板格式，实现松耦合。

---

## 精选对话记录

> 按话题分段保留最有价值的原始对话内容。去除问候语、重复、跑题，保留信息完整的原始表述。可直接引用原文，也可做适度精简。

### 1. 定位问题：日期格式写死在模板文件中

**用户**：为什么对话日志模板和闪念日志模板的文件名日期格式不一样，在哪里设置

**LLM**：两个模板的日期格式由各自文件中的 `tp.date.now()` 调用独立控制——对话日志用 `YYYYMMDD`（8位），闪念笔记用 `YYYYMMDDHHmm`（12位）。Templater 全局配置 `date_format: "YYYY-MM-DD"` 仅是不传参时的默认值，模板中传了显式参数所以不受影响。

### 2. 发现矛盾：模板写的是无 `-` 格式，实际文件却有 `-`

**用户**：现在对话日志文件名日期会带-符

**LLM**：检查现有文件（如 `2026-06-07_群论中的函数群与双射条件.md`）确认带 `-`。排查模板代码确认写的是 `tp.date.now("YYYYMMDD")`（无 `-`），与实际文件矛盾。

### 3. 根源：Claude 按 CLAUDE.md 创建，未经过 Templater

**用户**：文件是你创建的，你创建的没有通过 Templater 创建吗？

**LLM**：意识到问题——Claude 创建文件时遵循的是 CLAUDE.md 的工作流规范 `原始资料/对话日志/{YYYY-MM-DD}_{主题}.md`，直接写入文件系统，没有经过 Templater，所以用了 CLAUDE.md 的 `YYYY-MM-DD` 格式，而非模板的 `YYYYMMDD`。

### 4. 第一轮修复：CLAUDE.md 硬编码为模板格式

**用户**：我希望你依然遵循CLAUDE.md，然后CLAUDE.md定义你创建时要按模板来创建

**LLM**：将 CLAUDE.md 两处日期格式改为 `YYYYMMDD`（无 `-`）：来源摘要示例 `2026-06-04_` → `20260604_`；对话日志工作流 `{YYYY-MM-DD}_{主题}` → `{YYYYMMDD}_{主题}`。

### 5. 用户指出隐患：硬编码仍会脱钩

**用户**：这样还是有问题，如果我更改模板日期格式，但是CLAUDE.md没有跟着更改，你还是会按CLAUDE.md约定的来

**LLM**：认识到问题本质——`YYYYMMDD` 仍是硬编码在 CLAUDE.md 中，与模板是"复制关系"而非"引用关系"。模板一改，CLAUDE.md 必然脱钩。

### 6. 第二轮修复：引用模板格式，松耦合

**LLM**：将 CLAUDE.md 从硬编码改为"日期格式遵循 `[[_templates/对话日志模板.md]]` 中 `tp.date.now()` 的格式"，以模板作为唯一事实来源（Single Source of Truth），不再写死具体格式字符串。

### 7. 用户更改模板后正则同步修复

**用户**：我已经更改模板了（`YYYYMMDD` → `YYYYMMDDHHmm`），为什么你的模板名字没有变化

**LLM**：同步将 `_templates/对话日志模板.md` 中的正则从 `/^\d{8}_/` 改为 `/^\d{12}_/`，与 `tp.date.now("YYYYMMDDHHmm")` 的 12 位前缀匹配。

---

## 关键信息点

> 从对话中提取的可复用信息 —— 概念解释、代码片段、方法步骤、事实论断等。每条独立可读，方便快速查阅。

- **文件名日期格式的设置位置**：日期格式直接写在每个模板文件的 `tp.date.now("格式字符串")` 中，没有全局统一的设置入口。Templater 的 `date_format` 配置仅用于 `tp.date.now()` 不传参时的默认值。
  来源：对话记录 §1

- **Templater `tp.date.now()` 函数签名**：`tp.date.now(format = "YYYY-MM-DD", offset?, reference?, reference_format?)`。第一个参数即 Moment.js 格式字符串，默认为 `"YYYY-MM-DD"`，显式传入则覆盖默认。
  来源：对话记录 §1

- **CLAUDE.md 与模板的双轨问题**：当 Claude 按 CLAUDE.md 创建文件和用户按 Templater 模板创建文件时，如果两者约定的格式不同会导致不一致。Claude 直接写文件系统，不经过 Obsidian/Templater。
  来源：对话记录 §3

- **硬编码 vs 引用的设计模式**：两处需保持格式一致时，"复制关系"（两处写一样的内容）不如"引用关系"（一处定义、另一处引用）可靠。前者改了一处另一处必然脱钩。
  来源：对话记录 §5–6

- **模板作为唯一事实来源（Single Source of Truth）**：CLAUDE.md 不复制模板中的具体格式，而是声明"遵循模板中的格式"。模板的 `tp.date.now()` 是最终定义。
  来源：对话记录 §6

- **正则匹配与日期格式的一致性要求**：模板中的日期前缀正则（如 `/^\d{12}_/`）必须与 `tp.date.now()` 的格式字符串生成的位数匹配，否则会导致弹窗逻辑异常。改了 `tp.date.now()` 的格式后必须同步改正则。
  来源：对话记录 §7
