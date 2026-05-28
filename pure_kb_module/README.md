# Pure KB Module

这不是在公开某个人的私有知识内容。

它公开的是一套可复用的本地优先人机协作框架，让你把自己的知识、本地经验和 AI 工作流接进来，并持续演化。

这套框架由 `pathfinder_czf` 发起与构建。

## What It Does

它主要做 3 件事：

1. `retrieve / 查用`
   - 先读 `manifest`
   - 先找最相关知识
   - 不让 AI 每次像失忆一样重来
2. `capture / 沉淀`
   - 把稳定结论整理成草稿
   - 给出建议回写位置
3. `governance / 治理`
   - 持续优化路由、结构、提示词和回写方式
   - 让 AI 使用这套知识库的方式本身也能被持续改进

这里最重要的不是“存更多内容”，而是让 `AI + 本地知识库 + 人工确认` 形成长期闭环。

## Intention

这个仓库真正想推动的，不是再做一个“AI memory”或“知识库产品”。

更高层目标是：

- 让人类和 AI 形成长期协作，而不是只靠单次对话上下文
- 让每个人都能保留自己的私有知识，同时持续优化自己的 AI 使用方式
- 把真正可公开的部分沉淀成一套别人也能复用的框架

这里公开的重点是：

- `method`
- `skill orchestration`
- `protocol framework`

不是公开私有知识本体。

## Why Governance Matters

这套模块最关键的不是单次查用，而是 `governance / 治理` 模式。

因为治理模式负责让系统逐步学会：

- 这次该先读什么
- 这类问题应该落到哪个领域
- 哪些经验值得回写
- 哪些规则需要调整

也就是说，这一层在做的其实是：

- 让 AI 围绕本地知识库持续自我优化

更直白地说：

- `retrieve` 在解决当前问题
- `capture` 在沉淀这次经验
- `governance` 在优化 AI 以后如何更好地使用这套知识系统

所以这里的治理，不只是“维护文档”，而是在持续优化：

- AI 该怎么读
- AI 该怎么写
- AI 该怎么越来越贴合你的本地知识和使用方式

## Start Here

如果你第一次来到这个仓库，不要先把所有文档读一遍。

先做这 2 步：

1. 把 `pure_kb_module/` 复制到你的工程根目录
2. 打开 [START_WITH_AI.md](./START_WITH_AI.md)，把里面那段提示词直接贴给 AI

这就是当前推荐的最开始操作。

这里的推荐动作是复制**整个** `pure_kb_module/`，而不是首次使用时只单独复制 `local_kb/`。

原因很简单：

- `local_kb/` 是知识库本体和运行核心
- `START_WITH_AI.md`、`QUICKSTART.md`、`ARCHITECTURE.md`、`examples/demo_workspace/` 负责首贴提示词、接入说明、架构说明和最小 demo 验证

如果你已经非常熟悉这套系统，后续当然可以只保留 `local_kb/`；
但第一次接入、迁移测试或公开给别人用时，仍然推荐保留完整 `pure_kb_module/`。

如果第一轮接入已经完成，还想让 AI 自动生成当前工具专属适配层，再继续看：

- [GENERATE_ADAPTER_FOR_YOUR_AI.md](./GENERATE_ADAPTER_FOR_YOUR_AI.md)

## Main Files

如果你只想快速知道“主要内容有哪些”，看这几个就够了：

- [START_WITH_AI.md](./START_WITH_AI.md)
  - 第一入口，复制给 AI
- [QUICKSTART.md](./QUICKSTART.md)
  - 最短手动接入路径
- [INTEGRATE_INTO_YOUR_PROJECT.md](./INTEGRATE_INTO_YOUR_PROJECT.md)
  - demo 跑通后，怎么接到真实工程
- [GENERATE_ADAPTER_FOR_YOUR_AI.md](./GENERATE_ADAPTER_FOR_YOUR_AI.md)
  - 第一轮接入后，怎么生成工具专属 adapter
- [ARCHITECTURE.md](./ARCHITECTURE.md)
  - 为什么这样设计
- [RELEASE_CHECKLIST.md](./RELEASE_CHECKLIST.md)
  - 发布前怎么快速检查

## What It Solves

这套模块主要解决 4 个问题：

1. AI 一开新对话就像失忆一样重来
2. 同类问题被反复解释，经验难以复用
3. 经验只停留在聊天记录里，难以沉淀为本地资产
4. 知识库越长越乱，缺少路由、治理和回写闭环

## Core Idea

这不是一个固定领域的知识库产品。

它更像一个本地优先的知识协作协议：

- 用 `manifest` 做路由
- 用 `Markdown + Obsidian` 存知识
- 用脚本做 `route / best_entry / digest / capture`
- 用 `suggested_writeback / governance_feedback` 持续自我优化

一句话说：

- 公开的是协作协议
- 本地长出的是每个人自己的知识系统

## What Is Included

当前纯模块包含：

- 整个 `pure_kb_module/`
  - 这是当前推荐复制到新工程里的完整可用包
- `local_kb/`
  - 知识库本体、总入口、路由规则、治理规则、模板和脚本
- `.trae/skills/`
  - 当前 IDE 的可选适配层，可在接入后再生成或再调整
- `examples/demo_workspace/`
  - 一个最小 demo 场景，用于演示完整闭环

## What Is Not Included

这里默认不包含：

- 私有领域知识
- 私有案例
- 历史调试记录
- 私有草稿
- 只适用于原工作区的上下文

## Demo

当前自带一个最小 `demo` 领域。

它不是业务真实知识，只用于演示：

- `route`
- `best_entry`
- `digest`
- `capture`
- `capture --save-draft --confirm`

相关入口：

- [demo/README.md](./local_kb/domains/demo/README.md)
- [demo_motor_not_spinning_pattern.md](./local_kb/domains/demo/demo_motor_not_spinning_pattern.md)

## How To Use It In Your Project

最稳的方式不是直接把 demo 当成真实知识，而是：

1. 保留 `local_kb/` 作为总知识库入口
2. 先跑通 demo 闭环
3. 再用你自己的领域入口替换或补充 `demo`
4. 最后按你的工程语义更新 `kb_manifest.yaml`

如果你已经准备把它接到真实工程里，直接看：

- [INTEGRATE_INTO_YOUR_PROJECT.md](./INTEGRATE_INTO_YOUR_PROJECT.md)

## Current Status

当前这版已经能独立演示：

- 总路由
- 查用
- 沉淀
- 治理
- 草稿回写建议

它适合做迁移测试、框架验证和公开说明，不替代你的真实私有知识库。
