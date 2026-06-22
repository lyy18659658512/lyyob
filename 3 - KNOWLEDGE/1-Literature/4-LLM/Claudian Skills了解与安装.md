---
title: "Claudian Skills 了解与安装"
type: llm
model: ""
created: 2026-06-07
updated: 2026-06-07
tags: [claudian, skills, obsidian]
links: []
aliases: []
---

# Claudian Skills 了解与安装

> **对话背景**：用户想了解 GitHub 上有哪些好用的 Claudian 专用 Skills，从了解逐步深入到安装使用。


## 精选对话记录

### 1. GitHub 上 Claudian 可用 Skills 概览

**用户**：github上有哪些好用的claudian专用的skills
**LLM**：介绍了多个仓库，核心推荐：
- **kepano/obsidian-skills**（Obsidian CEO 编写，5 个 Skill）
- **axtonliu/axton-obsidian-visual-skills**（可视化：Excalidraw/Mermaid/Canvas）
- **gebicundewazi/obsidian-vault-claude-skill**（4 模式知识管理）
- **ashish141199/obsidian-claude-code**（模板+Slash Commands）
- **somasays/skill-creator**（元技能：创建自定义 Skill）

### 2. kepano/obsidian-skills 详细介绍

**用户**：kepano/obsidian-skills介绍一下有哪些用处
**LLM**：详述其 5 个 Skill：
- `obsidian-markdown`：Wiki 链接、Callout、Frontmatter、Dataview 等
- `json-canvas`：`.canvas` 画布的 JSON 结构生成
- `obsidian-bases`：Bases 数据库视图（表/看板/日历等）
- `obsidian-cli`：命令行操作知识库
- `defuddle`：网页→纯净 Markdown 提取

### 3. obsidian-markdown 的使用方式

**用户**：obsidian-markdown这个SKILL要如何使用？
**LLM**：解释其被动技能机制——装好后自动生效，无需手动调用。用户只需正常说话（"写条笔记"、"加个 Callout"），输出自动符合 Obsidian 语法。

**用户**：是不是可以理解为它是一个被动技能，不需要主动调用
**LLM**：确认，类比游戏"被动光环"，始终后台生效。

**用户**：帮我装进去
**LLM**：克隆 kepano/obsidian-skills，安装全部 5 个 Skill。

### 4. defuddle 使用说明

**用户**：defuddle这个如何使用
**LLM**：解释需先全局安装 `npm install -g defuddle`，之后被动生效——用户发链接时自动用 defuddle 替代 WebFetch 抓取。

### 5. skill-creator 介绍与安装

**用户**：skill-creator这个技能怎么用，有什么用处
**LLM**：介绍其为"造技能的技能"（元技能），可根据对话、文件、文档链接等工作流自动生成 SKILL.md。

**用户**：装上后，如果暂时没用，会影响我其他方面使用吗
**LLM**：不影响——所有 Skill 均为按需加载，日常仅占约 30-50 tokens 的元信息。

**用户**：装上
**LLM**：克隆安装到 `.claude/skills/skill-creator/`。

### 6. 提供工作流的方式

**用户**：使用skill-creator这个技能时，一般我提供流程的方式有哪些？
**LLM**：四种方式——①直接对话描述 ②结合现有文件提炼 ③提供参考文档链接 ④从历史对话捕捉。


## 关键信息点

- **概念 / Skill（技能）**：SKILL.md 文件，包含 YAML 元信息 + Markdown 指令体 + 可选资源文件。采用渐进式加载（元信息常驻→触发时加载正文→按需读取引用文件）。**均为被动触发，按需加载，不占上下文**。来源：对话记录 §1-3

- **方法 / 安装第三方 Skill**：克隆 GitHub 仓库到 `.claude/skills/<skill-name>/` 目录即可生效。来源：对话记录 §3

- **方法 / 使用 skill-creator**：自然语言描述工作流→LLM 提取步骤→生成 SKILL.md→测试→交付。提供流程的四种方式：对话描述、引用文件、提供文档链接、从历史对话提取。来源：对话记录 §6

- **工具 / defuddle**：CLI 工具，`npm install -g defuddle` 安装，`defuddle parse <url> --md` 使用。自动过滤广告/导航，输出纯净 Markdown。来源：对话记录 §4

- **事实 / 当前已装 Skills（7 个）**：
  - `obsidian-markdown` — Obsidian 语法正确输出
  - `obsidian-bases` — Bases 数据库视图
  - `json-canvas` — Canvas 画布生成
  - `obsidian-cli` — CLI 操作
  - `defuddle` — 网页净化
  - `skill-creator` — 创建自定义 Skill
  - `对话总结` — 对话知识提取
  来源：对话记录 §3-5
