---
title: "Claudian Skills 触发方式与自定义技能配置"
type: llm
model: ""
created: 2026-06-07
updated: 2026-06-07
tags: [claudian, skills, obsidian]
links: []
aliases: []
---

# Claudian Skills 触发方式与自定义技能配置

> **对话背景**：用户想了解 Claudian 中 Skills 的各种触发方式，以及如何创建和优化自定义技能文件。

---

## 精选对话记录

> 按话题分段保留最有价值的原始对话内容。去除问候语、重复、跑题，保留信息完整的原始表述。可直接引用原文，也可做适度精简。

### 1. Skills 触发方式

**用户**：claudian 中 skills 的触发方式有哪些
**LLM**：介绍了 6 种触发方式：
- `/名称` 斜杠命令（主要方式）
- 内置 SDK Skills（deep-research、code-review 等）
- 仓库级自定义 Skills（`.claude/skills/{name}/SKILL.md`）
- Sub-Agent 配置调用（skills 字段间接触发）
- `userInvocable: false` 控制显隐
- 隐藏技能设置（Hidden Commands and Skills）

**用户**：`/{名称}` 需要加中括号吗
**LLM**：不需要，直接 `/技能名称` 即可

### 2. 自定义 Skills 的文件结构

**用户**：仓库级自定义 skills 需要先创建 skill 命名的文件夹吗
**LLM**：需要。结构为 `.claude/skills/{技能名称}/SKILL.md`，可通过 UI 自动创建或手动创建

**用户**：为什么 UI 没有创建选项，没有文件夹也能使用？
**LLM**：因为 Claudian 连接了 Claude Code SDK。SDK 有内置技能返回时，优先使用 SDK 技能列表，跳过 `.claude/skills/` 目录，UI 也不显示管理面板。当 SDK 断开时，才回退到本地 skills

### 3. SDK 连接说明

**用户**：断开 SDK 连接是什么意思，如何操作？
**LLM**："SDK 连接"指 Claudian 与 Claude Code CLI 的后台通信。断开后 Claudian 无法从 SDK 获取技能，会回退到 `.claude/skills/`。可在设置中清空 CLI Path 实现

### 4. SKILL.md 文件编写与修复

**用户**：帮忙评估我写的 SKILL.md
**LLM**：发现两个问题：
- **P0**：YAML 缺少关闭符 `---`，导致 `description` 未被解析
- **P1**：路径描述不够健壮，建议加 `vault 根目录` 前缀

**用户**：argumentHint 字段有什么用？
**LLM**：下拉菜单中的使用提示，告诉用户可传入什么参数

**用户**：帮修复 YAML
**LLM**：在 `description` 后加 `---` 关闭 YAML

---

## 关键信息点

> 从对话中提取的可复用信息 —— 概念解释、代码片段、方法步骤、事实论断等。每条独立可读，方便快速查阅。

- **概念 / Skills 触发方式**：Claudian 中 skills 主要通过 `/名称` 斜杠命令触发。触发方式包括：SDK 内置技能、本地自定义技能（`.claude/skills/{name}/SKILL.md`）、Sub-Agent 配置调用。前置 YAML 字段 `userInvocable` 控制是否出现在 `/` 下拉菜单中。
  来源：对话记录 §1

- **概念 / SDK 连接机制**：Claudian 连接 Claude Code CLI 时，SDK 内置技能优先显示，本地 `.claude/skills/` 被跳过且 UI 不显示管理面板。断开 SDK 后回退到本地 skills。
  来源：对话记录 §2-3

- **结构 / SKILL.md 文件格式**：自定义技能文件必须放在 `.claude/skills/{名称}/SKILL.md`。文件包含 YAML 前置元数据（name、description、argumentHint、userInvocable 等字段）和 Markdown 正文（作为 prompt）。YAML 必须用 `---` 正确关闭。
  来源：对话记录 §4

- **方法 / argumentHint 字段**：为技能添加使用提示，在 `/` 下拉菜单中显示，格式如 `argumentHint: "[主题/文件路径]"`，让用户知道可传入参数。
  来源：对话记录 §4
