#!/usr/bin/env python3
"""
算法之美（WeRead）笔记处理脚本 — 解析导出文件、创建/更新读书笔记。

用法:
  # 解析 WeRead 导出文件，输出 JSON
  python weread_process.py parse <inbox_path>

  # 创建新的读书笔记
  python weread_process.py create <inbox_path> <output_path>

  # 增量更新已有的读书笔记
  python weread_process.py update <inbox_path> <existing_path> <output_path>

返回值:
  0 - 成功（有改动）
  1 - 成功（无改动，已是最新）
  2 - 出错

输出说明:
  - parse 模式: 向 stdout 输出 JSON，包含 book_metadata 和 highlights 列表
  - create 模式: 将生成的读书笔记写入 <output_path>，向 stderr 输出 "CREATED"
  - update 模式: 将合并后的读书笔记写入 <output_path>，向 stderr 输出 "UPDATED" 或 "NO_CHANGE"
"""

import json
import re
import sys
import os
import urllib.request
from urllib.parse import urlparse
from collections import defaultdict
from datetime import date


# ── 正则表达式 ──────────────────────────────────────────────────────────

# YAML frontmatter
FM_PATTERN = re.compile(r'^---\n(.*?)\n---', re.DOTALL)

# 章节标题：## 章节名（划线评论中用 ##）
CHAPTER_PAT = re.compile(r'^##\s+(.+)')

# 纯划线区域的章节头：可用 ## 或 ###（因为 export 版本不同）
PURE_HL_CHAPTER_PAT = re.compile(r'^(#{2,3})\s+(.+)')

# 划线 + refID：> 📌 ... ^refID
HIGHLIGHT_PAT = re.compile(r'^>\s*📌\s*(.*?)\s+\^([\w-]+)\s*$')

# 划线（纯划线格式）：> 📌 [text](url)
HIGHLIGHT_LINE_PAT = re.compile(r'^>\s*📌\s+(.+)$')

# 提取 markdown 链接中的文本：[text](url) → text
MD_LINK_TEXT_PAT = re.compile(r'^\[(.+)\]\(.+\)$')

# 时间戳 + refID：> ⏱ ... ^refID
TIMESTAMP_REF_PAT = re.compile(r'^>\s*⏱\s+.*\s+\^([\w-]+)$')

# 评论：- 💭 ...
COMMENT_PAT = re.compile(r'^\s*-\s*💭\s*(.*)')

# 时间戳：- ⏱ ...
TIMESTAMP_PAT = re.compile(r'^\s*-\s*⏱\s*(.*)')

# 已存在的 refID（兼容两种格式：HTML 注释 <!-- ^refID --> 与内联 ^refID）
EXISTING_REF_PAT = re.compile(r'<!--\s*\^([\w-]+)\s*-->|\^([\w-]+)')

# 非法文件名字符（Windows）
INVALID_FILENAME_CHARS = r'[:*?"<>|/\\]'


# ── 工具函数 ────────────────────────────────────────────────────────────

def parse_frontmatter(content: str) -> dict:
    """解析 YAML frontmatter 为字典。"""
    match = FM_PATTERN.match(content)
    if not match:
        raise ValueError("未找到有效的 YAML frontmatter")

    fm_text = match.group(1)
    fm = {}
    for line in fm_text.split('\n'):
        line = line.strip()
        if ':' in line and not line.startswith('#'):
            key, _, value = line.partition(':')
            fm[key.strip()] = value.strip().strip('"').strip("'")
    return fm


def safe_filename(name: str) -> str:
    """替换非法文件名字符为全角等效。"""
    char_map = {
        ':': '：', '*': '＊', '?': '？', '"': '＂',
        '<': '＜', '>': '＞', '|': '｜', '/': '／', '\\': '＼',
    }
    for illegal, replacement in char_map.items():
        name = name.replace(illegal, replacement)
    return name.strip()


def extract_refs_from_note(content: str) -> set:
    """从已有的读书笔记中提取所有 refID。"""
    refs = set()
    for match in EXISTING_REF_PAT.finditer(content):
        refs.add(match.group(1) or match.group(2))
    return refs


