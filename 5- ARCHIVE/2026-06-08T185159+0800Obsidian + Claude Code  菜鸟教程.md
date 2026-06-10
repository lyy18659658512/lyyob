---
title: "Obsidian + Claude Code | 菜鸟教程"
source: "https://www.runoob.com/obsidian/obsidian-claude-code.html"
author:
published:
created: 2026-06-08
description: "Obsidian + Claude Code  Obsidian 是主打本地存储的 Markdown 笔记工具，文件全部保存在你自己电脑的文件夹里，安全、私密、可离线使用，加上双向链接和海量插件，它特别适合程序员用来存代码、记笔记、做长期知识沉淀。 Claude Code 是 Anthropic 推出的 AI 编程助手，基于 Claude 大模型优化，擅长读代码、改代码、写代码、查问题。 我们可以在 Obsidian 里安装 Claud.."
tags:
  - "clippings"
---
## Obsidian + Claude Code

Obsidian 是主打本地存储的 Markdown 笔记工具，文件全部保存在你自己电脑的文件夹里，安全、私密、可离线使用，加上双向链接和海量插件，它特别适合程序员用来存代码、记笔记、做长期知识沉淀。

Claude Code 是 Anthropic 推出的 AI 编程助手，基于 Claude 大模型优化，擅长读代码、改代码、写代码、查问题。

我们可以在 Obsidian 里安装 Claudian 插件，把 Claude Code 直接集成进来，让 AI 帮你写文档、整理笔记和项目进度、自动推送每日 AI 热点，让笔记库变成智能工作空间。

![](https://www.runoob.com/wp-content/uploads/2026/02/aa515366-64b6-4aa6-ab35-5bc426885eb9.webp)

---

## 环境安装与配置

### 1、Obsidian 下载

我们需要先去 Obsidian 官方网站 [https://obsidian.md/download](https://obsidian.md/download) 下载 Obsidian，提供了各种系统版本:

![](https://www.runoob.com/wp-content/uploads/2026/02/500d33bf-7b0d-4faa-9a8c-6ed906569a99.png)

### 2、安装 Claude Code

终端执行（全局安装一次就好）：

```
npm install -g @anthropic-ai/claude-code
```

安装完成后，运行一次授权：

```
claude
```

它会让你登录 Claude 账号，完成 OAuth 授权（只需要做一次）。

> **注意：** 如果没有 Claude 账号，我们也可以用国内的大模型代替，参考： [Claude Code API 配置](https://www.runoob.com/claude-code/claude-code-setup.html) 。
> 
> Claude Code 详细内容参考： [https://www.runoob.com/claude-code/claude-code-tutorial.html](https://www.runoob.com/claude-code/claude-code-tutorial.html)

### 3、安装 Obsidian 社区插件 Claudian

我们可以从 GitHub Release [https://github.com/YishenTu/claudian/releases/latest](https://github.com/YishenTu/claudian/releases/latest) 下载 main.js、manifest.json 和 styles.css 这三个文件：

![](https://www.runoob.com/wp-content/uploads/2026/02/1e16e925-9c4f-427d-b083-1264dc5bb0e1.png)

在你的 Obsidian 库的插件文件夹 plugins 中（如果没有创建一个），新建一个名为 claudian 的文件夹，路径示例：

```
/path/to/vault/.obsidian/plugins/claudian/
```

**注：** /path/to/vault/ 需替换为你自己的 Obsidian 库实际路径。

仓库管理菜单可以看到详细的路径：

![](https://www.runoob.com/wp-content/uploads/2026/02/37ad34de-46b4-4881-b7e4-62e3c3c3f43a.png)

将下载好的三个文件复制到这个 claudian/plugins/ 文件夹中。

```
.obsidian/
└── plugins/
    └── claudian/
        ├── main.js         # 插件的编译后 JavaScript 主文件（包含所有逻辑）
        ├── manifest.json   # 插件元数据（ID、名称、版本、描述、最低 Obsidian 版本等）
        └── styles.css      # 插件的 CSS 样式
```

![](https://www.runoob.com/wp-content/uploads/2026/02/9617d366-9cb9-4f03-9df0-abb838fac4b6.png)

在 Obsidian 中启用该插件：设置 → 社区插件 → 开启「Claudian」插件开关。

![](https://www.runoob.com/wp-content/uploads/2026/02/c4dd25ea-a49a-46ae-9442-267d8b212e4f.png)

通过设置，可以设置为中文语言：

![](https://www.runoob.com/wp-content/uploads/2026/02/runoob_1780401700296.png)

![](https://www.runoob.com/wp-content/uploads/2026/02/runoob_1780401722669.png)

---

## 第一次使用 Claudian

打开任意笔记，左侧边栏会出现一个 机器人图标（或用命令面板 Ctrl/Cmd+P 输入 Claudian: Open Chat）:

![](https://www.runoob.com/wp-content/uploads/2026/02/2333faf8-13a6-4e06-8207-f7a5043836e3.png)

第一次打开会提示你选择 Claude 模型（可以设置国内的大模型），输入框打 / 会出现所有可用技能（skills）：

![](https://www.runoob.com/wp-content/uploads/2026/02/edd40563-697a-41c8-b62d-ccfc111a5f4e.png)

测试：

```
写一篇新笔记（最常用场景）text帮我写一篇关于「2026年最值得关注的5个AI编程工具」的文献笔记，格式用我 vault 里最常用的文献笔记模板，从今天更新的网页抓取信息
```

接下来就开始正常干活了：

![](https://www.runoob.com/wp-content/uploads/2026/02/6f08996e-ee76-422c-b1a6-8eda20caf63a.png)

### 功能与使用方法

通过侧边栏功能区图标或命令面板打开聊天侧边栏，选中文本并使用快捷键即可进行行内编辑。

所有操作都与你熟悉的编码代理（Claude Code、Codex、Opencode、Pi）一致 —— 与代理对话，它就能读取、写入、编辑和搜索你库中的文件。

- **行内编辑** — 选中文本或定位光标后按下快捷键，可直接在笔记中编辑内容，并提供单词级别的差异预览。
- **斜杠命令与技能** — 输入 / 或 $ 可调用可复用的提示词模板，或来自用户级 / 库级作用域的技能（Skills）。
- **@ 提及** - 输入 @ 可提及任何你希望代理处理的对象，包括库文件、子代理、MCP 服务器或外部目录中的文件。
- **规划模式** — 通过 Shift+Tab 切换。代理会先探索设计方案再执行实现，随后呈现规划内容供你确认。
- **指令模式 #** — 可在聊天输入框中添加精细化的自定义指令。
- **MCP 服务器** — 通过模型上下文协议（Model Context Protocol，支持标准输入输出、服务器发送事件、HTTP）连接外部工具。Claude 可在应用内管理库级 MCP；Codex 则使用其独立的命令行界面（CLI）管理 MCP 配置。
- **多标签页与对话** — 支持多聊天标签页、对话历史记录、对话分支、恢复对话及紧凑视图模式。