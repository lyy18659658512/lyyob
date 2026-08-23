---
title: "Obsidian Web Clipper | 菜鸟教程"
source: "https://www.runoob.com/obsidian/obsidian-web-clipper.html"
author:
published:
created: 2026-06-08
description: "Obsidian Web Clipper  Obsidian Web Clipper 是 Obsidian 官方出品的浏览器扩展，它能将任何网页一键保存为本地的 Markdown 笔记。 Obsidian Web Clipper 免费、开源、无广告，是你构建个人知识库的利器。   安装  Web Clipper 支持所有主流浏览器，从对应商店安装即可。   浏览器安装链接 Chrome / Brave / Arc / VivaldiCh.."
tags:
  - "clippings"
---
## Obsidian Web Clipper

Obsidian Web Clipper 是 Obsidian 官方出品的浏览器扩展，它能将任何网页一键保存为本地的 Markdown 笔记。

Obsidian Web Clipper 免费、开源、无广告，是你构建个人知识库的利器。

### 安装

Web Clipper 支持所有主流浏览器，从对应商店安装即可。

| 浏览器 | 安装链接 |
| --- | --- |
| Chrome / Brave / Arc / Vivaldi | [Chrome Web Store](https://chromewebstore.google.com/detail/obsidian-web-clipper/cnjifjpddelmedmihgijeibhnjfabmlf) |
| Firefox | [Firefox Add-ons](https://addons.mozilla.org/en-US/firefox/addon/web-clipper-obsidian/) |
| Safari（iOS / macOS） | [App Store](https://apps.apple.com/us/app/obsidian-web-clipper/id6720708363) |
| Edge | [Edge Add-ons](https://microsoftedge.microsoft.com/addons/detail/obsidian-web-clipper/eigdjhmgnaaeaonimdklocfekkaanfme) |

安装完成后，点击浏览器工具栏中的 Obsidian 图标即可打开 Clipper 面板。

首次使用时，它会自动检测正在运行的 Obsidian 仓库并完成关联，无需额外配置。

我们可以在设置里面设置中文语言，点击 Obsidian 图标，点击设置按钮：

![](https://www.runoob.com/wp-content/uploads/2026/06/runoob_1780455188172.png)

常规选项中语言设置中文：

![](https://www.runoob.com/wp-content/uploads/2026/06/runoob_1780455158661.png)

---

## 核心功能

Web Clipper 提供两种主要使用方式：整页剪藏和高亮剪藏。

### 整页剪藏

打开任意网页，点击扩展图标，再点击「添加到 Obsidian」，页面内容就会以 Markdown 格式保存到你的仓库。

Web Clipper 会自动提取以下内容：

- 文章正文（去除广告和侧边栏）
- 标题、作者、发布日期、描述
- 页面 URL 和来源域名
- 代码块（保留语法高亮标记）、数学公式（LaTeX 格式）

![](https://www.runoob.com/wp-content/uploads/2026/06/runoob_1780454126644.png)

### 高亮剪藏

不想保存整篇文章？选中你感兴趣的段落，点击高亮按钮，只保存划线部分。

高亮内容会以引用块（>）的形式写入笔记。再次访问该页面时，你的高亮依然可见。

操作流程如下：

1. 用鼠标选中页面上的文字或图片
2. 点击扩展图标
3. 选择「高亮选中内容」
4. 积累好所有高亮后，点击「添加到 Obsidian」一次性保存

![](https://www.runoob.com/wp-content/uploads/2026/06/runoob_1780454859925.png)

也可以右击鼠标选中 Obsidian Web Clipper 保存：

![](https://www.runoob.com/wp-content/uploads/2026/06/runoob_1780454703611.png)

---

## 模板：让剪藏更聪明

这是 Web Clipper 最强大的功能。

默认情况下所有网页都以同一格式保存，而模板让你可以针对不同类型的网页定制保存结构。

我们可以在设置页面中模板选项下的 Default 中查看：

![](https://www.runoob.com/wp-content/uploads/2026/06/runoob_1780455390238.png)

### 内置模板类型

Web Clipper 官网展示了几种典型模板，适用于不同场景：

| 模板类型 | 提取内容 | 适用场景 |
| --- | --- | --- |
| 文章模板 | 自动填入 author、published、description，正文以文章格式保存 | 阅读内容、博客、新闻 |
| 食谱模板 | 提取食材列表（自动转为待办复选框 - \[ \]）、步骤、营养信息 | 烹饪清单管理，配合 Tasks 插件体验更佳 |
| 电影/书籍模板 | 提取导演、评分、时长、主演、简介等 | 配合 Dataview 插件制作观影记录数据库 |
| 学术论文模板 | 完整保留代码块和 LaTeX 公式 | arxiv、ACM Digital Library 等学术网站 |

### 创建自定义模板

在扩展设置 → 模板 → 新建模板中，你可以自定义以下内容：

| 配置项 | 说明 | 示例 |
| --- | --- | --- |
| 模板名称 | 模板的标识名称 | 「YouTube 视频」「GitHub 仓库」 |
| 笔记名称 | 支持变量 | {{title}} 或 {{date}}-{{title}} |
| 保存位置 | 指定仓库中的文件夹 | Clippings/Articles |
| Properties | 笔记顶部自动填入的结构化属性（YAML 前置元数据） | author、published、tags 等 |
| 笔记正文 | 完全自定义的 Markdown 模板 | 可嵌入变量和任意 Markdown 内容 |

### 模板自动触发

设置「模板触发条件」后，访问特定网站时会自动应用对应模板，无需手动选择。

| 触发条件 | 自动应用 |
| --- | --- |
| URL 包含 youtube.com | YouTube 模板 |
| URL 包含 arxiv.org | 论文模板 |
| URL 包含 amazon.com | 购物模板 |

---

## 模板变量速查

模板里可以使用变量自动填入页面数据，格式为 {{变量名}}。

### 常用预设变量

| 变量 | 说明 |
| --- | --- |
| {{title}} | 页面标题 |
| {{url}} | 当前 URL |
| {{author}} | 作者 |
| {{published}} | 发布日期 |
| {{description}} | 页面描述 |
| {{content}} | 正文内容（Markdown 格式） |
| {{highlights}} | 所有高亮内容 |
| {{date}} | 当前日期 |
| {{site}} | 网站名称 |
| {{domain}} | 域名 |
| {{image}} | 社交分享图片 URL |
| {{words}} | 字数统计 |

### 高级变量

Meta 变量 用于提取页面 <meta> 标签中的内容：

## 实例

{{meta:name:description}} ← description meta 标签  
{{meta:property:og:title}} ← Open Graph 标题

CSS 选择器变量 用于精准提取页面特定元素：

## 实例

{{selector:h1}} ← 提取 h1 标题文字  
{{selector:.author}} ← 提取 class 为 author 的元素  
{{selector:img.hero?src}} ← 提取特定图片的 src 属性

Schema.org 变量 用于从结构化数据中提取信息：

## 实例

{{schema:@Recipe:name}} ← 食谱名称  
{{schema:@Article:author}} ← 文章作者  
{{schema:author.name}} ← 不指定类型，直接取 author.name

AI 提示变量（Prompt 变量） 需要启用 Interpreter 功能才能使用：

## 实例

{{"用三句话总结本文"}}  
{{"提取文中所有人名，以列表形式返回"}}  
{{"将关键论点翻译为中文"}}

---

## 实用模板示例：文章剪藏

以下是一个完整的文章模板配置，可以直接在设置中创建并使用。

### 笔记名称

## 实例

{{date:YYYY-MM-DD}} {{title}}

### 保存位置

## 实例

Clippings/Articles

### Properties（YAML 前置元数据）

## 实例

span style="color: green;">  
category: Clippings: "{{author}}"  
published: "{{published}}"  
source: "{{url}}"  
site: "{{site}}"  
description: "{{description}}"  
tags: \[clippings, articles\]

### 笔记正文

## 实例

\> \[!info\] 来源  
\> 作者：{{author}} | 发布于：{{published}} | \[原文链接\]({{url}})  
  
{{content}}

---

## 隐私与数据所有权

这是 Web Clipper 相比 Pocket、Instapaper 等服务最大的优势。

- 所有内容存在本地。剪藏的笔记是你硬盘上的.md 文件，没有任何内容上传到服务器。
- 高亮和设置可以导出为 JSON，随时迁移，无锁定风险。
- 使用 Prompt 变量调用 AI 时，数据会发送给你配置的 AI 服务提供商（如 OpenAI），这是唯一可能涉及网络传输的场景。

---

## 常见问题

以下是使用 Web Clipper 时常见的问题及解决方法。

| 问题 | 解决方法 |
| --- | --- |
| 剪藏后在 Obsidian 里找不到文件？ | 检查扩展设置中的「仓库」是否指向了正确的 Obsidian 仓库，以及「笔记位置」里设置的文件夹是否存在。 |
| 正文内容提取不准确，夹杂了广告和导航栏？ | 在模板正文中改用 {{selector:article}} 或 {{selector:.post-content}} 等 CSS 选择器，针对具体网站精准提取内容。 |
| 能不能同时保存到多个仓库？ | 可以在扩展设置的「通用」页中添加多个仓库，在每个模板里分别指定目标仓库。 |
| Safari 上可以用吗？ | 可以。Safari 版本在 iOS 和 macOS 均可使用，从 App Store 安装。功能与桌面浏览器版本基本一致。 |

---