def today_str() -> str:
    """返回当天日期字符串 YYYY-MM-DD。"""
    return date.today().isoformat()


def safe_remove(path: str):
    """安全删除文件，兼容中文路径的 Windows 问题。"""
    if not path or not os.path.exists(path):
        return
    try:
        os.remove(path)
    except Exception:
        # 如果直接删除失败（如中文路径编码问题），尝试按文件名查找
        import glob as _glob
        basename = os.path.basename(path)
        candidates = _glob.glob(os.path.join(os.path.dirname(path) or '.', basename))
        candidates += _glob.glob(os.path.join(os.path.dirname(path) or '.', '*'))
        for c in candidates:
            if os.path.exists(c) and os.path.isfile(c):
                try:
                    os.remove(c)
                    return
                except Exception:
                    pass


# ── 封面图片下载 ──────────────────────────────────────────────────────────

# 支持的图片扩展名
COVER_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}


def download_cover(cover_url: str, book_title: str) -> str:
    """
    将封面图片下载到 6 - ATTACHMENTS/，返回本地相对路径。

    如果文件已存在则跳过下载（幂等）。
    如果下载失败（网络错误、URL 无效等），返回原始 URL 作为兜底。
    """
    if not cover_url or not cover_url.startswith('http'):
        return cover_url  # 非 URL 字段原样返回（可能已经是本地路径）

    # 从 URL 提取扩展名
    parsed = urlparse(cover_url)
    ext = os.path.splitext(parsed.path)[1].lower()
    if ext not in COVER_EXTENSIONS:
        ext = '.jpg'  # 默认

    # 构建安全文件名
    safe_title = safe_filename(book_title).strip().replace(' ', '_')
    if not safe_title:
        safe_title = 'unknown'
    if len(safe_title) > 100:
        safe_title = safe_title[:100]

    atta_dir = '6 - ATTACHMENTS'
    os.makedirs(atta_dir, exist_ok=True)

    local_path = os.path.join(atta_dir, f'cover_{safe_title}{ext}')

    # 已下载则跳过
    if os.path.exists(local_path):
        return local_path.replace('\\', '/')

    try:
        urllib.request.urlretrieve(cover_url, local_path)
        return local_path.replace('\\', '/')
    except Exception:
        # 下载失败，用原始 URL 兜底
        return cover_url


# ── 解析 WeRead 导出文件 ──────────────────────────────────────────────

