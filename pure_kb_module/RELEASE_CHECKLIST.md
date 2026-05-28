# Release Checklist

这份文档专门用于首版公开发布前的最后检查。

## 这份文档负责什么

这份文档负责：

- 帮你在发布前快速检查当前模块是否适合公开
- 给出最小测试命令和通过标准
- 帮你确认公开边界是否干净

这份文档不负责：

- 代替 `README.md` 讲项目使命
- 代替 `QUICKSTART.md` 做接入说明
- 代替 `ARCHITECTURE.md` 解释设计细节

## 1. 公开边界

发布前先确认当前仓库里不包含下面这些内容：

- 私有领域知识
- 私有案例
- 历史聊天记录
- 历史调试记录
- 私有草稿
- 只对原工作区成立的上下文

## 2. 首页入口

确认首页已经能回答下面 4 个问题：

1. 这个项目想实现什么使命目标
2. 这个项目公开的到底是什么
3. 第一次使用应该先做什么
4. 每份核心文档分别负责什么

最小检查位置：

- `README.md`
- `START_WITH_AI.md`
- `QUICKSTART.md`

## 3. 核心路由入口

确认 `local_kb/kb_manifest.yaml` 已经满足：

- 它是唯一固定入口
- 它包含 `intent_routing`
- 它包含 `domain_routing`
- 它包含 `creation_policy`
- 它没有把 `skill` 写成唯一前置条件

## 4. demo 闭环测试

进入仓库根目录后，至少跑通下面 4 个命令：

```bash
python3 local_kb/tools/kb_dispatch.py route --text "帮我分析 demo 机器人电机不转的问题" --format json
python3 local_kb/tools/kb_dispatch.py best-entry --text "demo 电机不转怎么排查" --format json
python3 local_kb/tools/kb_dispatch.py digest --text "把 demo 电机不转排查整理成最小摘要" --format json
python3 local_kb/tools/kb_dispatch.py capture --text "请总结 demo 电机不转这次排查，并写成知识草稿" --format json
```

最小通过标准：

- `route` 命中 `demo`
- `best-entry` 命中 `local_kb/domains/demo/demo_motor_not_spinning_pattern.md`
- `digest` 返回 `best_entry` 和 `suggested_writeback`
- `capture` 返回 `local_kb/domains/demo/drafts` 作为草稿回写目标

## 5. adapter 第二阶段

确认下面这些入口都存在且职责清楚：

- `GENERATE_ADAPTER_FOR_YOUR_AI.md`
- `ADAPTER_SPEC.md`
- `ADAPTER_SCHEMA.yaml`
- `local_kb/adapters/README.md`

同时确认：

- `Trae` 只是一个样例，不是唯一实现
- 没有把整份知识库正文复制进 adapter 文档
- 没有把 `SKILL.md` 写成首入口

## 6. 文档一致性

发布前快速扫一遍，确认没有明显冲突：

- `README.md`
- `MODULE_PLAN.md`
- `ARCHITECTURE.md`
- `INTEGRATE_INTO_YOUR_PROJECT.md`

重点检查：

- 当前主线是否仍然写成固定架构主线
- `skill` 是否仍被写成前置必带
- 是否还有过期目录结构描述

## 7. 建议发布方式

更稳的发布方式是：

1. 先把 `pure_kb_module/` 复制到一个干净目录
2. 在干净目录里初始化新的 Git 仓库
3. 在那个目录里再做一次最小测试
4. 再推送到 GitHub

## 8. 发布时的口径

当前最适合的发布口径是：

- `first public release`
- `v0.1`
- `public preview`

不建议当前直接写成：

- 完整成熟产品
- 已覆盖所有 AI 工具
- 已包含完整公开知识内容

## 9. 发布后第一件事

首版发出去后，建议第一时间沉淀一份发布复盘，至少记录：

- 哪些入口最容易让人理解
- 哪些地方仍然容易误解
- 哪些地方最需要继续补样例
- 下一轮优先增强体系、验证效果还是连续性
