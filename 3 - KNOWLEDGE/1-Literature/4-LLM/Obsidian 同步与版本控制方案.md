---
title: Obsidian 同步与版本控制方案
type: llm
source: ""
created: 2026-06-10
updated: 2026-06-10
tags: []
links: []
aliases: []
---

# Obsidian 同步与版本控制方案

## 对话背景

用户在其 Obsidian 知识库（vault "第二大脑"）中已安装 Remotely Save 插件用于多端同步，并新安装了 Obsidian Git 插件。三次会话围绕 Git 插件的安装配置、.gitignore 规则的三轮优化、以及 Remotely Save 与 Git 的功能对比展开，最终确定了「Remotely Save 主力同步附件、Git 版本控制文字笔记」的分工策略。

## 精选对话记录

### §1 Remotely Save vs Obsidian Git 功能对比

**用户**：obsidian的第三方同步备份插件，remote和git功能上有什么不一样

**LLM**（检查 vault 状态后发现用户已安装 Remotely Save）：

| 维度 | Obsidian Git | Remotely Save |
|------|-------------|---------------|
| 后端存储 | Git 仓库（GitHub/GitLab/自建） | 云盘/对象存储（Dropbox, OneDrive, S3, WebDAV 等） |
| 本地依赖 | 需安装 Git + 基础配置 | 无额外依赖，纯 JS 实现 |
| 同步机制 | `git pull` + `git push` | 文件级上传/下载 |
| 冲突处理 | 手动解决 merge conflict | 「最后写入者胜」，无冲突干预 |
| 版本历史 | 完整 Git 历史，可回滚任意版本 | 依赖云服务自身的版本能力 |
| 移动端支持 | 有限（需 Termux 等额外工具） | 原生支持 Android/iOS |
| 加密 | 依赖 Git 平台（私有库默认加密传输） | 原生端到端加密，云端数据不可读 |
| 同步粒度 | 整个仓库 | 可配置忽略路径/文件 |
| 大文件/附件 | Git 对二进制文件不友好，仓库会膨胀 | 更适合含图片/附件的 vault |
| 本质 | **版本控制系统** | **文件同步工具** |
| 网络要求 | 必须能连接 Git 远程 | 支持多种传输协议，适应性强 |
| 首次上手难度 | 中等（需 Git 基础） | 低，选云服务→授权即可 |

**核心结论**：两者不是非此即彼，很多人**两者同时用**——Remotely Save 做日常多端同步（主力），Obsidian Git 做定期版本快照（辅助）。你的 vault 已用 Remotely Save，这个选择很合理：Windows 路径含中文 Git 偶尔有编码问题、移动端同步 Remotely Save 更流畅、微信读书插件附件多 Git 对二进制不友好。但缺少版本历史回溯能力是 Remotely Save 最大的短板。

---

### §2 Git 插件安装后配置指南

**用户**：我已经安装好git插件，设置界面需要配置哪些呢？

**LLM**（检查后发现当前状态）：

| 项目 | 状态 |
|------|------|
| Git 插件 | ✅ 已安装并启用（community-plugins.json 中存在 `obsidian-git`） |
| Git 本体 | ✅ 已安装（`git version 2.50.0.windows.1`） |
| Git 仓库初始化 | ❌ 未初始化（`fatal: not a git repository`） |
| `.gitignore` | ❌ 不存在 |
| 自动备份 | ❌ 已关闭（data.json 中所有间隔为 0） |

**执行操作：**

**① `git init`** 初始化仓库
```
Initialized empty Git repository in D:/Obsidian Notes/第二大脑/.git/
```

**② 创建 `.gitignore`**，排除无需跟踪的文件：

```
# Obsidian
.obsidian/workspace.json         # 工作区布局（打开的标签页、面板位置）
.obsidian/workspace-mobile.json  # 移动端工作区布局
.obsidian/cache/                 # 缓存目录（搜索索引、预览缓存等）
.obsidian/graph.json             # 图谱视图节点位置数据
.trash/                          # Obsidian 回收站
# OS files
Thumbs.db                        # Windows 图片缩略图缓存
.DS_Store                        # macOS 文件夹自定义属性缓存
desktop.ini                      # Windows 文件夹自定义配置
# Remotely Save 同步缓存
.remotely-save/
# Git 插件日志
obsidian-git-data.json
```

⚠️ 注意：`.obsidian/` 中的**核心配置文件**（`app.json`、`community-plugins.json`、`hotkeys.json`、`appearance.json`）**没有被忽略**，说明设备间会共享插件列表、外观设置和快捷键等配置。

**③ 调整插件设置**（编辑 data.json）：

| 设置项 | 改前 | 改后 | 说明 |
|-------|------|------|------|
| autoSaveInterval | 0 | 10 分钟 | 自动提交间隔 |
| autoPullOnBoot | false | true | 启动时自动拉取远程更新 |
| autoPushInterval | 0 | 0（保持不变） | 手动推送更安全 |
| pullBeforePush | true | true（保持不变） | 推送前先拉取，避免冲突 |