def parse_weread_note(filepath: str) -> dict:
    """
    解析 WeRead 导出笔记文件。

    返回:
        {
            "book": {
                "title": str,
                "author": str,
                "progress": str,
                "isbn": str,
                "bookId": str,
                "cover": str
            },
            "highlights": [
                {
                    "chapter": str,
                    "text": str,
                    "comment": str or None,
                    "refID": str,
                    "timestamp": str or None
                },
                ...
            ]
        }
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. 解析 frontmatter
    fm = parse_frontmatter(content)
    book = {
        'title': fm.get('title', '未知书名'),
        'author': fm.get('author', '未知作者'),
        'progress': fm.get('progress', ''),
        'isbn': fm.get('isbn', ''),
        'bookId': fm.get('bookId', ''),
        'cover': fm.get('cover', ''),
    }

    # 2. 找到正文起始位置（移除 frontmatter）
    fm_match = FM_PATTERN.match(content)
    body = content[fm_match.end():]

    # 3. 检查各部分是否存在
    has_reading_notes = '# 读书笔记' in body
    has_highlights = '# 高亮划线' in body

    highlights = []

    # 4. 主解析：从 # 读书笔记 中提取
    notes_section = ''
    if has_reading_notes:
        notes_start = body.index('# 读书笔记')
        notes_end = body.index('# 本书评论') if '# 本书评论' in body[notes_start:] else len(body)
        notes_section = body[notes_start:notes_end]

    if notes_section.strip():
        highlights = parse_notes_section(notes_section)

    # 5. 同时从 # 高亮划线 中提取纯划线（与 # 读书笔记 合并，不互相排斥）
    if has_highlights:
        hl_start = body.index('# 高亮划线')
        hl_end = body.index('# 读书笔记') if has_reading_notes else len(body)
        hl_section = body[hl_start:hl_end]
        pure_highlights = parse_pure_highlights(hl_section)
        # 用 refID 去重（读书笔记区已收录的跳过）
        seen_refs = {h['refID'] for h in highlights if h.get('refID')}
        for h in pure_highlights:
            if h.get('refID') and h['refID'] not in seen_refs:
                highlights.append(h)

    return {'book': book, 'highlights': highlights}


def parse_notes_section(section: str) -> list:
    """解析 # 读书笔记 部分，提取章节、划线、评论。"""
    highlights = []
    current_chapter = None
    lines = section.split('\n')
    i = 0

    while i < len(lines):
        line = lines[i]

        # 检测章节标题
        ch_match = CHAPTER_PAT.match(line)
        if ch_match:
            # 跳过 "读书笔记" 这个大标题本身
            chapter_name = ch_match.group(1).strip()
            if chapter_name != '读书笔记':
                current_chapter = chapter_name
            i += 1
            continue

        # 检测划线 + refID
        hl_match = HIGHLIGHT_PAT.match(line)
        if hl_match and current_chapter:
            raw_text = hl_match.group(1).strip()
            # 如果内容在 markdown 链接中，提取显示文本
            md_match = MD_LINK_TEXT_PAT.match(raw_text)
            text = md_match.group(1).strip() if md_match else raw_text
            ref_id = hl_match.group(2).strip()
            comment = None
            timestamp = None

            # 查看后续行（缩进内容）提取评论和时间戳
            j = i + 1
            while j < len(lines) and (lines[j].startswith(' ') or lines[j].startswith('\t') or lines[j].strip() == ''):
                stripped = lines[j].strip()
                if not stripped:
                    j += 1
                    continue
                cm_match = COMMENT_PAT.match(lines[j])
                if cm_match:
                    comment = cm_match.group(1).strip()
                ts_match = TIMESTAMP_PAT.match(lines[j])
                if ts_match:
                    timestamp = ts_match.group(1).strip()
                j += 1

            highlights.append({
                'chapter': current_chapter,
                'text': text,
                'comment': comment,
                'refID': ref_id,
                'timestamp': timestamp,
            })

            i = j
            continue

        i += 1

    return highlights


def parse_pure_highlights(section: str) -> list:
    """从 # 高亮划线 部分解析纯划线（无评论）。

    支持两种格式：
    格式 A: > 📌 text ^refID                          （refID 同行）
    格式 B: > 📌 [text](url)                          （refID 在下一行 > ⏱）
            > ⏱ timestamp ^refID
    """
    highlights = []
    lines = section.split('\n')
    current_chapter = None
    pending_highlight = None  # 暂存格式 B 的划线，等下一行的 refID

    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue

        # 检测章节头（## 或 ###）
        ch_match = PURE_HL_CHAPTER_PAT.match(stripped)
        if ch_match:
            chapter_name = ch_match.group(2).strip()
            if chapter_name not in ('高亮划线', '划线评论'):
                current_chapter = chapter_name
            continue

        # 尝试格式 A：> 📌 text ^refID
        hl_a = HIGHLIGHT_PAT.match(stripped)
        if hl_a:
            raw_text = hl_a.group(1).strip()
            # 如果内容在 markdown 链接中，提取显示文本
            md_match = MD_LINK_TEXT_PAT.match(raw_text)
            text = md_match.group(1).strip() if md_match else raw_text
            highlights.append({
                'chapter': current_chapter or '📖 全书摘录',
                'text': text,
                'refID': hl_a.group(2).strip(),
                'comment': None,
                'timestamp': None,
            })
            continue

        # 检测 - 💭 评论（可能跟在格式 A 划线之后，补充到上一条）
        cm_match = COMMENT_PAT.match(stripped)
        if cm_match and highlights:
            raw_comment = cm_match.group(1).strip()
            # 去掉末尾的时间戳（- ⏱ YYYY-MM-DD HH:MM:SS）
            raw_comment = re.sub(r'\s*-\s*⏱\s*.*$', '', raw_comment).strip()
            highlights[-1]['comment'] = raw_comment
            continue

        # 尝试格式 B：> 📌 [text](url) 或 > 📌 text（无 refID 同行）
        hl_b = HIGHLIGHT_LINE_PAT.match(stripped)
        if hl_b:
            raw_text = hl_b.group(1).strip()
            # 如果内容在 markdown 链接中，提取显示文本
            md_match = MD_LINK_TEXT_PAT.match(raw_text)
            text = md_match.group(1).strip() if md_match else raw_text
            pending_highlight = {
                'chapter': current_chapter or '📖 全书摘录',
                'text': text,
                'refID': None,
                'comment': None,
                'timestamp': None,
            }
            continue

        # 检查是否为 > ⏱ ... ^refID（格式 B 的 refID 行）
        ts_match = TIMESTAMP_REF_PAT.match(stripped)
        if ts_match and pending_highlight:
            pending_highlight['refID'] = ts_match.group(1).strip()
            highlights.append(pending_highlight)
            pending_highlight = None
            continue

        # 不匹配任何已知模式，清除暂存
        pending_highlight = None

    return highlights


