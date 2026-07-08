---
name: weread-book-note
description: >
  Process book notes exported by the WeRead (微信读书) Obsidian plugin
  into structured reading notes. Use this when the user says any of:
  "整理读书笔记", "更新读书笔记", "处理微信读书笔记",
  "处理WeRead笔记", "把我INBOX里的读书笔记整理一下", "我的读书笔记有新的划线了",
  or asks to convert an INBOX note containing book highlights into a
  formatted reading note. Also triggers when a file with
  `doc_type: weread-highlights-reviews` is found in `0 - INBOX/`.
  This skill parses the plugin export format (highlighted text + personal
  comments organized by chapters), creates new reading notes following the
  vault's 读书笔记模板.md, and supports incremental updates — each run
  only appends highlights whose unique reference IDs (`^refID`) are not
  already in the existing reading note.
---

# WeRead 读书笔记处理 Skill

## 概述

这个 Skill 处理微信读书（WeRead）同步插件导出的临时笔记，将其转换为符合知识库规范的读书笔记。

**核心流程：**

1. 读取 `0 - INBOX/` 中的 WeRead 导出笔记（`doc_type: weread-highlights-reviews`）
2. 解析其中的划线（原文摘录）和评论（个人思考），按章节组织
3. 检查读书笔记是否已存在
4. 不存在 → 按模板创建；已存在 → 增量更新（仅追加新内容）
5. 使用划线内容拥有的唯一 `^refID` 做去重

**输出文件路径格式：**

```
3 - KNOWLEDGE/1-Literature/1-Books/{书名}.md
```

---

## 输入格式（WeRead 导出）

WeRead 插件导出的笔记包含 YAML frontmatter + 正文划线评论。

### YAML Frontmatter

```yaml
---
doc_type: weread-highlights-reviews
bookId: "12345678"
title: 书名
author: 作者名
progress: 100%
cover: https://...
readingStatus: "4"
isbn: 9787508686882
---
```

### 正文结构

```markdown
# 高亮划线
（纯划线，无评论的区域——可能为空）

# 读书笔记
## 章节名
### 划线评论
> 📌 划线内容... ^refID
    - 💭 你的评论
    - ⏱ 2025-06-17 11:32:58
```

### 关键字段说明

| 字段 | 说明 |
|------|------|
| `> 📌 ... ^refID` | 划线（原文摘录），`^refID` 是每段划线的唯一标识 |
| `- 💭 ...` | 用户的评论（对应个人思考） |
| `- ⏱ ...` | 评论时间戳 |
| `## 章节名` | 章节标题（作为分类依据） |
| `progress: X%` | 阅读进度，直接映射到读书笔记 frontmatter 的 `progress` |
| `# 高亮划线` | 仅有划线无评论的区域（若 `# 读书笔记` 无内容则从这里补充） |

---

## 快速使用

只需一步，自动处理 INBOX 中所有未处理的 WeRead 导出：

```bash
python scripts/weread_process.py scan
```

脚本会自动：扫描 INBOX → 创建/更新读书笔记 → 删除源文件。
无需手动指定文件名，无中文路径编码问题。

---

## 核心原则

### 模板定义格式，技能填充内容

**文件结构、YAML 字段、正文节标题——所有关乎"怎么写"的规则，均由模板 `[[9 - SYSTEM/Templates/读书笔记模板.md]]` 定义。**

- 写入前读取模板，严格按模板的 YAML 字段、节标题和格式进行填充
- 模板中的 Templater 语法（`<% tp.date.now() %>`、`<% tp.file.title %>`）替换为实际值
- 技能只负责"提取什么"和"映射到哪个字段"，不规定"写成什么样"
- **若模板更新（新增字段、修改结构），技能自动适配，无需修改**

> ⚠️ **绝不自作主张**：YAML 字段中凡模板设为空值（`tags: []`、`links: []`、`aliases: []` 等），技能不得自行填入内容，**原样保留**留给用户填写。

### 字段填充规则

| 来源 | 行为 |
|------|------|
| **从 WeRead 自动抓取** | `title` `author` `progress` `cover` → 每次新建/更新都从源文件同步最新值。`cover` 为 URL 时自动下载到 `6 - ATTACHMENTS/` 并填入本地相对路径 |
| **系统自动生成** | `type` → 固定 `book`（覆盖模板默认）；`created` → 仅新建时设为当天，后续永不修改；`updated` → 当天日期 |
| **手动维护（永不覆盖）** | `tags` `links` `aliases` 及模板中所有空值字段 → 技能不得填充或覆盖，更新时原样保留 |
| **正文占位符** | `> **摘要**` / `## 💡 关键收获` → 新建时生成空占位符，需手动补充 |

