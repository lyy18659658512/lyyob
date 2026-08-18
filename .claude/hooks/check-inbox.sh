#!/bin/bash
# 检查 INBOX 是否有待处理文件
# SessionStart hook 自动调用

inbox_dir="0 - INBOX"

if [ ! -d "$inbox_dir" ]; then
  exit 0
fi

# 统计 .md 文件数量
files=$(ls "$inbox_dir"/*.md 2>/dev/null)
if [ -z "$files" ]; then
  exit 0
fi

count=$(echo "$files" | wc -l)
echo "📥 INBOX 中有 $count 个待处理文件："
echo "$files" | while read f; do
  echo "  - $(basename "$f")"
done
echo "> 💡 可用 conversation-log / weread-book-note 等 Skill 处理。"
