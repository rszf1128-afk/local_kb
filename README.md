# Pure KB Module

> 这不是在公开某个人的私有知识内容。  
> *This repository does not publish anyone's private knowledge content.*

> 它公开的是一套可复用的、本地优先的人机协作框架，让你把自己的知识、本地经验和 AI 工作流接进来，并持续演化。  
> *It publishes a reusable, local-first human-AI collaboration framework that lets you connect your own knowledge, local experience, and AI workflows, then keep evolving them over time.*

【https://github.com/rszf1128-afk/local_kb教程】 https://www.bilibili.com/video/BV1x8VH6uEVz/?share_source=copy_web&vd_source=5d4b33e0957c12bc60060601ac596228

## 项目概览

这套模块最核心的目标，不是“多存一点内容”，而是让 `AI + 本地知识库 + 人工确认` 形成长期闭环。  
*The core goal is not just to store more content, but to create a long-term loop between `AI + local knowledge base + human confirmation`.*

它主要做 3 件事：  
*It mainly does 3 things:*

1. `retrieve / 查用`
   - 先读 `manifest`，优先找最相关知识，避免 AI 每次像失忆一样重来。
   - *Read the `manifest` first, find the most relevant knowledge first, and avoid restarting from scratch in every new AI session.*
2. `capture / 沉淀`
   - 把稳定结论整理成草稿，并给出建议回写位置。
   - *Turn stable conclusions into drafts and suggest where they should be written back.*
3. `governance / 治理`
   - 持续优化路由、结构、提示词和回写方式。
   - *Continuously improve routing, structure, prompts, and write-back behavior.*

## 仓库意图

这个仓库真正想推动的，不是再做一个“AI memory”或“知识库产品”，而是推动一种可长期演化的人机协作方式。  
*This repository is not trying to become yet another "AI memory" or "knowledge base product". It is trying to push forward a durable, evolvable way of human-AI collaboration.*

更高层目标是：  
*The higher-level goals are:*

- 让人类和 AI 形成长期协作，而不是只靠单次对话上下文。  
  *Enable long-term collaboration between humans and AI instead of relying only on one-off conversation context.*
- 让每个人都能保留自己的私有知识，同时持续优化自己的 AI 使用方式。  
  *Let each person keep their private knowledge while continuously improving how they work with AI.*
- 把真正可公开的部分沉淀成一套别人也能复用的框架。  
  *Extract the genuinely shareable part into a reusable framework for others.*

这里公开的重点是：  
*What is being published here is mainly:*

- `method`
- `skill orchestration`
- `protocol framework`

不是公开私有知识本体。  
*It is not about publishing private knowledge itself.*

## 为什么治理重要

这套模块最关键的不是单次查用，而是 `governance / 治理` 模式。  
*The most important part of this module is not one-time retrieval, but the `governance` mode.*

治理负责让系统逐步学会：  
*Governance helps the system gradually learn:*

- 这次该先读什么。  
  *What should be read first for the current task.*
- 这类问题应该落到哪个领域。  
  *Which domain this kind of question should route to.*
- 哪些经验值得回写。  
  *Which experience is worth writing back.*
- 哪些规则需要调整。  
  *Which rules should be adjusted.*

更直白地说：  
*More directly:*

- `retrieve`：解决当前问题  
  *Solve the current problem.*
- `capture`：沉淀本次经验  
  *Capture this round of experience.*
- `governance`：优化以后如何更好地使用这套知识系统  
  *Improve how the system will be used in the future.*

## 从这里开始

如果你第一次来到这个仓库，不要先把所有文档读一遍。  
*If this is your first time here, do not start by reading every document.*

先做这 2 步：  
*Start with these 2 steps:*

1. 把 `pure_kb_module/` 复制到你的工程根目录。  
   *Copy `pure_kb_module/` into the root of your project.*
2. 打开 [START_WITH_AI.md](./START_WITH_AI.md)，把里面那段提示词直接贴给 AI。  
   *Open [START_WITH_AI.md](./START_WITH_AI.md) and paste the prompt inside directly to your AI tool.*

当前推荐第一次使用时复制**整个** `pure_kb_module/`，而不是只复制 `local_kb/`。  
*For first-time use, it is recommended to copy the **entire** `pure_kb_module/`, not just `local_kb/`.*

原因是：  
*The reason is:*

- `local_kb/` 是知识库本体和运行核心。  
  *`local_kb/` is the knowledge-base core and runtime center.*
- `START_WITH_AI.md`、`QUICKSTART.md`、`ARCHITECTURE.md`、`examples/demo_workspace/` 负责首贴提示词、接入说明、架构说明和最小 demo 验证。  
  *`START_WITH_AI.md`, `QUICKSTART.md`, `ARCHITECTURE.md`, and `examples/demo_workspace/` provide the initial prompt, integration guide, architecture explanation, and minimal demo validation.*

如果第一轮接入已经完成，还想让 AI 自动生成当前工具专属适配层，再看：  
*If the first integration is already done and you want AI to generate a tool-specific adapter, continue with:*

- [GENERATE_ADAPTER_FOR_YOUR_AI.md](./GENERATE_ADAPTER_FOR_YOUR_AI.md)

## 主要文件

如果你只想快速知道主要内容，看这几个就够了：  
*If you only want the key entry points, these files are enough:*

- [START_WITH_AI.md](./START_WITH_AI.md)  
  *第一入口，直接复制给 AI。*  
  *First entry point, meant to be pasted into your AI tool.*