---

## 触发方式

**手动触发。** 用户说出以下任一短语时激活本 Skill：

| 中文短语 | 英文/混合短语 |
|----------|---------------|
| "整理读书笔记" | "Process WeRead notes" |
| "更新读书笔记" | "Update my reading notes" |
| "处理微信读书笔记" | "Merge new highlights" |
| "处理 WeRead 导出" | "Process book export" |
| "把我 INBOX 里的读书笔记整理一下" | "Sync my book notes" |
| "我的读书笔记有新的划线了" | - |

---

## 工作流程

### 快速方式（推荐）

运行 `python scripts/weread_process.py scan`，脚本自动完成全部流程（扫描 → 创建/更新 → 删除源文件）。

### 手动方式（分步）

#### Step 1：定位源文件

扫描 `0 - INBOX/` 目录，查找包含 `doc_type: weread-highlights-reviews` 的 `.md` 文件。

```yaml
# 匹配标准：YAML frontmatter 中必须有
doc_type: weread-highlights-reviews
```

**多种情况处理：**

| 情况 | 处理 |
|------|------|
| 找到 0 个匹配文件 | 告知用户未找到 WeRead 导出文件 |
| 找到 1 个匹配文件 | 直接使用该文件 |
| 找到 2+ 个匹配文件 | 列出所有文件，询问用户要处理哪一个 |

**用户也可能直接指定路径**，如 `0 - INBOX/某本书.md`，此时直接使用。

---

### Step 2：解析源文件

读取文件后，依次提取各部分内容。

#### 2.1 提取元数据

从 YAML frontmatter 提取并映射到读书笔记的 frontmatter：

| WeRead 字段 | 读书笔记字段 |
|-------------|-------------|
| `title` | `title` |
| `author` | `author` |
| `progress` | `progress` |
| `cover` | `cover` → 下载到 `6 - ATTACHMENTS/` 后填入本地相对路径 |
| — | `type: book`（固定） |
| — | `created` / `updated` 设为当天日期 |

#### 2.2 解析章节与划线评论

解析正文，支持两种 WeRead 导出格式：

**格式 A（划线评论型）**：解析 `# 读书笔记` 部分
```
## 章节名
### 划线评论
> 📌 划线内容... ^refID
    - 💭 你的评论
    - ⏱ 2025-06-17 11:32:58
```

**格式 B（纯划定型）**：当 `# 读书笔记` 为空时，回退到 `# 高亮划线` 部分
```
### 章节名（可用 ## 或 ###）
> 📌 [划线内容](weread://...)              ← 文本可能包在 markdown 链接中
> ⏱ 2025-06-17 11:32:58 ^refID            ← refID 在下一行
```

**解析逻辑：**

```
highlights = []  # 每个元素: {chapter, text, comment, refID}

# 优先解析格式 A
FOR EACH line AFTER "# 读书笔记":
    IF line matches /^##\s+(.+)/:
        current_chapter = 提取章节名
    IF line matches /^>\s*📌\s*(.+)\s+\^([\w-]+)/:
        text, refID = 提取划线和 refID
        look for next line with /\s*-\s*💭\s*(.+)/ → comment
        highlights.add({chapter, text, comment, refID})

# 若格式 A 无结果，回退格式 B
IF highlights is empty:
    FOR EACH line AFTER "# 高亮划线":
        IF line matches /^(#{2,3})\s+(.+)/:  ← 兼容 ## 和 ###
            current_chapter = 提取章节名
        IF line matches /^>\s*📌\s+(.+)/:
            extract text (handle markdown links [text](url))
            pending = {chapter, text}
        IF line matches /^>\s*⏱\s+.*\^([\w-]+)/:
            pending.refID = 提取 refID  ← refID 在下一行
            highlights.append(pending)
```

#### 2.3 提取章节信息

解析结果中每条记录都带有 `chapter` 字段，但输出时**不按章节分组**，所有摘录按文件中的原始顺序平铺排列。

> 章节信息保留在解析结果中，仅在处理无章节信息的纯划线时用作「📖 全书摘录」默认值。

---

### Step 3：检查目标读书笔记

目标路径：

```
3 - KNOWLEDGE/1-Literature/1-Books/{书名}.md
```

> **注意**：如果书名中包含 `:`、`/`、`*`、`?`、`"`、`<`、`>`、`|` 等 Windows 非法文件名字符，替换为全角字符或空格。

```
书名 = WeRead frontmatter 中的 title
```

- **文件不存在** → 执行 Step 4a（创建新笔记）
- **文件已存在** → 执行 Step 4b（增量更新）

如果目标目录不存在，自动创建。

---

### Step 4a：创建新的读书笔记