# ── 模板相关 ─────────────────────────────────────────────────────────────

TEMPLATE_PATH = '9 - SYSTEM/Templates/读书笔记模板.md'


def _read_template_body() -> str:
    """读取模板文件正文（去除 frontmatter）。读取失败时返回空字符串。"""
    try:
        with open(TEMPLATE_PATH, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        return ''

    fm_match = FM_PATTERN.match(content)
    if not fm_match:
        return ''
    return content[fm_match.end():]


def load_template_prefix(book: dict) -> str:
    """
    读取模板文件，提取 `` ## 📝 摘录与思考 `` 之前的所有内容（前缀），
    处理 Templater 标签后返回。

    返回处理后的 Markdown 字符串。读取失败或找不到目标区域时返回空字符串。
    """
    body = _read_template_body()

    notes_idx = body.find('## 📝 摘录与思考')
    if notes_idx < 0:
        return ''

    prefix = body[:notes_idx]

    # 处理 Templater 标签
    prefix = prefix.replace('<% tp.file.title %>', book['title'])
    prefix = re.sub(r"<%\s*tp\.date\.now\(.*?\)\s*%>", today_str(), prefix)
    # 清理其他未处理的 Templater 标签（保留可见文本）
    prefix = re.sub(r'<%.*?%>', '', prefix)

    return prefix.strip()


def load_template_suffix() -> str:
    """
    读取模板文件，提取「## 📝 摘录与思考」之后的后续章节
    （从第一个后续 ## 标题起至文件末尾，如 ## 📌 行动指南），
    处理 Templater 标签后返回。

    返回处理后的 Markdown 字符串。读取失败或没有后续章节时返回空字符串。
    """
    body = _read_template_body()

    notes_idx = body.find('## 📝 摘录与思考')
    if notes_idx < 0:
        return ''

    # 在「摘录与思考」之后找第一个 ## 标题（即模板的后续章节）
    after_notes = body[notes_idx + len('## 📝 摘录与思考'):]
    heading = re.search(r'^##\s+.*$', after_notes, re.MULTILINE)
    if not heading:
        return ''
    suffix = after_notes[heading.start():]

    # 处理 Templater 标签
    suffix = re.sub(r"<%\s*tp\.date\.now\(.*?\)\s*%>", today_str(), suffix)
    # 清理其他未处理的 Templater 标签（保留可见文本）
    suffix = re.sub(r'<%.*?%>', '', suffix)

    return suffix.strip()

def generate_book_note(parsed: dict, existing_refs: set = None) -> tuple:
    """
    生成读书笔记 Markdown 内容。

    参数:
        parsed: parse_weread_note() 的返回值
        existing_refs: 已存在的 refID 集合（增量更新时传入）

    返回:
        (new_content, stats)
        new_content: str — 完整的 Markdown 内容
        stats: dict — 统计数据
    """
    if existing_refs is None:
        existing_refs = set()

    book = parsed['book']
    all_highlights = parsed['highlights']

    # 下载封面图片到本地
    if book.get('cover'):
        book['cover'] = download_cover(book['cover'], book['title'])

    # 过滤出新条目
    new_highlights = [h for h in all_highlights if h['refID'] not in existing_refs]
    is_update = len(existing_refs) > 0

    stats = {
        'total_in_source': len(all_highlights),
        'existing_count': len(existing_refs),
        'new_count': len(new_highlights),
        'chapters_new': set(),
        'action': 'no_change',
    }

    if not new_highlights and is_update:
        return None, stats  # 无新内容

    if not new_highlights and not is_update:
        # 首次创建但源文件为空
        return None, stats

    stats['action'] = 'update' if is_update else 'create'

    # ── 组装内容 ──
    lines = []

    # Frontmatter
    lines.append('---')
    lines.append(f'title: {book["title"]}')
    lines.append('type: book')
    lines.append(f'author: {book["author"]}')
    lines.append(f'cover: {book["cover"]}')
    lines.append(f'progress: {book["progress"]}')
    lines.append(f'created: {today_str() if not is_update else "{{EXISTING_CREATED}}"}')
    lines.append(f'updated: {today_str()}')
    lines.append('tags: []')
    lines.append('links: []')
    lines.append('aliases: []')
    lines.append('---')
    lines.append('')

    # ── 正文前缀 ──
    if is_update:
        # 更新场景：只生成摘录列表（merge 会提取新条目追加到已有笔记）
        lines.append(f'# {book["title"]}')
        lines.append('')
        lines.append('> **摘要**：<!-- 待补充 -->')
        lines.append('')
    else:
        # 创建场景：从模板读取前缀（关键收获等自定义章节随模板自动生效）
        template_prefix = load_template_prefix(book)
        if template_prefix:
            lines.append(template_prefix)
            lines.append('')
        else:
            # 模板读取失败时的备用
            lines.append(f'# {book["title"]}')
            lines.append('')
            lines.append('> **摘要**：<!-- 待补充 -->')
            lines.append('')

    # 摘录与思考（列表格式，无章节信息）
    lines.append('## 📝 摘录与思考')
    lines.append('')

    items = new_highlights if is_update else all_highlights
    for i, h in enumerate(items):
        text = h['text'].replace('\n', ' ')
        comment = h['comment'] if h['comment'] else '—'
        lines.append(f'- **原文摘录**：{text} <!-- ^{h["refID"]} -->')
        lines.append(f'  **个人思考**：{comment}')
        if i < len(items) - 1:  # 条目之间用 --- 分隔
            lines.append('')
            lines.append('---')
            lines.append('')

    # 创建场景：追加模板中「摘录与思考」之后的后续章节（如 ## 📌 行动指南）
    if not is_update:
        template_suffix = load_template_suffix()
        if template_suffix:
            lines.append(template_suffix)

    content = '\n'.join(lines)
    stats['chapters_new'] = len(new_highlights)

    return content, stats


def merge_with_existing(new_content: str, existing_content: str) -> str:
    """
    将新生成的列表项追加到已有的读书笔记中。

    策略:
    1. 保持已有笔记的 frontmatter（只更新 updated、progress 和 cover）
    2. 提取新内容中的列表项（`- **原文摘录**：` / `**个人思考**：`），追加到已有列表末尾
    """
    new_lines = new_content.split('\n')
    existing_lines = existing_content.split('\n')

    # 查找已有笔记中摘录与思考的位置
    target_section_idx = None
    for i, line in enumerate(existing_lines):
        if line.strip() == '## 📝 摘录与思考':
            target_section_idx = i
            break

    if target_section_idx is None:
        return new_content

    # 从新内容中提取 frontmatter 的 updated、progress 和 cover
    new_updated = today_str()
    new_progress = ''
    new_cover = ''
    for line in new_lines:
        if line.startswith('progress: '):
            new_progress = line[len('progress: '):]
        if line.startswith('cover: '):
            new_cover = line[len('cover: '):]
        if new_progress and new_cover:
            break

    # 从新内容中提取摘录列表（从 `## 📝 摘录与思考` 之后到末尾的所有内容）
    new_list_items = []
    capture = False
    for line in new_lines:
        if line.strip() == '## 📝 摘录与思考':
            capture = True
            continue
        if capture:
            new_list_items.append(line)

    if not new_list_items:
        return existing_content  # 无新内容，返回原样

    # 更新已有 frontmatter
    result_lines = []
    in_fm = False
    fm_done = False
    for line in existing_lines:
        if line.strip() == '---' and not fm_done:
            if not in_fm:
                in_fm = True
                result_lines.append(line)
            else:
                in_fm = False
                fm_done = True
                result_lines.append('updated: ' + new_updated)
                if new_progress:
                    pass  # progress 行会在下面的循环中处理
                continue
        elif in_fm:
            if line.startswith('updated:'):
                continue  # 已写入
            if line.startswith('progress:') and new_progress:
                result_lines.append('progress: ' + new_progress)
                continue
            if line.startswith('cover:') and new_cover:
                result_lines.append('cover: ' + new_cover)
                continue
            result_lines.append(line)
        else:
            result_lines.append(line)

    # 找到已有列表的末尾（## 📝 摘录与思考 之后，遇到下一个 ## 或文件末尾）
    list_end = target_section_idx + 1
    for i in range(target_section_idx + 1, len(result_lines)):
        if i > target_section_idx + 1 and result_lines[i].startswith('## '):
            break
        list_end = i

    # 检查已有条目，若有则在旧条目和新条目之间加 --- 分隔
    has_existing_entries = any(
        line.strip().startswith('- **原文摘录**：')
        for line in result_lines[target_section_idx:list_end + 1]
    )
    if has_existing_entries:
        # 去掉新内容开头的空行（如果有）
        while new_list_items and new_list_items[0].strip() == '':
            new_list_items.pop(0)
        new_list_items = ['', '---', ''] + new_list_items

    # 在列表末尾插入新列表项
    insert_pos = list_end + 1
    if insert_pos < len(result_lines) and result_lines[insert_pos - 1] != '':
        result_lines.insert(insert_pos, '')
        insert_pos += 1
    for item in new_list_items:
        result_lines.insert(insert_pos, item)
        insert_pos += 1
    result_lines.insert(insert_pos, '')

    return '\n'.join(result_lines)


# ── CLI ─────────────────────────────────────────────────────────────────

def cmd_parse(args):
    """解析 WeRead 导出文件并输出 JSON。"""
    if len(args) < 1:
        print("用法: weread_process.py parse <inbox_path>", file=sys.stderr)
        sys.exit(2)

    filepath = args[0]
    if not os.path.exists(filepath):
        print(f"错误: 文件不存在 — {filepath}", file=sys.stderr)
        sys.exit(2)

    try:
        parsed = parse_weread_note(filepath)
        print(json.dumps(parsed, ensure_ascii=False, indent=2))
        sys.exit(0)
    except Exception as e:
        print(f"解析错误: {e}", file=sys.stderr)
        sys.exit(2)


def cmd_create(args):
    """创建新的读书笔记。支持 --delete-source。"""
    delete_source = '--delete-source' in args
    args = [a for a in args if a != '--delete-source']

    if len(args) < 2:
        print("用法: weread_process.py create [--delete-source] <inbox_path> <output_path>", file=sys.stderr)
        sys.exit(2)

    inbox_path, output_path = args[0], args[1]

    if not os.path.exists(inbox_path):
        print(f"错误: 文件不存在 — {inbox_path}", file=sys.stderr)
        sys.exit(2)

    try:
        parsed = parse_weread_note(inbox_path)
        content, stats = generate_book_note(parsed)

        if content is None:
            print("源文件中没有找到划线内容。", file=sys.stderr)
            sys.exit(1)

        # 确保输出目录存在
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)

        # 创建成功后删除源文件
        if delete_source:
            safe_remove(inbox_path)

        print(f"CREATED|{stats['new_count']}")
        sys.exit(0)
    except Exception as e:
        print(f"创建失败: {e}", file=sys.stderr)
        sys.exit(2)


