# Generate Adapter For Your AI

这份文档专门回答一件事：

- 当 AI 已经完成第一轮最小接入后，如何再自动生成当前工程专属的工具适配层

## 这份文档负责什么

这份文档负责第二阶段：

- 说明什么时候该开始生成 adapter
- 说明不同 AI 工具可以投影成什么 carrier
- 给出可直接复制给 AI 的二阶段提示词

这份文档不负责：

- 代替第一阶段接入入口
- 代替 adapter 的正式评审标准
- 代替机器可读的结构化 schema

这里说的适配层，不只指 `Trae` 的 `SKILL.md`。

它也可以是：

- 某个 AI IDE 的 `skill`
- 某个代理工具的工作区指令文件
- 某个助手的可复用 prompt
- 某个命令包装或 slash command

重点不是文件名，而是：

- 把同一套本地知识库协议，投影成当前 AI 工具能真正使用的入口

如果你不只是想“生成一次”，而是想把这件事做成可复用实现，再同时看：

- `ADAPTER_SPEC.md`
- `ADAPTER_SCHEMA.yaml`

先用一句话区分这 4 份文档：

- `START_WITH_AI.md`：先接入
- `GENERATE_ADAPTER_FOR_YOUR_AI.md`：再生成
- `ADAPTER_SPEC.md`：给人评审
- `ADAPTER_SCHEMA.yaml`：给 AI 或脚本读取

## 1. 先分清什么是 adapter

`adapter` 不是知识库本体。

它只是把下面这些稳定规则，映射成某个具体 AI 工具能理解的形式：

- 唯一固定入口是 `local_kb/kb_manifest.yaml`
- 先做 `intent routing`
- 再做 `domain routing`
- 只做最小化读取
- 优先复用已有知识
- 新知识先确认创建
- 输出时说明读取、复用、缺口和回写建议

所以：

- 稳定规则应该留在 `local_kb/`
- 工具差异才放进 `adapter`

不要把大量知识正文复制进适配层。

## 2. 什么时候再生成 adapter

不要一上来就先生成工具适配层。

推荐顺序是：

1. 先把 `pure_kb_module/` 复制到工程里
2. 先按 `START_WITH_AI.md` 完成第一轮最小接入
3. 先确认当前工程已经能正确命中领域入口
4. 再让 AI 生成当前工具专属 `adapter`

至少满足下面 3 条，再进入这一步：

- `local_kb/kb_manifest.yaml` 已经适配到你的工程语义
- 你的真实领域入口已经存在，或已经确认要先保留 `demo`
- 你已经知道当前使用的是哪种 AI 工具，以及它支持什么接入方式

## 3. 生成 adapter 时必须读取什么

最小读取集合应该是：

1. `local_kb/kb_manifest.yaml`
2. 当前命中的领域入口，例如 `local_kb/domains/<domain>/README.md`
3. 当前工具已有的适配文件，如果已经存在
4. 与当前工具相关的最小实现说明

不要因为要生成 `adapter`，就回头把整个知识库读一遍。

## 4. adapter 必须保留的协议骨架

无论最后生成成什么格式，至少都要保留下面这些行为约束。

### 4.1 固定入口

- 第一动作永远是读取 `local_kb/kb_manifest.yaml`

### 4.2 路由顺序

- 先判断 `retrieve / capture / package_or_governance`
- 再判断命中的 `domain`

### 4.3 读取边界

- 只读取当前最相关的总库或子库入口
- 不默认扩读整个仓库
- 不预设固定文档名单

### 4.4 复用优先

- 先复用已有正式知识
- 再参考相关草稿
- 不平行生成同义新文档

### 4.5 创建确认

- 没命中领域时，不自动创建新领域
- 命中领域但缺少合适条目时，不自动写正式知识
- 必须先请求用户确认

### 4.6 输出约束

输出至少要能稳定覆盖：

- 读取了哪些知识
- 复用了哪些经验
- 当前缺了哪些知识
- 建议回写到哪里

如果是完整闭环任务，尽量还能覆盖：

- `best_entry`
- `digest`
- `capture`
- `suggested_writeback`
- `governance_feedback`

## 5. 不同 AI 工具怎么适配

不要把“适配”理解成只能生成一个 `SKILL.md`。

更稳的做法是先看当前工具支持哪一种载体：

### 5.1 文件型适配

适用于支持工作区指令文件、skill 文件、agent profile 文件的工具。

输出目标通常是：

- 工具原生约定路径下的指令文件

例如：

- `.trae/skills/local-kb-orchestrator/SKILL.md`

### 5.2 Prompt 型适配

适用于没有固定技能目录，但支持长期保存工作区提示词或项目说明的工具。

输出目标通常是：

- 一段可复用的项目级 prompt
- 一份可复制到工具设置页的 instruction

