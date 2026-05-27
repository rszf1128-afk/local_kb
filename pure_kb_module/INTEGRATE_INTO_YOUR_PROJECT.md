# Integrate Into Your Project

这份文档不是解释概念，而是专门回答一件事：

- 当你准备把 `pure_kb_module` 接到一个真实工程里时，应该保留什么、替换什么、修改什么

如果你还没有跑通过 demo，先看：

- `QUICKSTART.md`

如果你想先理解整体设计，再回来做接入，先看：

- `ARCHITECTURE.md`

## 1. 什么时候需要这份文档

你已经不再满足于“先跑通 demo”，而是准备：

- 把这套模块接到自己的真实工程
- 用自己的领域知识替换 `demo`
- 让 AI 开始围绕你的工程做路由、摘要、沉淀和回写

这时就应该看这份文档。

## 2. 先保留什么

第一次接入时，建议先原样保留这些部分：

- `local_kb/`
- `.trae/skills/`
- `README.md`
- `QUICKSTART.md`
- `ARCHITECTURE.md`
- `INTEGRATE_INTO_YOUR_PROJECT.md`

原因很简单：

- `local_kb/` 是知识系统本体
- `.trae/skills/` 是当前 IDE 的适配层
- 根目录几份文档负责对外入口和迁移说明

## 3. 先不要急着改什么

第一次迁移时，不建议一上来就改这些：

- `local_kb/tools/kb_dispatch.py`
- `shared` 领域下的总纲文档
- `kb_creation_policy.md`
- `kb_confirmation_workflow.md`

原因是：

- 这些是当前闭环能稳定跑起来的共性规则
- 先验证你的工程能不能挂到这套规则上
- 再决定是否需要做针对性改动

## 4. 正确接入顺序

推荐按下面顺序做：

1. 把 `pure_kb_module/` 整体复制到你的工程根目录
2. 把新工程目录作为工作区根目录打开
3. 用 `local_kb/kb_bootstrap_prompt.md` 初始化 AI
4. 先跑一次 `demo` 闭环
5. 新建你的真实领域入口
6. 把 `kb_manifest.yaml` 的领域路由改成你的工程语义
7. 再逐步替换或移除 `demo`

这个顺序的目标是：

- 先确认框架可用
- 再挂真实知识
- 最后再做清理

## 5. 你需要新建哪些东西

把 demo 换成真实工程时，至少建议补这三类内容：

### 5.1 领域入口

先创建：

- `local_kb/domains/<your_domain>/README.md`

它负责：

- 说明这个领域管什么
- 提供第一层入口
- 告诉 AI 先看什么，不要乱扩读

### 5.2 正式知识

再逐步补：

- `pattern`
- `principle`
- `checklist`
- `case`

建议一条笔记只解决一类问题。

这部分如何写，直接参考：

- `local_kb/kb_obsidian_conventions.md`

### 5.3 草稿目录

同时准备：

- `local_kb/domains/<your_domain>/drafts/`

因为真实接入后，`capture` 最先产生的通常不是正式知识，而是草稿。

## 6. 你需要改哪些地方

接入真实工程时，最常需要改的是下面几处。

### 6.1 修改 `kb_manifest.yaml`

至少要看这几段：

- `domain_routing`
- `intent_routing`
- `writeback_policy`
- `creation_policy`

其中最重要的是：

- 把 `demo` 替换成你的领域关键词和读取入口
- 保留 `shared` 作为治理与主线恢复总入口

### 6.2 修改领域入口

你的领域 `README.md` 至少要写清楚：

- 领域边界
- 推荐先读哪些正式知识
- 当前还缺哪些知识
- 哪些问题应该继续回到 `shared`

### 6.3 决定是否保留 `demo`

有两种做法都可以：

1. 暂时保留 `demo`
   - 用来持续做闭环回归测试
2. 在真实领域跑稳后移除 `demo`
   - 让模块只保留你的真实入口

如果你刚开始接入，我更建议先保留一段时间。

## 7. 哪些地方不要混在一起

接入真实工程时，最容易出问题的是把这几类东西混写：

- demo 示例知识
- 真实工程正式知识
- 运行中产生的临时草稿
- 私有背景说明

建议分开：

- `demo` 只做演示
- 真实领域只放真实知识
- `drafts/` 只放草稿
- 私有补充信息放在你自己的私有知识域

## 8. 如何判断接入成功

最小验收标准是这 5 条：

1. `route` 能命中你的真实领域
2. `best-entry` 能命中你的领域入口或正式知识
3. `digest` 能给出最小但有用的摘要
4. `capture` 能把新结论落到正确的 `drafts/`
5. `suggested_writeback` 没有持续回到错误位置

如果这 5 条都成立，说明你的工程已经基本接上这套模块。

## 9. 常见错误

最常见的错误包括：

- 只打开 `local_kb/` 子目录，而不是整个工程根目录
- 还没跑通 demo 就大改脚本
- 改了领域目录，但没改 `kb_manifest.yaml`
- 直接把旧聊天整段塞进正式知识
- 新主题一出现就直接创建正式笔记

## 10. 推荐的第一次接入动作

如果你只想按最稳的顺序做一次接入，建议按下面流程：

1. 复制 `pure_kb_module/` 到新工程
2. 跑通 `demo`
3. 新建一个真实领域入口 `README.md`
4. 只放 1 到 3 条最稳定的正式知识
5. 建好 `drafts/`
6. 测一次 `route / best-entry / digest / capture`
7. 再决定是否删掉 `demo`

## 11. 和编写规范的关系

这份文档不替代：

- `local_kb/kb_obsidian_conventions.md`

两者关系是：

- 这份文档回答“模块怎么接”
- `kb_obsidian_conventions.md` 回答“知识怎么写”

真实迁移时，两份文档要一起看，但用途不同。