- [QUICKSTART.md](./QUICKSTART.md)  
  *最短手动接入路径。*  
  *The shortest manual integration path.*
- [INTEGRATE_INTO_YOUR_PROJECT.md](./INTEGRATE_INTO_YOUR_PROJECT.md)  
  *demo 跑通后，如何接入真实工程。*  
  *How to integrate it into a real project after the demo works.*
- [GENERATE_ADAPTER_FOR_YOUR_AI.md](./GENERATE_ADAPTER_FOR_YOUR_AI.md)  
  *第一轮接入后，如何生成工具专属 adapter。*  
  *How to generate a tool-specific adapter after the first integration.*
- [ARCHITECTURE.md](./ARCHITECTURE.md)  
  *为什么这样设计。*  
  *Why the system is designed this way.*
- [RELEASE_CHECKLIST.md](./RELEASE_CHECKLIST.md)  
  *公开发布前的快速检查清单。*  
  *A quick pre-release checklist for public publishing.*

## 它解决什么问题

这套模块主要解决 4 个问题：  
*This module mainly solves 4 problems:*

1. AI 一开新对话就像失忆一样重来。  
   *AI starts over like it has amnesia in every new conversation.*
2. 同类问题被反复解释，经验难以复用。  
   *Similar issues get re-explained again and again, and experience is hard to reuse.*
3. 经验只停留在聊天记录里，难以沉淀为本地资产。  
   *Experience stays inside chat history instead of becoming a local asset.*
4. 知识库越长越乱，缺少路由、治理和回写闭环。  
   *As the knowledge base grows, it becomes messy without routing, governance, and write-back loops.*

## 核心思想

这不是一个固定领域的知识库产品，而更像一个本地优先的知识协作协议。  
*This is not a fixed-domain knowledge-base product. It is closer to a local-first collaboration protocol for knowledge work.*

它的核心做法是：  
*Its core approach is:*

- 用 `manifest` 做路由。  
  *Use a `manifest` for routing.*
- 用 `Markdown + Obsidian` 存知识。  
  *Store knowledge in `Markdown + Obsidian`.*
- 用脚本做 `route / best_entry / digest / capture`。  
  *Use scripts for `route / best_entry / digest / capture`.*
- 用 `suggested_writeback / governance_feedback` 持续自我优化。  
  *Use `suggested_writeback / governance_feedback` for continuous self-improvement.*

一句话说：  
*In one sentence:*

- 公开的是协作协议。  
  *What is public is the collaboration protocol.*
- 本地长出的是每个人自己的知识系统。  
  *What grows locally is each person's own knowledge system.*

## 仓库包含什么

当前纯模块包含：  
*This module currently includes:*

- `pure_kb_module/`  
  *当前推荐复制到新工程里的完整可用包。*  
  *The full package recommended for copying into a new project.*
- `local_kb/`  
  *知识库本体、总入口、路由规则、治理规则、模板和脚本。*  
  *The knowledge-base core, entry point, routing rules, governance rules, templates, and scripts.*
- `.trae/skills/`  
  *当前 IDE 的可选适配层，可在接入后再生成或调整。*  
  *An optional adapter layer for the current IDE, which can be generated or adjusted after integration.*
- `examples/demo_workspace/`  
  *一个最小 demo 场景，用来演示完整闭环。*  
  *A minimal demo workspace that demonstrates the full loop.*

## 仓库不包含什么

这里默认不包含：  
*This repository intentionally does not include:*

- 私有领域知识  
  *Private domain knowledge*
- 私有案例  
  *Private cases*
- 历史调试记录  
  *Historical debugging records*
- 私有草稿  
  *Private drafts*
- 只适用于原工作区的上下文  
  *Context that only makes sense in the original workspace*

## 演示

仓库自带一个最小 `demo` 领域，它不是业务真实知识，只用于演示完整流程。  
*The repository ships with a minimal `demo` domain. It is not real business knowledge and is only used to demonstrate the full workflow.*

它演示的能力包括：  
*It demonstrates:*

- `route`
- `best_entry`
- `digest`
- `capture`
- `capture --save-draft --confirm`

相关入口：  
*Related entry points:*

- [demo/README.md](./local_kb/domains/demo/README.md)
- [demo_motor_not_spinning_pattern.md](./local_kb/domains/demo/demo_motor_not_spinning_pattern.md)

## 如何接入你的项目

更稳的方式不是把 demo 当成真实知识，而是：  
*The safer way is not to treat the demo as real knowledge, but to:*

1. 保留 `local_kb/` 作为总知识库入口。  
   *Keep `local_kb/` as the main knowledge-base entry point.*
2. 先跑通 demo 闭环。  
   *First make the demo loop work.*
3. 再用你自己的领域入口替换或补充 `demo`。  
   *Then replace or extend `demo` with your own domain entry points.*
4. 最后按你的工程语义更新 `kb_manifest.yaml`。  
   *Finally update `kb_manifest.yaml` based on your project's semantics.*

更多接入细节：  
*For more integration details:*

- [INTEGRATE_INTO_YOUR_PROJECT.md](./INTEGRATE_INTO_YOUR_PROJECT.md)

## 当前状态

当前这版已经能独立演示：  
*The current version can already demonstrate:*

- 总路由  
  *Global routing*
- 查用  
  *Retrieval*
- 沉淀  
  *Capture*
- 治理  
  *Governance*
- 草稿回写建议  
  *Suggested draft write-back targets*
