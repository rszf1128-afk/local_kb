# Pure KB Module Plan

这份文档不再描述“准备怎么抽离”。

当前 `pure_kb_module/` 已经完成第一轮抽离、整理和公开化包装。
因此这里改为记录：

- 现在已经成型的模块结构
- 当前版本准备公开什么
- 发布前最小验收点
- 发布后的下一轮演进方向

## 当前结构

```text
pure_kb_module/
  README.md
  START_WITH_AI.md
  QUICKSTART.md
  ARCHITECTURE.md
  INTEGRATE_INTO_YOUR_PROJECT.md
  GENERATE_ADAPTER_FOR_YOUR_AI.md
  ADAPTER_SPEC.md
  ADAPTER_SCHEMA.yaml
  MODULE_PLAN.md
  .trae/skills/local-kb-orchestrator/SKILL.md
  local_kb/
    README.md
    kb_manifest.yaml
    kb_bootstrap_prompt.md
    kb_user_manual.md
    kb_usage_guide.md
    kb_creation_policy.md
    kb_confirmation_workflow.md
    kb_obsidian_conventions.md
    tools/
    templates/
    domains/
    adapters/
  examples/
    demo_workspace/
```

## 当前公开对象

当前准备公开的不是私有知识内容，而是：

- `method`
- `skill orchestration`
- `protocol framework`

它们目前已经落成 4 层：

1. `mission layer`
   - 定义为什么做、什么公开、什么保持本地
2. `knowledge layer`
   - 用 `Markdown + Obsidian` 承载知识主存
3. `routing and protocol layer`
   - 用 `manifest + route + best_entry + digest + capture + governance_feedback` 形成闭环
4. `adapter layer`
   - 把同一套协议投影到不同 AI 工具

## 当前已完成

这一轮已经完成的关键项包括：

- 把首入口改成 `copy + paste + let AI adapt`
- 把 `skill` 降级为可选 adapter，而不是前置条件
- 建立 `demo` 领域，能演示 `route / best-entry / digest / capture`
- 建立跨 AI 工具 adapter 生成路径
- 把 GitHub 首页、架构文档、接入文档和 adapter 文档串成完整入口
- 把“主线”从固定架构主线纠偏为动态恢复的会话态主线

## 发布前最小验收

当前版本在公开前至少应满足下面这些条件：

1. 首页能说明使命目标、模型、第一步操作和文档分工
2. `START_WITH_AI.md` 能作为第一入口直接交给 AI
3. `local_kb/kb_manifest.yaml` 能作为唯一固定入口驱动路由
4. `demo` 闭环能跑通：
   - `route`
   - `best-entry`
   - `digest`
   - `capture`
5. adapter 第二阶段文档可读，且不把 `Trae` 误写成唯一实现

## 默认不公开

当前仍然默认不公开：

- 私有领域知识
- 私有案例
- 历史调试记录
- 私有草稿
- 只适用于原工作区的上下文

## 下一轮演进

如果首版公开发布后继续推进，下一轮最值得补的是：

1. 增加更多公开领域样例
2. 增加更多 AI 工具 adapter 样例
3. 增加 adapter 自动校验或自动生成脚本
4. 补公开发布后的复盘与治理沉淀

## 当前状态判断

当前这份模块已经不是“抽离计划”，而是：

- 一个可独立理解的公开框架骨架
- 一个可试跑的最小 demo
- 一个可迁移到新工程的本地知识协作模块

因此它适合以首版公开项目形式发布，但仍应按 `v0.x` 或 `public preview` 理解，而不是作为最终成熟产品描述。
