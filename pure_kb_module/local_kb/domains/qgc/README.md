---
title: QGC Domain Home
type: moc
domain: qgc
status: active
tags:
  - qgc
  - qgroundcontrol
  - moc
  - ground-station
---

# QGC 开发领域入口

这个领域用于沉淀：

## 这份文档负责什么

这份文档负责：

- 作为 `QGC/QGroundControl` 领域的总入口
- 告诉 AI 命中 `QGC` 后应先把问题放到什么语义范围里理解
- 说明当前纯模块阶段 `QGC` 领域已经有什么、还缺什么

这份文档不负责：

- 假装已经包含完整 `QGC` 正式知识库
- 直接展开所有 `QML / MAVLink / FactSystem` 细节
- 代替未来真实工程里的 `QGC` 条目承载具体个案

- `QGC/QGroundControl` 页面开发经验
- `QML` 组件和 `FactSystem` 使用经验
- `MAVLink` 地面站交互经验
- 参数面板、地图、通信和插件开发经验

当前状态：

- 结构已预留
- 正式知识条目待后续逐步补充

## 当前边界

- 当前包含：
  - `QGC` 领域入口
  - 首批主题建议
  - 与 `PX4 / MAVLink / 参数系统` 的语义关系
- 当前不包含：
  - 完整正式条目
  - 真实项目中的 `QGC` 私有经验
  - 细分页面和具体消息链的长期沉淀

## 语义关联

`QGC` 在知识图谱里通常同时连接到：

- `PX4`
- `MAVLink`
- 参数系统
- 调试与验证链

推荐首批知识主题：

1. `QML + FactPanel` 页面改动模式
2. 参数显示与绑定调试
3. `MAVLink` 消息链排查
4. 设备连接、串口、网络链路经验

## AI 进入本领域后的最小动作

1. 先把本页作为 `QGC` 领域入口
2. 先判断问题更偏 `QML`、参数系统、连接链路还是 `MAVLink`
3. 如果当前工程已有对应正式条目，再继续进入最相关条目
4. 如果还没有正式知识，先生成草稿或请求确认，不直接扩写正式知识

## 推荐回写位置

- 稳定的 `QGC` 模式或 checklist：写成正式条目
- 还在排查中的新结论：先落 `drafts/`
- 跨 `QGC / PX4 / embedded` 的治理或方法问题：回到 `shared`

## 相关主题

- [[../../MOCs/01_Domain_Graph|领域图谱]]
- [[../../MOCs/03_Capture_Governance_Graph|沉淀与治理图谱]]
- [[../px4/README|PX4 领域]]
- [[../embedded/README|嵌入式领域]]
- [[../shared/README|通用领域]]
