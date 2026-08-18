#!/bin/bash
# 拦截危险 Bash 命令
# PreToolUse hook on Bash 自动调用

cmd=$(jq -r '.tool_input.command // ""' 2>/dev/null)
if [ -z "$cmd" ]; then
  exit 0
fi

# 危险模式列表
if echo "$cmd" | grep -qE 'rm\s+-rf\s+/|git\s+push\s+--force|git\s+reset\s+--hard|:\(\)\s*\{|dd\s+if=/dev/zero'; then
  echo "🔴 危险命令被拦截: $cmd"
  exit 2
fi

exit 0
