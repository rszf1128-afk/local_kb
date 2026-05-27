---
title: Local Knowledge Base Home
type: moc
domain: workspace
tags:
  - knowledge-base
  - obsidian
  - px4
  - qgc
  - embedded
---

# 本地知识库总入口

这是纯知识库模块中的总入口。

## 这份文档负责什么

这份文档负责：

- 作为 `local_kb/` 目录的总入口
- 告诉你总库里先看哪些规则文档
- 告诉你有哪些领域入口和当前边界

这份文档不负责：

- 代替根目录 README 做 GitHub 首页说明
- 代替具体领域 README 承载领域细节
- 代替 adapter 文档说明工具专属接入方式

它负责：

- 总路由
- 总治理
- 总规则
- 领域入口

它不负责承载所有个案知识。

## 目录功能

`local_kb/` 目录主要分成这几类内容：

- `kb_manifest.yaml`
  - 唯一固定入口和总路由规则
- `domains/`
  - 各知识领域入口和正式知识
- `templates/`
  - 新建领域或 capture 草稿时复用的模板
- `tools/`
  - `route / best-entry / digest / capture` 等脚本入口
- `adapters/`
  - 不同 AI 工具的最小 adapter 样例或回退载体

## 先看哪几份

- [[kb_bootstrap_prompt|单句提示词]]
- [[kb_user_manual|用户操作手册]]
- [[kb_usage_guide|维护与使用说明]]
- [[kb_creation_policy|新知识创建策略]]
- [[kb_confirmation_workflow|确认后创建流程]]

## 领域入口

- [[domains/shared/README|shared / 通用治理]]
- [[domains/px4/README|px4]]
- [[domains/qgc/README|qgc]]
- [[domains/embedded/README|embedded]]
- [[domains/demo/README|demo]]

## 当前边界

这个纯模块只保留：

- 总路由
- 总治理
- 领域入口
- 模板与脚本

它不包含原工作区中的私有子知识包和真实领域经验。

当前额外带了一份最小 `demo` 领域，用于演示完整闭环，不代表真实业务知识。

## 给 AI 的最小规则

1. 先读 `kb_manifest.yaml`
2. 先判断 `intent`
3. 再判断 `domain`
4. 只读取最相关入口
5. 优先复用已有知识
6. 新知识先确认创建

## 当前主线

这套系统当前重点不是补某个固定业务域，而是持续完善：

- 主线恢复
- 最小化读取
- capture / 治理闭环
- 知识库自身的连续性

如果用户当前谈的是具体业务域，主线就收束到该业务域；
如果谈的是体系、治理、交付或公开定位，主线才落到总库自身。

## 移植方式

如果你要把这套纯模块搬到新工程里测试，优先保留：

- `local_kb/`
- `.trae/skills/`
- `README.md`

然后把新工程根目录作为工作区打开，再使用 `local_kb/kb_bootstrap_prompt.md` 初始化 AI。
