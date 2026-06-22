---
title: "Claude Code Skills 渐进式设计与目录结构"
type: llm
model: "元宝"
created: 2026-06-14
updated: 2026-06-14
tags: []
links: []
aliases: []
---

# Claude Code Skills 渐进式设计与目录结构

## 对话背景

两段与腾讯元宝的对话，围绕 Claude Code 的 Skills 系统展开——第一段涵盖文件夹标准结构、可选文件的启用判据、以及各子目录的具体文件示例；第二段深入解释 Skills 三层渐进式披露设计理念。对话来源为 Obsidian INBOX 中两篇独立的元宝对话导出，因主题互补合并整理。

## 精选对话记录

> 按话题分段保留最有价值的原始对话内容。去除问候语、重复、跑题，保留信息完整的原始表述。可直接引用原文，也可做适度精简。

### 1. Skills 文件夹标准结构

**用户**：Claude Code 的 Skills 文件夹下一般有哪些文件和文件夹？

**LLM**（元宝 — 腾讯 AI 助手）：

Skills 文件夹分为两级存放：

| 作用域 | 路径 | 说明 |
|--------|------|------|
| **个人级** | `~/.claude/skills/` | 不在 git 中，仅本人可见 |
| **项目级** | `<项目根>/.claude/skills/` | 随仓库提交，团队共享 |

单个 Skill 文件夹的标准结构（文件夹名 = skill ID，kebab-case 命名）：

```
~/.claude/skills/
└── my-skill/                  ← 文件夹名 = skill ID（kebab-case）
    ├── SKILL.md              ← 【必需】核心文件，Claude 读的就是它
    ├── README.md             ← 可选，给人看的说明文档
    ├── scripts/              ← 可选，可执行脚本
    ├── references/           ← 可选，参考资料/静态数据
    ├── templates/            ← 可选，输出模板
    ├── assets/               ← 可选，静态资源
    └── docs/                 ← 可选，附加文档
```

SKILL.md 的格式要点：YAML frontmatter 必须包含 `name` + `description`；`description` 极其重要，Claude 靠它做自动匹配触发。正文建议不超过 500 行。

### 2. 可选文件的决策判据与文件举例

**用户**：可选文件是如何确定要不要的？

**LLM**（元宝）：

核心判据一句话：**Skills 采用"三层渐进式披露"（Progressive Disclosure）三层模型——能不加载就不加载，能执行就不当文本喂进上下文。**

| 层级 | 内容 | 何时在上下文中 |
|------|------|--------------|
| **L0 元数据层** | frontmatter（name + description） | ✅ 常驻，启动即读，~几十 Token |
| **L1 指令层** | SKILL.md 正文（步骤/规则/约束） | ✅ 任务匹配后加载，几百~几千 Tokens |
| **L2 资源层** | scripts / references / templates 等 | ✅ 执行阶段按需读取/调用 |

**用户**：每个子目录具体放什么、什么时候该用？

**LLM**（元宝）：

**scripts/ — 可执行脚本**

放真正会被 Claude 执行（而非阅读）的代码：shell、Python、Node 等。要它当且仅当：有确定性的机械计算/转换/校验（如解析二进制/Office/PDF、批量 rename、schema validate），或需要依赖 pip/npm 能装的库（pandas、pdfplumber 等）。

```
scripts/
├── setup.sh            # 环境初始化（安装依赖、创建目录）
├── extract-text.py     # 从 PDF/Office 提取纯文本
├── batch-rename.sh     # 批量重命名工具
├── validate.js         # JSON Schema 校验器
├── analyze-csv.py      # CSV 数据分析
└── deploy.sh           # 部署脚本
```

不要放：密钥/secrets、构建产物、`__pycache__`、`node_modules`。

**references/ — 只读参考资料**

放大部头"只读资料"（Markdown / JSON Schema / SQL DDL / 协议说明），给 Claude 按链接去读，而不是硬塞进正文。