#### 4a.1 组装 Frontmatter

1. 读取模板 `[[9 - SYSTEM/Templates/读书笔记模板.md]]` 的 YAML frontmatter 作为基准结构
2. 映射 WeRead 字段覆盖对应值：

   | 模板字段 | 填充规则 |
   |---------|---------|
   | `title` | 从 WeRead 源文件的 `title` 字段获取 |
   | `type` | 固定为 `book`（覆盖模板默认） |
   | `author` | 从 WeRead 源文件的 `author` 字段获取 |
   | `progress` | 从 WeRead 源文件的 `progress` 字段获取 |
   | `cover` | 从 WeRead 源文件的 `cover` 字段获取 URL，下载到 `6 - ATTACHMENTS/` 后填入本地相对路径 |
   | `created` | 设置为当天日期 `YYYY-MM-DD` |
   | `updated` | 设置为当天日期 `YYYY-MM-DD` |

3. **模板中其他空值字段（`tags: []`、`links: []`、`aliases: []` 等）原样保留**，技能不填充、不删除
4. 替换 Templater 语法：`<% tp.date.now("YYYY-MM-DD") %>` → 当天日期

#### 4a.2 组装正文

1. 读取模板 `[[9 - SYSTEM/Templates/读书笔记模板.md]]` 的正文结构作为基准
2. 按模板的节标题和格式填充内容，保留模板中的所有注释和示例格式
3. 替换 Templater 语法：
   - `<% tp.file.title %>` → WeRead 书名
   - `<% tp.date.now("YYYY-MM-DD") %>` → 当天日期
4. 保留模板中示例格式的注释说明（如条目格式、分隔规则等），不删除
5. 将 Step 2 解析出的所有摘录，按模板中 `## 📝 摘录与思考` 部分的条目格式生成

#### 4a.3 按模板格式生成摘录

将 Step 2 解析出的所有摘录，按 `9 - SYSTEM/Templates/读书笔记模板.md` 中 `## 📝 摘录与思考` 部分的格式与示例生成。输出内容需与模板中的条目格式、分隔规则保持一致。

#### 4a.4 写入文件

路径：`3 - KNOWLEDGE/1-Literature/1-Books/{书名}.md`

使用 UTF-8 编码写入。

---

### Step 4b：增量更新已有读书笔记

#### 4b.1 提取已有 refID

读取已有读书笔记全文，用正则提取所有 `<!-- ^refID -->`：

```python
existing_refs = set()
existing_pat = re.compile(r'<!--\s*\^([\w-]+)\s*-->')
for match in existing_pat.finditer(existing_content):
    existing_refs.add(match.group(1))
```

#### 4b.2 过滤出新条目

只保留 Step 2 解析结果中 refID 不在 `existing_refs` 中的条目：

```python
new_highlights = [h for h in all_highlights if h['refID'] not in existing_refs]
```

如果 `new_highlights` 为空，跳到 Step 5 报告无变化。

#### 4b.3 追加新条目

新条目直接追加到 `## 📝 摘录与思考` 末尾的已有列表之后：

- 定位 `## 📝 摘录与思考` 下方已有列表的结束位置
- 在末尾追加新列表项（保持 `- **原文摘录**：` / `  **个人思考**：` 格式）
- 无需章节标题，所有条目平铺排列

#### 4b.4 更新 Frontmatter

更新已有笔记的 YAML frontmatter，**只更新 WeRead 自动抓取的字段**：

| 更新 | 不更新 |
|------|--------|
| `progress` → 从 WeRead 获取最新值 | `title` `author`（通常不变，若不匹配则同步） |
| `cover` → 从 WeRead 同步封面（下载到本地） | **模板中所有其他字段**（`tags` `links` `aliases` 及未来新增字段）→ 原样保留，不改动用户设置 |
| `updated` → 当天日期 | |
| 正文中新增摘录 | 已有正文内容不变 |

---

### Step 5 — 写入后自检

确认：
1. ✅ 没有残留 Templater 占位符（`<% ... %>`）
2. ✅ `tags` `links` `aliases` `cover` 等空值字段未被填充，原样保留
3. ✅ 摘录格式正确：条目格式、`---` 分隔规则、最后一条无多余分隔线
4. ✅ `created` / `updated` 已填充实际日期
5. ✅ 封面图片已成功下载到 `6 - ATTACHMENTS/`（`cover` 为 URL 时需确认已转本地路径）
6. ✅ 增量更新场景：新摘录的 refID 不与已有 refID 重复

自检发现问题 → 修正后再进入下一步。
自检全部通过 → 继续。

---

### Step 6：结果报告

根据操作类型向用户报告。

**新建场景：**

