# Obsidian 编写规范

## 1. 目标

这套知识库默认按 `Obsidian` 友好方式编写，目的是：

- 你自己可以继续把它当笔记系统用
- AI 可以读取统一结构
- 同事可以快速浏览和维护

## 2. 推荐规则

### 2.1 每个笔记都带 frontmatter

建议字段：

```yaml
---
title: note title
type: moc | principle | pattern | case | checklist | capture
domain: px4 | qgc | embedded | shared
status: draft | active | deprecated
theme: control | simulation | tooling | governance | hardware
parents:
  - parent topic
related:
  - related topic
tags:
  - knowledge-base
  - px4
---
```

说明：

- `theme`
  - 用于表达这条笔记更偏哪个主题
- `parents`
  - 用于表达它在知识语义上挂在哪些上层主题下
- `related`
  - 用于表达横向交叉关系

**结构化元信息**

- `layer`: `format`
- `symptom`: 笔记缺少稳定元信息，导致 AI 路由、图谱理解和人工筛选都不稳定
- `evidence`:
  - `frontmatter` 可承载 `domain/type/status/theme`
  - 元信息稳定后更容易被脚本转译和筛选
- `recommended_action`:
  - 新笔记默认补齐 `frontmatter`
  - 至少保持 `title/type/domain/status/tags`
- `portability`: `high`
- `confidence`: `verified`

### 2.2 使用 MOC

推荐用 `MOC/Map of Content/内容地图` 做导航页：

- 总入口页
- 已知领域入口页
- 新领域入口页

### 2.3 使用 wikilink

推荐优先使用：

- `[[kb_user_manual]]`
- `[[domains/px4/README]]`
- `[[domains/shared/README]]`

这样在 `Obsidian` 里浏览最顺畅。

推荐同时显式写出：

- 上游主题
- 平行主题
- 相关子图

**结构化元信息**

- `layer`: `graph`
- `symptom`: 知识之间只有文件夹关系，没有语义连接，导致 `Obsidian` 图谱和 AI 主题理解都偏弱
- `evidence`:
  - `wikilink` 能表达上游、平行和子图关系
  - 单靠文件夹位置无法表达交织知识
- `recommended_action`:
  - 关键笔记优先补 `wikilink`
  - 同时补上上游主题、平行主题和子图入口
- `portability`: `high`
- `confidence`: `verified`

### 2.4 一条笔记只解决一类问题

避免在一个笔记里同时混入：

- 设计背景
- 调试时间线
- 最终经验

推荐拆开：

- `Case/个案`
- `Pattern/模式`
- `Checklist/清单`

### 2.5 技术术语规则

统一保留：

- 原始英文术语
- 必要中文解释

例如：

- `uORB/topic 总线`
- `SITL/软件在环仿真`
- `QGC/QGroundControl`
- `STM32H73/微控制器`

### 2.6 新领域创建规则

当出现新的知识领域时：

1. 先确认用户是否同意创建
2. 再按 `domain_home_template.md` 生成新领域入口
3. 优先创建 `draft/草稿`，不要直接堆积正式笔记

**结构化元信息**

- `layer`: `governance`
- `symptom`: 新领域一出现就开始堆正式笔记，导致入口不清晰、图谱不完整且后续迁移困难
- `evidence`:
  - 新领域通常需要先有领域入口和最初骨架
  - 直接堆正式笔记会跳过结构设计
- `recommended_action`:
  - 先确认用户是否创建新领域
  - 先生成领域入口和草稿，再逐步沉淀正式知识
- `portability`: `high`
- `confidence`: `verified`

## 3. 推荐目录结构

```text
local_kb/
  README.md
  kb_manifest.yaml
  kb_user_manual.md
  kb_bootstrap_prompt.md
  kb_obsidian_conventions.md
  MOCs/
  domains/
  templates/
  tools/
```

## 4. 草稿规则

自动生成的知识草稿建议：

- 放到 `drafts/`
- 带时间戳
- 经人工审阅后再并入正式笔记
- 新领域也应先生成骨架，再人工确认归档位置

## 5. 与脚本配合

脚本层可以把结构化字段转译为：

- `Obsidian` 笔记
- 紧凑 `JSON`
- AI 可读的最小摘要

所以推荐长期坚持 `Markdown` 主存、脚本投影的路线，而不是直接让机器表示成为唯一真源。

## 6. 图谱优先规则

如果目录层级和知识语义冲突，优先相信：

1. `wikilink`
2. `MOC`
3. `frontmatter` 中的 `parents/related/theme`

而不是仅仅相信文件夹位置。

**结构化元信息**

- `layer`: `graph`
- `symptom`: 目录结构和知识语义冲突时，不知道应该以哪个为准，导致路径调整后整体认知被打乱
- `evidence`:
  - 目录主要服务于落盘和仓库管理
  - 语义主线更适合由 `wikilink/MOC/frontmatter` 表达
- `recommended_action`:
  - 语义冲突时优先相信图谱连接
  - 文件夹位置只作为存储边界，不作为唯一知识关系依据
- `portability`: `high`
- `confidence`: `verified`