**④ 首次提交** — 插件自动备份已产生一笔 commit（`d362a1a vault backup: 2026-06-10 11:25:38`），验证 .gitignore 已生效（`git check-ignore .obsidian/workspace.json .obsidian/cache/` → 返回路径，表示被忽略）。

**后续确认**：Git 插件当前尚未连接任何 GitHub 远程仓库，仅限本地版本控制。

**LLM 给出的远程关联指引**：
```bash
cd "D:/Obsidian Notes/第二大脑"
git remote add origin https://github.com/你的用户名/仓库名.git
git branch -M main
git push -u origin main
```
注意：不要同时用 Git 和 Remotely Save 推同一个远程，否则会冲突。

---

### §3 .gitignore 配置分析与三轮优化

#### 第一轮：理解现有 .gitignore

**用户**：（粘贴 .gitignore 内容）解释一下这个配置忽略了哪些

**LLM**：逐项解析——

**Obsidian 相关（5项）**：`.obsidian/workspace.json`（工作区布局——每个设备不同，不应共享）、`.obsidian/workspace-mobile.json`（移动端布局）、`.obsidian/cache/`（搜索索引等缓存）、`.obsidian/graph.json`（图谱节点位置）、`.trash/`（回收站）

**操作系统文件（3项）**：`Thumbs.db`（Windows 缩略图缓存）、`.DS_Store`（macOS 文件夹元数据）、`desktop.ini`（Windows 文件夹配置）

**Remotely Save 插件（1项）**：`.remotely-save/`

**Git 插件（1项）**：`obsidian-git-data.json`

总结：设计合理——排除了平台/设备相关的临时数据、系统自动生成的垃圾文件、插件运行时状态文件。同时**保留了**笔记内容、模板、`.obsidian` 中的核心配置（插件列表、快捷键等）。

#### 第二轮：.claude/ 和 .claudian/ 应否忽略

**用户**：.claudian, .claude 那这两个文件夹会忽略吗？

**LLM**：不会。当前 .gitignore 只列出了具体路径，没有通配符模式，所以 Git 只忽略明确列出的那几项。.claudian/ 和 .claude/ 不在此列。评估两者性质：

| 文件夹 | 来源 | 用途 | 是否需跨设备同步 |
|-------|------|------|---------------|
| `.claude/` | **Claude Code**（终端 AI 编程工具） | 会话历史、技能定义、工作流脚本、本地设置 | ❌ 各设备独立生成，互不需要 |
| `.claudian/` | **Claudian**（当前 AI 助手） | 会话状态、缓存数据 | ❌ 同上 |

**与 `.obsidian/` 的对比**：`.obsidian/` 中的核心配置（app.json、hotkeys.json、community-plugins.json）应该同步因为对所有设备有用；而 `.obsidian/cache/`、`workspace.json`、`graph.json` 则忽略因为是各设备独立的。`.claude/` 和 `.claudian/` 的全部内容都类似于 `cache/` 和 `workspace.json`——每个设备独立、不需要共享。即使只在电脑端使用，同步到其他设备也没有意义，反而可能引起冲突、浪费同步流量。手机和平板端也不会生成这两个文件夹。

**用户**：加进去

**LLM**：执行 Edit 追加到 .gitignore：
```gitignore
# AI 辅助工具本地缓存（设备特有，无需同步）
.claude/
.claudian/
```

#### 第三轮：6 - ATTACHMENTS/ 应否忽略

**用户**：6 - ATTACHMENTS 这个是不是也要忽略？

**LLM**（检查后发现）：目录里目前有 2 张微信读书封面图片（`cover_我的几何人生：丘成桐自传.jpg` 59KB + `cover_我的教育观.jpg` 80KB，共 144KB），**未被 .gitignore 匹配**（`git check-ignore` exit 1），但**已被 Git 追踪**（`git ls-files` 可查到）。

**初始建议不忽略**：`6 - ATTACHMENTS/` 和 `.claude/` 性质完全不同——这是用户主动放入的笔记内容素材（笔记里通过 `![[cover_xxx.jpg]]` 引用），所有设备都需要。如果忽略掉，别人（或新设备）克隆仓库后笔记里的图片会断裂无法显示。

**用户**：未来会有越来越多图片

**LLM**（重新评估，考虑用户已有 Remotely Save）：

| 方案 | 做法 | 优缺点 |
|------|------|--------|
| **方案一 ✅ 推荐** | 忽略附件，依赖 Remotely Save 同步 | Git 永远轻量只有 .md；附件通过云存储对大文件更友好。缺点：附件没有 Git 版本历史 |
| 方案二 | 保持追踪 + Git LFS | 附件也有版本历史，但需服务端支持、配置复杂 |
| 方案三 | `.gitkeep` 保留目录但忽略内容 | 效果同方案一，多留个空目录占位 |