```
references/
├── API_REFERENCE.md      # API 接口完整文档
├── ERROR_CODES.md        # 错误码大全与处理建议
├── GLOSSARY.md           # 术语表/字段语义表
├── SCHEMA.sql            # 数据库 DDL
├── compliance-rules.md   # 合规检查条款
└── config-samples/       # 配置样例
    ├── dev-config.yaml
    └── prod-config.yaml
```

不要放：其实只有一小段规则——直接写在 SKILL.md 正文里更稳定。

**examples/ — 样本输入输出**

放"样本输入输出、gold standard 对照"。要它当且仅当：要给强暗示"照这个格式来"，且样例 ≥ 3 个时拆出去。

```
examples/
├── input-output-1.md     # 样例 1：输入→期望输出
├── input-output-2.json   # 样例 2：JSON 格式样本 IO
├── good-example.txt      # 好的输出示例（gold standard）
├── bad-example.txt       # 需要避免的输出模式（negative example）
└── sample-report.md      # 完整报告样本
```

**templates/ — 产出物骨架**

放"产出物格式契约"：PR 模板、MR 描述、release note 骨架、report markdown layout、JSON 输出 schema 示例等。要它当且仅当：Skill 产出强调一致性，且模板 >10 行。

```
templates/
├── report-template.md     # 报告骨架
├── pr-description.md      # PR 描述模板
├── release-notes.md       # 发布说明模板
├── meeting-minutes.md     # 会议纪要格式
└── output-schema.json     # JSON 输出结构示例
```

**assets/ — 静态资源**

```
assets/
├── icon.png              # Skill 图标
├── header-logo.svg       # 报告模板用到的 Logo
├── sample-fixture.bin    # 样本 fixture 文件
└── boilerplate.py        # 模板代码骨架
```

**schemas/ — 结构校验**

```
schemas/
├── output-validator.json   # 输出 JSON Schema
├── config-schema.yaml      # 配置文件格式定义
└── api-response-spec.yaml  # API 响应结构定义
```

**docs/ — 附加文档**

```
docs/
├── DESIGN.md              # 设计决策记录（ADR）
├── CHANGELOG.md           # Skill 变更日志
├── FAQ.md                 # 常见问题解答
└── ARCHITECTURE.md        # 整体架构说明
```

**速判口诀**：默认只写 SKILL.md。只有当某类内容开始"吃掉 token / 淹没步骤指令 / 需要被执行而非被阅读"时，才给它一个子目录，并在 SKILL.md 里写清楚什么时候去读它、怎么调用它。

### 3. 模板与资源文件的归属架构

**用户**：Obsidian 笔记模板可以放知识库下的 templates 目录吗？还是一定要放 skills 下的 template 文件夹？

**LLM**（元宝）：

**模板完全可以放在 Obsidian Vault 中，不必塞进 skills 下的 template/。** 这是归属权问题：

- `skills/` 下适合放的是 Skill 的"逻辑/指令/可执行部分"（即"怎么做"）
- 笔记模板属于知识库的资产（"内容素材"），天然该跟 Vault 走

正确姿势：**模板归 Vault，Skill 只保留一个指向模板的引用。**

SKILL.md 中推荐的写法：

```
1. 从知识库模板读取内容：
   读取文件：Templates/meeting-note.md
   （用 Read 工具读，不自己从头捏格式）
2. 根据对话把变量填进去
3. 写入目标文件
```

**用户**：是否所有可选文件都可以不放 skills 文件夹下？

**LLM**（元宝）：

真正"必须"的只有 SKILL.md 本身要在 skills 目录中。其他资产：

