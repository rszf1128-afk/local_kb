---
title: Embedded Domain Home
type: moc
domain: embedded
status: active
tags:
  - embedded
  - stm32
  - moc
  - hardware
---

# 嵌入式开发领域入口

这个领域用于沉淀：

## 这份文档负责什么

这份文档负责：

- 作为 `embedded/嵌入式` 领域的总入口
- 告诉 AI 命中嵌入式问题后应先从什么方向进入
- 说明当前纯模块阶段已经预留了什么、还没有什么

这份文档不负责：

- 假装已经包含完整板级 bring-up 和驱动知识库
- 代替未来正式条目承载具体外设个案
- 吞掉本应回到 `PX4` 或 `shared` 的问题

- `STM32H73` 相关开发经验
- 外设驱动、串口、DMA、中断、时钟树经验
- `NuttX/POSIX` 适配层经验
- 板级 bring-up/上板经验

当前状态：

- 结构已预留
- 正式条目待逐步补充

## 当前边界

- 当前包含：
  - 嵌入式领域入口
  - 首批主题建议
  - 与 `PX4 / NuttX / 驱动 / 板级 bring-up` 的语义关系
- 当前不包含：
  - 具体板卡长期知识
  - 真实项目中的外设个案经验
  - 成体系的正式 checklist 和模式条目

## 语义关联

`embedded/嵌入式` 在知识图谱里通常同时连接到：

- `硬件平台`
- `驱动`
- `板级 bring-up`
- `PX4/NuttX`

推荐首批知识主题：

1. `STM32H73` 最小 bring-up 清单
2. 驱动调试时的证据采样规范
3. `PX4 + NuttX` 板级适配 checklist
4. 外设异常时的日志与寄存器观察模板

## AI 进入本领域后的最小动作

1. 先把本页作为嵌入式领域入口
2. 先判断问题更偏 bring-up、驱动、日志采样还是 `PX4/NuttX` 适配
3. 如果当前工程已有正式条目，再继续读取最相关条目
4. 如果当前还没有正式知识，先写草稿或请求确认，不直接膨胀为正式知识

## 推荐回写位置

- 稳定的 bring-up / driver / checklist：写入正式条目
- 还在排查中的新结论：先落 `drafts/`
- 明显跨领域的方法与治理经验：回到 `shared`

## 相关主题

- [[../../MOCs/01_Domain_Graph|领域图谱]]
- [[../../MOCs/02_Control_Simulation_Graph|控制与仿真图谱]]
- [[../px4/README|PX4 领域]]
- [[../qgc/README|QGC 领域]]
- [[../shared/README|通用领域]]
