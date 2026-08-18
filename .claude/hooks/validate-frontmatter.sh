#!/bin/bash
# Frontmatter 字段校验 — 动态对照模板
# PreToolUse hook on Write 自动调用
# 比对新建笔记的 frontmatter 字段与对应模板是否一致（只提醒，不阻塞）

set -euo pipefail

file_path=$(jq -r '.tool_input.file_path // ""' 2>/dev/null)
content=$(jq -r '.tool_input.content // ""' 2>/dev/null)

# ── 前置过滤 ──────────────────────────────────────
[ -z "$file_path" ] && exit 0
[ -z "$content" ] && exit 0

# 只检查 vault 内的 .md 文件
echo "$file_path" | grep -q '\.md$' || exit 0

# 跳过系统目录
echo "$file_path" | grep -qvE '^(9 - SYSTEM|\.claude|\.obsidian)/' || exit 0

# 跳过已存在的文件（用 awk 模拟 file_path 转换，仅对创建场景校验）
# 注意：Write 天然会覆盖旧文件，但覆盖时字段可能已合法，无需校验。
# 此处仅校验 frontmatter 存在时，不做"新建 vs 覆盖"的判断。

# ── 提取 frontmatter ──────────────────────────────
fm=$(echo "$content" | tr -d '\r' | sed -n '/^---$/,/^---$/p' | sed '1d;$d')
[ -z "$fm" ] && exit 0

# ── 提取 type ─────────────────────────────────────
note_type=$(echo "$fm" | grep -E '^type:\s*' | head -1 | sed 's/^type:\s*//' | tr -d '"'"'" | xargs)
[ -z "$note_type" ] && exit 0

# ── type → 模板映射 ───────────────────────────────
template=""
case "$note_type" in
  diary)    template="9 - SYSTEM/Templates/日记模板.md" ;;
  project)  template="9 - SYSTEM/Templates/项目笔记模板.md" ;;
  book)     template="9 - SYSTEM/Templates/读书笔记模板.md" ;;
  course)   template="9 - SYSTEM/Templates/课程笔记模板.md" ;;
  article)  template="9 - SYSTEM/Templates/文章笔记模板.md" ;;
  llm)      template="9 - SYSTEM/Templates/对话日志模板.md" ;;
  atomic)   template="9 - SYSTEM/Templates/原子笔记模板.md" ;;
  dashboard|system) exit 0 ;;   # 无对应模板
  *)        exit 0 ;;            # 未知 type，不误报
esac

[ -f "$template" ] || { echo "⚠️  模板文件不存在: $template"; exit 0; }

# ── 提取顶层字段名（排除注释与空行）───────────────
get_fields() {
  echo "$1" | grep -E '^[a-zA-Z]' | sed 's/:.*//' | sed 's/[[:space:]]*$//' | sort -u
}

note_fields=$(get_fields "$fm")
[ -z "$note_fields" ] && exit 0

tpl_fm=$(sed -n '/^---$/,/^---$/p' "$template" | sed '1d;$d')
tpl_fields=$(get_fields "$tpl_fm")
[ -z "$tpl_fields" ] && exit 0

# ── diff 比对 ─────────────────────────────────────
extra=$(comm -23 <(echo "$note_fields") <(echo "$tpl_fields") | tr '\n' ' ' | xargs)
missing=$(comm -13 <(echo "$note_fields") <(echo "$tpl_fields") | tr '\n' ' ' | xargs)

if [ -n "$extra" ] || [ -n "$missing" ]; then
  tpl_name=$(basename "$template")
  echo "📋 Frontmatter 与模板 [$tpl_name] 不一致:"
  [ -n "$extra" ]   && echo "  ➕ 多了: $extra"
  [ -n "$missing" ] && echo "  ➖ 少了: $missing"
  echo "> 💡 建议重新用 Templater 插入模板创建笔记。"
fi

exit 0