| 类型 | 推荐位置 | 理由 |
|------|---------|------|
| **templates/** | Vault 的 Templates/ 目录 | Obsidian 可直接管理、链接、版本、预览 |
| **references/** | Vault 的 References/ 目录 | 本身就是知识库资产，可被手动翻阅或他处引用 |
| **examples/** | Vault 的模板/示例区 | 样本本质是"笔记长得什么样"的示范 |
| **scripts/** | 建议留在 skills 旁 | 避免干扰 Obsidian 索引，更好管控执行权限 |

**分界线口诀**：Skill 管"流程与约定"，Vault 管"内容与模板"。

---

## 关键信息点

> 从对话中提取的可复用信息，每条独立可读。

- **概念 /** **渐进式披露（Progressive Disclosure）**：Skills 采用三层加载模型——L0 元数据（name + description，启动即读，~几十 Token）、L1 指令层（SKILL.md 正文，匹配后才加载）、L2 资源层（scripts/references/templates，执行阶段按需读取/调用）。核心思想是"不一次性把所有能力灌进上下文，先知道有什么，再按需加载细节"。
  来源：对话记录 §2

- **概念 /** **SKILL.md 格式规范**：YAML frontmatter 必须包含 `name` + `description`；`description` 极其重要，Claude 靠它做自动匹配触发；正文建议不超过 500 行；Skill 文件夹名使用 kebab-case，文件夹名即 skill ID。
  来源：对话记录 §1

- **方法 /** **"要不要拆"速判表**：触发元数据→frontmatter；步骤指令/规则→SKILL.md 正文；大表/字段词典/API 细节→references/；样本 IO/对照格式→examples/（≥3 个时拆）；产出格式骨架→templates/（>10 行时拆）；可执行代码/CLI→scripts/；结构校验→schemas/。
  来源：对话记录 §2

- **方法 /** **模板归属分界线**：模板放在 Obsidian Vault 的 Templates/ 目录下，SKILL.md 用 vault 相对路径引用。Skill 管"流程与约定"，Vault 管"内容与模板"。scripts/ 建议留在 skills 旁，不混入 vault 避免干扰 Obsidian 索引。
  来源：对话记录 §3-4

- **事实 /** **Claude Code Skills 存放位置**：个人级 `~/.claude/skills/`（跨项目通用，不在 git 中）；项目级 `<项目根>/.claude/skills/`（随仓库提交，团队共享）。`SKILL.md` 是唯一必需文件。
  来源：对话记录 §1

- **方法 /** **scripts/ 的启用判据**：需要有确定性的机械计算/转换/校验（如解析二进制/Office/PDF、批量 rename、schema validate）、需要依赖 pip/npm 可装的库、想锁死复杂实现避免 LLM 自由发挥出错时才用。不要放密钥/secrets/构建产物。安全写法：配合 `allowed-tools: [Bash]` + 只让信任的脚本路径可执行。
  来源：对话记录 §2

- **方法 /** **references/ 的启用判据**：当有字段语义表、错误码表、API 完整参数表、数据字典、合规条文等"大部头只读资料"需要给 Claude 按需阅读时启用。拆出去的唯一理由是让 SKILL.md 从"文档"变回"指令"。
  来源：对话记录 §2

- **方法 /** **examples/ 的启用判据**：当需要强暗示"照这个格式 / 照这个决策"来，且样例超过 2-3 个散在正文会淹没有效指令时启用。样例文件可以是带格式的 `.md` / `.json` / 小 `.csv`。仅 1 个短例子建议内联在正文中。
  来源：对话记录 §2

- **方法 /** **templates/ 的启用判据**：当 Skill 产出强调一致性、机器可读性、团队规范（比自由发挥格式更重要），且模板本身是给人复制填充的格式骨架时启用。格式规则三句话能写完的，直接在正文用代码 fence 写死即可。
  来源：对话记录 §2

- **概念 /** **渐进式披露解决的问题**：上下文窗口有限（99% Skill 内容不在上下文中待命）、Token 成本暴涨（只加载命中的 Skill）、任务干扰/降智（无关 Skill 的规则不在场）、技能越多越难管（可挂几十上百个 Skill，元数据加起来仅一两千 Token）。
  来源：对话记录 §2
