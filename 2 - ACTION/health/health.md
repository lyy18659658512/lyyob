---
title: 健康
type: dashboard
created: 2026-06-11
updated: 2026-06-11
tags: [health]
---

# 🏃 健康

## 🎯 目标
<!-- 在这里写你的健康长期目标 -->

## 🚀 当前项目

```dataview
TABLE deadline AS "截止", created AS "创建"
FROM "2 - ACTION/health"
WHERE status = "active"
SORT deadline ASC
```

## 🌱 持续关注

```dataview
TABLE created AS "创建"
FROM "2 - ACTION/health"
WHERE status = "ongoing"
SORT created DESC
```

## 📌 推荐链接
-

## 🔗 相关 KNOWLEDGE
-