### 5.3 命令型适配

适用于支持命令包装、斜杠命令或脚本入口的工具。

输出目标通常是：

- 一个固定说明文件
- 配套调用 `local_kb/tools/kb_dispatch.py` 的命令入口

### 5.4 回退策略

如果当前 AI 工具既没有稳定文件入口，也没有项目级 instruction 存储位置：

- 至少生成一份 `adapter prompt`
- 并保存为工程内可复用文档

推荐回退位置：

- `local_kb/adapters/<tool>/README.md`

这样即使换工具，也还能继续复用。

## 6. 推荐的生成流程

推荐让 AI 按下面顺序执行：

1. 识别当前 AI 工具支持的适配方式
2. 读取 `local_kb/kb_manifest.yaml`
3. 读取当前工程最相关领域入口
4. 判断当前工具应该生成：
   - `skill file`
   - `workspace instruction`
   - `adapter prompt`
   - `command wrapper`
5. 生成最小适配层
6. 用 3 类问题自测
7. 报告还缺哪些知识和哪些工具能力

推荐最小自测问题：

- `retrieve`：这个工程里某类已知问题怎么排查
- `capture`：请把这次排查沉淀成知识草稿
- `governance`：这个工程的知识库结构还缺什么

## 7. 最小样例

如果你想先看结果大概长什么样，而不是只看规则，先看这两个最小样例：

- `local_kb/adapters/trae/SKILL.example.md`
- `local_kb/adapters/generic-chat-tool/PROJECT_PROMPT.example.md`

它们只演示：

- 同一套协议如何投影到不同载体
- 不演示完整工具细节
- 不复制知识库正文

## 8. 可直接复制给 AI 的二阶段提示词

在第一轮接入完成后，把下面这段话直接贴给 AI。

```text
请基于当前已经接入完成的本地知识库模块，为当前工程生成“当前 AI 工具专属的适配层”。

要求：
1. 先读取 `local_kb/kb_manifest.yaml`，把它当作唯一固定入口；
2. 先识别你当前所处的 AI 工具、IDE 或代理环境，判断它支持哪种适配方式：
   - skill file
   - workspace instruction
   - reusable prompt
   - command wrapper
3. 只读取生成当前适配层所必需的最小知识：
   - `local_kb/kb_manifest.yaml`
   - 当前命中的领域入口
   - 当前工具已有的适配文件（如果存在）
4. 生成的适配层必须保留这套知识库协议的核心约束：
   - 先做 intent routing，再做 domain routing
   - 只做最小化读取
   - 优先复用已有知识
   - 新知识或新领域先请求用户确认，不要自动创建正式知识
   - 输出时明确说明读取了哪些知识、复用了哪些经验、缺了哪些知识、建议回写到哪里
5. 如果当前工具支持原生适配文件，就直接生成到该工具的原生路径；
6. 如果当前工具没有原生适配文件路径，就生成一份项目级 adapter prompt，并保存到工程内可复用的位置；
7. 不要把整个知识库正文复制进适配层，只保留工具需要的最小协议映射；
8. 生成后请再给出最小验证步骤，至少覆盖 retrieve、capture、governance 三类问题。
```

## 9. 对实现者的要求

如果你要把这一步做成对外可复用实现，优先保证下面几件事：

- 适配层永远是派生产物，不是知识库本体
- 工具变化时，尽量不改 `local_kb/` 的稳定协议
- 同一套知识库规则，应能投影到不同 AI 工具
- 工具专属文件尽量薄，不重复承载知识正文
- 生成失败时，至少还能回退到可复制的 prompt 版本

## 10. 最小验收标准

当你说“adapter 已生成完成”时，至少应该满足这 5 条：

1. 当前工具有一个明确可复用的接入载体
2. 这个载体把 `local_kb/kb_manifest.yaml` 设成唯一固定入口
3. 它没有覆盖掉创建确认规则
4. 它没有把整个知识库复制进工具配置里
5. 它附带最小验证步骤

## 11. 和 `SKILL.md` 的关系

如果你当前用的是 `Trae/IDE`，最后的产物很可能是：

- `.trae/skills/local-kb-orchestrator/SKILL.md`

但这只是当前工具的一个投影结果，不是这套模块唯一正确的实现形式。

更高一层应该始终理解为：

- 先有 `local_kb` 协议
- 再按工具生成对应 `adapter`

## 12. 再往下怎么继续整理

如果后面你要和别人一起继续整理这部分，推荐按下面顺序收敛：

1. 先用这份文档统一生成流程
2. 再用 `ADAPTER_SPEC.md` 收敛评审标准
3. 再用 `ADAPTER_SCHEMA.yaml` 收敛结构化字段
4. 最后再针对具体工具补各自的最小实现样例