def cmd_update(args):
    """增量更新已有的读书笔记。支持 --delete-source。"""
    delete_source = '--delete-source' in args
    args = [a for a in args if a != '--delete-source']

    if len(args) < 3:
        print("用法: weread_process.py update [--delete-source] <inbox_path> <existing_path> <output_path>", file=sys.stderr)
        sys.exit(2)

    inbox_path, existing_path, output_path = args[0], args[1], args[2]

    if not os.path.exists(inbox_path):
        print(f"错误: 文件不存在 — {inbox_path}", file=sys.stderr)
        sys.exit(2)

    if not os.path.exists(existing_path):
        print(f"错误: 已有笔记不存在 — {existing_path}", file=sys.stderr)
        sys.exit(2)

    try:
        # 解析源文件
        parsed = parse_weread_note(inbox_path)

        # 读取已有笔记并提取 refID
        with open(existing_path, 'r', encoding='utf-8') as f:
            existing_content = f.read()
        existing_refs = extract_refs_from_note(existing_content)

        # 生成新内容（仅新条目）
        new_content, stats = generate_book_note(parsed, existing_refs)

        if new_content is None and stats['action'] == 'no_change':
            print("NO_CHANGE")
            sys.exit(1)  # 无变化，不删除源文件

        if new_content is None:
            print("源文件中没有找到划线内容。", file=sys.stderr)
            sys.exit(1)

        # 合并到已有笔记
        merged = merge_with_existing(new_content, existing_content)

        # 写入输出
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(merged)

        # 更新成功后删除源文件
        if delete_source:
            os.remove(inbox_path)

        print(f"UPDATED|{stats['new_count']}")
        sys.exit(0)
    except Exception as e:
        print(f"更新失败: {e}", file=sys.stderr)
        sys.exit(2)


