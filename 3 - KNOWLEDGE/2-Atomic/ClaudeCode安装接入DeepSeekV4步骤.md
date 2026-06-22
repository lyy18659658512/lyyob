---
title: ClaudeCode安装接入DeepSeekV4步骤
type: atomic
created: 2026-06-16
updated: 2026-06-16
tags: []
source: ""
links: []
aliases: []
---
## ClaudeCode安装接入DeepSeekV4步骤
### 安装ClaudeCode运行环境Node.js
- 进入官网[Node.js — 在任何地方运行 JavaScript](https://nodejs.org/zh-cn)
- 点击获取Node.s→点击获取Windows安装程序
- 打开安装程序进行安装
- 检查是否安装成功，命令行窗口输入以下命令，正确显示版本号说明安装成功
- ```
  node -v
  npm -v
  ```
## 安装git
- 进入官网[Git](https://git-scm.com/)
- 点击windows安装 ，选择对应版本安装程序，Windows 上打开 **任务管理器 → 性能 → CPU**，查看"架构"一栏：
	- `x64` → 选非 ARM 版本
	- `ARM64` → 选 ARM 版本
- 打开安装程序进行安装
- 检查是否安装成功，命令行窗口输入以下命令，正确显示版本号说明安装成功
- ```
  git -v
  ```
## 安装CCSwitch
- 进入GitHub仓库[发行作品 ·Farion1231/CC-交换机](https://github.com/farion1231/cc-switch/releases)
- 下滑页面，找到对应的版本下载
- 打开安装程序进行安装

## 安装Claude Code
- 用[[包管理器]]下载，打开命令行输入npm install -g @anthropic-ai/claude-code
- 检查是否安装成功，输入命令
- ```
  claude -v
  ```
- 启动，输入命令,跳出错误，需修改配置文件
- ```
  claude
  ```
- C盘用户名文件夹下，找到打开Claude.json文件，加一个字段和字段值（==上一个字段尾部加英文逗号==）："hasCompletedOnboarding": true
- 修改完成后，重新启动，就不会跳出错误

## 接入Deep seek
- 创建APIkey,复制密匙
- 打开CCSWITH，选择右上角+，选择deep seek，填入密匙
- 模型槽位分别填入deepseek-v4-pro或deepseek-v4-flash，一个便宜一个贵，按需填写
- 重新启动Claude，启动后输入/model,可查看到刚刚模型槽位配置的模型