> ✅ 已创建读书笔记 [[书名]]
> - 共收录 **N** 条划线评论，分布在 **M** 个章节
> - 阅读进度：XX%

**更新场景：**

> ✅ 已更新读书笔记 [[书名]]
> - 本次新增 **N** 条划线评论（新增章节：XX）
> - 当前共 **M** 条划线评论
> - 阅读进度：XX%

**无变化场景：**

> ℹ️ 没有发现新的划线内容，读书笔记已是最新状态。

**如果文件不存在于 INBOX：**

> ❌ 在 `0 - INBOX/` 中没有找到 WeRead 导出的笔记文件。请先在微信读书中用 WeRead 同步插件导出笔记。

---

### Step 7：清理源文件

处理成功并确认无误后，**删除 INBOX 中的临时笔记文件**，保持 INBOX 整洁。

使用 `scan` 命令可自动处理删除，无需额外参数（推荐，无中文路径问题）：

```bash
python scripts/weread_process.py scan
```

使用 `create` / `update` 时附加 `--delete-source` 参数（注意：Windows 下中文路径可能编码异常，推荐用 `scan`）：

```bash
# 新建 + 自动删除源文件
python weread_process.py create --delete-source "0 - INBOX/书名.md" "3 - KNOWLEDGE/1-Literature/1-Books/书名.md"

# 更新 + 自动删除源文件
python weread_process.py update --delete-source "0 - INBOX/书名.md" "..." "..."
```

或手动删除：

```bash
rm "0 - INBOX/{文件名}.md"
```

> ⚠️ 处理完成后即删除源文件（即使无新增内容也清理，避免 INBOX 堆积）。
> 只有在处理失败（如解析出错）时才保留源文件。



---

## 边界情况处理

| 情况 | 处理方式 |
|------|----------|
| **划线无对应评论（- 💭）** | 个人思考显示 `—` |
| **同一条 refID 已存在** | 跳过，不重复添加 |
| **INBOX 中有多本书的 WeRead 导出** | 询问用户要处理哪一本 |
| **目标文件夹不存在** | 自动创建 `3 - KNOWLEDGE/1-Literature/1-Books/` |
| **含非法文件名字符** | `: / * ? " < > \|` → 替换为全角 `：／＊？＂＜＞｜` 或空格 |
| **`^refID` 格式后续变化** | 匹配模式：`^` 后跟字母、数字、连字符、下划线 |
| **已有读书笔记使用旧格式（表格）** | 保留旧格式，按旧格式追加新行；新旧不混用 |
| **WeRead 导出为空（无划线无评论）** | 告知用户后保留源文件，不删除 |
| **中文路径编码异常** | Windows + Bash 下中文路径传参可能截乱。用 `scan` 命令绕过（内部用 Python glob 处理） |
| **处理成功** | 自动删除 INBOX 中的源文件 |
| **无新内容** | 同样删除源文件，避免 INBOX 堆积 |
| **处理失败** | 保留源文件，不删除 |

---

## 推荐工作流

```
阅读微信读书 → 划线 + 写想法
        ↓
用 WeRead 同步插件导出笔记（存入 0 - INBOX/）
        ↓
对 Claude 说「整理我的读书笔记」
        ↓
处理完成 → 临时笔记自动删除
        ↓
继续阅读 → 再次划线 → 再次导出
        ↓
对 Claude 说「更新读书笔记」
        ↓
处理完成 → 临时笔记自动删除
        ↓
（循环…）
```

每次导入新划线后触发一次，笔记自动累积，无需手动复制粘贴。

---

## 参考资源

| 资源 | 路径 |
|------|------|
| 模板文件 | `9 - SYSTEM/Templates/读书笔记模板.md` |
| 输出目录 | `3 - KNOWLEDGE/1-Literature/1-Books/` |
| 辅助脚本 | `scripts/weread_process.py`（可选，解析与合并） |
| 知识库规范 | `9 - SYSTEM/知识库操作规范.md` |

---

## 使用示例

### 示例 1：首次创建

**用户：**
> 帮我整理一下微信读书导出的笔记

**Claude 操作：**
1. 扫描 INBOX，找到 WeRead 导出文件
2. 解析摘录，检查目标路径 → 不存在，创建新笔记
3. 自动删除 INBOX 源文件
4. 报告结果

### 示例 2：增量更新

**用户（几天后）：**
> 之前那本书又读了一些，帮我更新一下读书笔记

**Claude 操作：**
1. 扫描 INBOX，找到更新后的导出文件
2. 解析新摘录，与已有笔记对比 → 仅追加新内容
3. 自动删除 INBOX 源文件
4. 报告「新增 X 条，当前共 Y 条」
