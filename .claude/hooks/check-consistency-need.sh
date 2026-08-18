#!/bin/bash
# 检查系统文件自上次一致性检测以来是否有变更
# SessionStart hook 自动调用，stdout 会注入 Claude 上下文

LAST_REPORT_DIR=".claude/skills/consistency-check"
SYSTEM_PATHS=(
  "9 - SYSTEM/Templates/"
  "9 - SYSTEM/知识库操作规范.md"
  "9 - SYSTEM/变更记录.md"
  "CLAUDE.md"
  ".claude/skills/"
)

# 找到最近一次检测报告
latest_report=$(ls -t "$LAST_REPORT_DIR"/report-*.md 2>/dev/null | head -1)

if [ -z "$latest_report" ]; then
  echo "⚠️ 尚未运行过一致性检测，建议运行 consistency-check 建立基线。"
  exit 0
fi

# 检查是否有系统文件比报告更新
changed_count=0
for path in "${SYSTEM_PATHS[@]}"; do
  if [ -e "$path" -o -d "$path" ]; then
    newer=$(find "$path" -newer "$latest_report" -type f 2>/dev/null | head -5)
    if [ -n "$newer" ]; then
      changed_count=$((changed_count + 1))
    fi
  fi
done

if [ "$changed_count" -gt 0 ]; then
  echo "🔍 自上次一致性检测（$(basename "$latest_report")）以来，有 $changed_count 处系统目录/文件发生了变更。"
  echo "> 💡 建议运行 **consistency-check** 检查模板、规范、CLAUDE.md 是否同步。"
fi
