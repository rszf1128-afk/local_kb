---
title: Demo Domain Home
type: moc
domain: demo
status: active
tags:
  - demo
  - moc
  - knowledge-base
  - sample
---

# Demo 领域入口

这个领域用于演示纯知识库模块如何在没有私有知识的情况下跑通完整闭环。

## 这份文档负责什么

这份文档负责：

- 作为 `demo` 领域的总入口
- 告诉 AI 先从哪里进入 demo 领域
- 说明这个领域的演示边界、测试方式和相关主题

这份文档不负责：

- 假装自己是真实业务知识库
- 代替正式模式笔记承载具体排查细节
- 指导真实工程如何长期组织自己的领域知识

它不是业务真实知识，只是一个最小可公开示例，用来验证：

- `route`
- `best_entry`
- `digest`
- `capture`
- `suggested_writeback`

## 当前包含什么

- 一条正式模式笔记：`demo_motor_not_spinning_pattern.md`
- 一个草稿目录：`drafts/`
- 一组可直接复测的示例请求

## 这个领域怎么用

推荐顺序是：

1. 先让总库命中 `demo`
2. 再读取本页作为领域入口
3. 再进入 `demo_motor_not_spinning_pattern.md`
4. 最后通过 `capture` 把新结论落到 `drafts/`

## 当前 demo 的语义边界

**结构化元信息**

- `layer`: `entrypoint`
- `symptom`: 纯模块虽然能路由，但没有一个最小领域可以完整演示从命中知识到生成草稿的闭环
- `evidence`:
  - 纯模块当前主要承载总路由、总治理和领域入口
  - 如果没有最小 demo 领域，就难以在新工程里直观看到完整闭环
- `recommended_action`:
  - 先把本领域作为最小 demo 入口读取
  - 先复测正式条目命中、摘要生成和 capture 草稿生成
  - 再决定是否替换成新工程自己的真实领域知识
- `portability`: `high`
- `confidence`: `verified`

## 推荐测试请求

1. `帮我分析 demo 机器人电机不转的问题。`
2. `请总结 demo 机器人电机不转这次排查，并写成知识草稿。`
3. `如果 demo 领域没有这个主题，请先问我要不要创建。`

## 推荐回写位置

- 演示过程的新结论：`local_kb/domains/demo/drafts/`
- 多次复用后的稳定模式：更新正式条目

## 相关主题

- [[demo_motor_not_spinning_pattern|demo 电机不转排查模式]]
- [[../shared/README|shared / 通用治理]]