**推荐方案一的三点理由**：(1) 已在用 Remotely Save 附件同步有托底 (2) Git 只管文字 clone 极快 diff 清晰 (3) 附件用 Git 做版本控制实际价值接近于零

**用户**：方案一

**LLM**（执行）：
1. `.gitignore` 追加：
```gitignore
# 附件素材（由 Remotely Save 同步，Git 仅管理文字笔记）
6 - ATTACHMENTS/
```

2. 但发现 2 张图片已被 Git 追踪——**`.gitignore` 对已追踪文件无效**。需要先解除追踪：
```
git rm --cached "6 - ATTACHMENTS/cover_我的几何人生：丘成桐自传.jpg"
git rm --cached "6 - ATTACHMENTS/cover_我的教育观（丘成桐作品）.jpg"
```
（`--cached` 参数表示仅从 Git 索引移除，本地文件保留不变）

**用户**：Git 追踪是什么意思，什么时候设置的追踪？

**LLM**：用比喻解释——"Git 追踪"就是 Git 记下了这个文件，以后每次改动它 Git 都会注意到。已追踪的文件 `.gitignore` 无效，因为"你已经让我盯着它了，现在说别盯着了没用，得先让我松手（`git rm --cached`）"。

通过 `git log --follow` 查出追踪来源——commit `d362a1a`（2026-06-10 11:25，提交信息 `vault backup: 2026-06-10 11:25:38`）。这是 Obsidian Git 插件的自动备份做的全库 `git add`——当时 `.gitignore` 还没排除 `6 - ATTACHMENTS/`，所以那 2 张封面图被顺带加进去了。

---

## 关键信息点

- **概念 /** **版本控制 vs 文件同步**：Git 是版本控制系统（完整 Git 历史，可回滚任意版本），Remotely Save 是文件同步工具（「最后写入者胜」，无冲突干预），两者可互补使用。
  来源：对话记录 §1

- **方法 /** **Git 插件完整配置流程**：(1) `git init` 初始化仓库 (2) 创建 .gitignore 排除工作区布局/缓存/OS 垃圾文件 (3) 调整插件设置（autoSaveInterval=10min, autoPullOnBoot=true）(4) 首次提交建立基线版本 (5) 用 `git check-ignore` 验证 .gitignore 生效
  来源：对话记录 §2

- **方法 /** **GitHub 远程关联步骤**：`git remote add origin <url>` → `git branch -M main` → `git push -u origin main`。注意不要同时用 Git 和 Remotely Save 推同一个远程，会冲突。
  来源：对话记录 §2

- **事实 /** **推荐的分工策略**：Remotely Save 做日常多端同步（主力），Git 做定期版本快照（辅助）。附件素材（6 - ATTACHMENTS/）由 Remotely Save 同步，Git 仅管理文字笔记，保持仓库轻量、clone 快速、diff 清晰。
  来源：对话记录 §1, §3

- **事实 /** **.gitignore 完整忽略清单**：Obsidian 工作区布局（workspace.json / workspace-mobile.json）、缓存（cache/）、图谱节点位置（graph.json）、回收站（.trash/）、OS 垃圾文件（Thumbs.db / .DS_Store / desktop.ini）、Remotely Save 同步缓存（.remotely-save/）、Git 插件日志（obsidian-git-data.json）、AI 工具本地缓存（.claude/、.claudian/）、附件素材（6 - ATTACHMENTS/）
  来源：对话记录 §2, §3

- **方法 /** **处理已追踪文件的 .gitignore 升级**：.gitignore 只对未追踪文件生效。已追踪文件需先用 `git rm --cached` 从 Git 索引移除（保留本地文件），.gitignore 才能拦截后续提交。
  来源：对话记录 §3

- **概念 /** **Git 追踪的含义**：Git 追踪意味着该文件已被登记在 Git 的版本记录中——`git status` 会显示其变更、`git diff` 会对比其内容、`git add` 会暂存其修改。被忽略的文件对 Git 完全透明。
  来源：对话记录 §3

- **事实 /** **.claude/ 和 .claudian/ 无需跨设备同步**：这两个文件夹是终端 AI 工具（Claude Code / Claudian）的本地工作目录，存放会话历史、技能定义、工作流脚本等运行时数据。与 Obsidian 无关，各设备独立生成，同步无意义且可能冲突。手机和平板端也不会生成它们。
  来源：对话记录 §3

- **事实 /** **6 - ATTACHMENTS/ 追踪起因**：附件图片是在 2026-06-10 11:25 被 Obsidian Git 插件自动备份时的全库 `git add` 顺带加入的，当时 .gitignore 尚未排除该目录。之后已通过 `git rm --cached` 解除追踪，后续新图片自动被 .gitignore 拦截。
  来源：对话记录 §3
