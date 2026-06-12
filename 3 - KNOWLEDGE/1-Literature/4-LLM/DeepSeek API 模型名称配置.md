---
title: DeepSeek API 模型名称配置
type: llm
source: 元宝（腾讯混元/DeepSeek）
created: 2026-06-09
updated: 2026-06-09
tags: []
links: []
aliases: []
---

# DeepSeek API 模型名称配置

## 对话背景

在 CC-Switch 中配置 DeepSeek 的 Anthropic 兼容 API 时遇到 HTTP 400 错误，原因是模型名称填写了带版本号的 `DeepSeek-V3.2`，而 API 只接受全小写的 `deepseek-v4-pro` 或 `deepseek-v4-flash`。对话包含了正确的配置参数以及 Pro 与 Flash 模型的区分。

## 精选对话记录

### 1. 错误原因与解决方法

**用户**：CC-SWITCH 配置后测试模型连不上，提示 `DeepSeek 检查失败: HTTP 400: {"error":{"message":"The supported API model names are deepseek-v4-pro or deepseek-v4-flash, but you passed DeepSeek-V3.2."}}`，是什么原因？

**LLM**：原因很简单——你在 CC-Switch 里配置的模型名称填的是 `DeepSeek-V3.2`，但 DeepSeek 的 Anthropic 兼容接口不接受这个字符串，只认 `deepseek-v4-pro` 或 `deepseek-v4-flash`（全小写、无版本号）。

**正确配置**：

| 配置项 | 正确值 |
|--------|--------|
| Base URL | `https://api.deepseek.com/anthropic` |
| Model / 主模型 | `deepseek-v4-pro`（推荐）或 `deepseek-v4-flash` |
| API Key | 你的 `sk-` 开头的 DeepSeek Key |

⚠️ 注意：
- 必须全小写，不能有空格、`[1m]` 后缀或版本号
- Base URL 末尾不要带多余斜杠 `/`
- 如果 CC-Switch 有"模型映射/Model Override"页面，确保没有残留的 `DeepSeek-V3.2`

### 2. V4 Pro 与 V4 Flash 的区别

**用户**：DeepSeek-V4-Pro 和 DeepSeek-V4-Flash 的区别是什么？

**LLM**：（对话中未提供具体回答内容，由用户自行查询）

---

## 关键信息点

- **事实 /** **API 规范**：DeepSeek Anthropic 兼容 API 端点接受 `deepseek-v4-pro` 和 `deepseek-v4-flash` 两种模型名称，必须全小写、不带版本号
  来源：对话记录 §1

- **方法 /** **CC-Switch 配置**：设置 Base URL 为 `https://api.deepseek.com/anthropic`，模型名填 `deepseek-v4-pro` 或 `deepseek-v4-flash`，URL 末尾不要加斜杠
  来源：对话记录 §1

- **事实 /** **错误原因**：HTTP 400 错误通常是因为传入了错误的模型名字符串（如 `DeepSeek-V3.2`、`deepseek-chat` 等），API 服务端校验不通过
  来源：对话记录 §1
