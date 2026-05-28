---
title: Demo Motor Not Spinning Pattern
type: pattern
domain: demo
status: active
theme: troubleshooting
parents:
  - demo domain
related:
  - demo capture
  - troubleshooting
  - writeback
tags:
  - knowledge-base
  - demo
  - pattern
  - troubleshooting
---

# demo 电机不转排查模式

这个模式用于演示最小知识闭环，不代表真实项目经验。

## 适用症状

- demo 机器人电机不转
- 控制指令已经发出，但执行器没有响应
- 日志里没有立即暴露明显代码错误

**结构化元信息**

- `layer`: `pattern`
- `symptom`: demo 机器人电机不转，但当前还没有真实工程知识，需要一个足够小的正式条目来演示命中、摘要和回写闭环
- `evidence`:
  - 控制指令已发送，但电机输出为零
  - 常见根因往往先集中在使能状态、仿真开关或参数门限，而不是立即深入代码细节
  - 对 demo 来说，最重要的是提供一个足够清楚、可复测、可回写的排查模板
- `recommended_action`:
  - 先检查电机使能开关是否开启
  - 再检查安全锁或仿真使能参数是否阻止输出
  - 最后记录观察、解释、动作和复测结果，沉淀为 capture 草稿
- `portability`: `high`
- `confidence`: `verified`

## 最小排查步骤

1. 检查执行器是否处于 enable 状态
2. 检查安全锁、arming 或 demo 开关是否阻断输出
3. 检查最小输出阈值是否把命令截断为零
4. 记录观察与修复动作，必要时沉淀到草稿

## 最小证据

- 控制链有输出意图
- 执行器状态为 disable 或被门限截断
- 修改使能或门限后电机恢复响应

## 建议回写

- 若只是一次演示过程：写入 `local_kb/domains/demo/drafts/`
- 若这个模式在多个 demo 中复用：补丁更新本页