def cmd_scan(args):
    """扫描 INBOX，自动处理所有 WeRead 导出笔记（避免中文路径传参问题）。"""
    import glob as _glob
    inbox_dir = '0 - INBOX'
    book_dir = '3 - KNOWLEDGE/1-Literature/1-Books'
    results = []

    for fpath in _glob.glob(os.path.join(inbox_dir, '*.md')):
        with open(fpath, 'r', encoding='utf-8') as f:
            if 'doc_type: weread-highlights-reviews' not in f.read(300):
                continue

        fname = os.path.basename(fpath)
        try:
            parsed = parse_weread_note(fpath)
            title = parsed['book']['title']
            out_path = os.path.join(book_dir, f'{title}.md')

            if os.path.exists(out_path):
                with open(out_path, 'r', encoding='utf-8') as f:
                    existing = f.read()
                existing_refs = extract_refs_from_note(existing)
                new_content, stats = generate_book_note(parsed, existing_refs)
                if new_content is None:
                    safe_remove(fpath)
                    results.append((fname, '无新内容，已清理'))
                else:
                    merged = merge_with_existing(new_content, existing)
                    os.makedirs(book_dir, exist_ok=True)
                    with open(out_path, 'w', encoding='utf-8') as f:
                        f.write(merged)
                    safe_remove(fpath)
                    results.append((fname, f'已更新，新增 {stats["new_count"]} 条'))
            else:
                content, stats = generate_book_note(parsed)
                os.makedirs(book_dir, exist_ok=True)
                with open(out_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                safe_remove(fpath)
                results.append((fname, f'已创建，共 {stats["new_count"]} 条'))
        except Exception as e:
            results.append((fname, f'失败: {e}'))

    if not results:
        print("INBOX 中没有找到 WeRead 导出的笔记。")
    else:
        print(f"处理了 {len(results)} 个文件：")
        for name, status in results:
            print(f"  {name} → {status}")


def main():
    if len(sys.argv) < 2:
        print("用法: weread_process.py <parse|create|update> [参数...]", file=sys.stderr)
        sys.exit(2)

    command = sys.argv[1]
    cmd_args = sys.argv[2:]

    if command == 'parse':
        cmd_parse(cmd_args)
    elif command == 'create':
        cmd_create(cmd_args)
    elif command == 'update':
        cmd_update(cmd_args)
    elif command == 'scan':
        cmd_scan(cmd_args)
    else:
        print(f"未知命令: {command}", file=sys.stderr)
        print("可用命令: parse, create, update, scan", file=sys.stderr)
        sys.exit(2)


if __name__ == '__main__':
    main()
