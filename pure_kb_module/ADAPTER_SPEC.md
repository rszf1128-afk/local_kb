# Adapter Spec

这份文档是给人看的 `adapter contract`。

## 这份文档负责什么

这份文档负责：

- 给实现者、协作者、reviewer 一份统一的文字版标准
- 说明 adapter 的边界、能力要求、禁止事项和验收清单
- 帮大家评审“这个实现是不是还在同一套协议里”

这份文档不负责：

- 充当第一阶段或第二阶段操作入口
- 直接生成某个工具的最终文件
- 代替结构化 `schema`

它的目标不是教人怎么写某个具体 `SKILL.md`，而是先把一件更高层的事说清楚：

- 不同 AI 工具都可以接入同一套 `local_kb` 协议
- 工具不同，载体不同
- 但协议骨架不应该变

如果说：

- `GENERATE_ADAPTER_FOR_YOUR_AI.md` 是使用流程
- `ADAPTER_SCHEMA.yaml` 是机器可读约束

那么这份文档就是：

- 给实现者、协作者、reviewer 看的文字版标准

可以把这 4 份文档理解成固定分工：

- `START_WITH_AI.md`：第一阶段入口
- `GENERATE_ADAPTER_FOR_YOUR_AI.md`：第二阶段流程
- `ADAPTER_SPEC.md`：文字版 contract
- `ADAPTER_SCHEMA.yaml`：结构化 contract

## 1. 目标

`adapter` 层的唯一职责是：

- 把 `local_kb` 的稳定协议，投影成当前 AI 工具可执行、可复用、可验证的接入形式

它不负责：

- 取代知识库本体
- 复制知识正文
- 发明新的知识治理规则

所以设计上必须满足：

1. 协议在 `local_kb/`
2. 工具差异在 `adapter`
3. 适配层是薄层，不是第二套知识库

## 2. 术语

### 2.1 Protocol

这里的 `protocol` 指 `local_kb` 中已经稳定的工作方式，包括：

- `kb_manifest.yaml` 作为唯一固定入口
- `intent routing`
- `domain routing`
- `minimal read`
- `reuse first`
- `confirmation before creation`
- `suggested_writeback`

### 2.2 Adapter

`adapter` 指某个 AI 工具专属的投影层。

典型形式可以是：

- `skill file`
- `workspace instruction`
- `project prompt`
- `command wrapper`

### 2.3 Carrier

`carrier` 指 `adapter` 最终落地的载体。

例如：

- `.trae/skills/local-kb-orchestrator/SKILL.md`
- 某个工具的项目级 instruction
- `local_kb/adapters/<tool>/README.md`

### 2.4 Projection

`projection` 指把同一套协议映射到不同工具上的动作。

重点不是“翻译文字”，而是：

- 保持协议行为不变
- 只替换工具接入方式

## 3. 分层边界

推荐按下面 4 层理解：

1. `knowledge layer`
   - `local_kb/` 中的知识正文、规则、模板、领域入口
2. `protocol layer`
   - `kb_manifest.yaml` 与通用治理规则
3. `adapter layer`
   - 面向具体 AI 工具的投影文件或指令
4. `runtime layer`
   - 实际对话、脚本调用、工具执行环境

设计要求是：

- 上层可以变
- 下层尽量稳

更具体地说：

- 换工具时，应优先只改 `adapter layer`
- 不要先回头改 `knowledge layer`

## 4. 最小必须能力

任何实现如果自称支持这套 `adapter spec`，至少要保留下面 6 类能力。

### 4.1 固定入口能力

必须保证第一固定入口是：

- `local_kb/kb_manifest.yaml`

不允许把其他文档硬编码成长期第一入口，除非它本身已经被 `manifest` 显式指定。

### 4.2 路由能力

必须保留以下顺序：

1. 先判断 `intent`
2. 再判断 `domain`
3. 再决定最小读取范围

其中 `intent` 至少应覆盖：

- `retrieve`
- `capture`
- `package_or_governance`

### 4.3 最小读取能力

必须保证：

- 不默认扩读整个仓库
- 不因为曾经读过某些文档，就永久固定优先它们
- 只读取当前任务最相关入口

### 4.4 复用能力

必须保证：

- 优先复用已有正式知识
- 再参考已有草稿
- 不平行制造同义知识文件

### 4.5 创建确认能力

必须保留：

- 新领域先确认
- 新正式知识先确认
- 如果只是沉淀旧对话，优先产出草稿，不直接写正式知识

### 4.6 输出可审计能力

必须能让用户看到至少这 4 类信息：

- 读取了哪些知识
- 复用了哪些经验
- 当前缺了哪些知识
- 建议回写到哪里

如果工具能力允许，建议再补：

- `best_entry`
- `digest`
- `capture`
- `suggested_writeback`
- `governance_feedback`

## 5. Carrier 类型

实现者应先判断当前工具最适合哪种 `carrier`。

### 5.1 Native File Carrier

适用于工具原生支持项目文件加载的情况。

例如：

- `skill`
- `agent profile`
- `workspace rule file`

优点：

- 可以直接随工程迁移
- 易于版本管理

风险：

- 容易把工具细节写进本体规则

### 5.2 Workspace Instruction Carrier

适用于工具支持工作区级 instruction，但没有固定文件目录的情况。

优点：

- 接入阻力低

风险：

- 不一定能跟随仓库迁移

### 5.3 Prompt Carrier

适用于工具没有稳定文件入口，但支持长期保存可复用 prompt。

优点：

- 最通用

风险：

- 漂移风险更高
- 更依赖人工复制

### 5.4 Command Carrier

适用于工具更偏命令式编排。

常见形式：

- slash command
- wrapper script
- task entry

优点：

- 能与 `kb_dispatch.py` 更直接对齐

风险：

- 不一定覆盖完整对话行为

## 6. 推荐生成流程

标准生成流程建议分成 3 段。

### 6.1 Inspect

生成前先识别：

- 当前工具是什么
- 当前工具支持什么 `carrier`
- 当前工程命中了哪个知识领域
- 当前是否已经存在旧 adapter

### 6.2 Project

然后把协议骨架投影过去，只保留最小内容：

- 固定入口
- 路由顺序
- 读取边界
- 创建确认
- 输出约束

### 6.3 Verify

最后用最小问题集验证：

- `retrieve`
- `capture`
- `governance`

这一步不是可选项。

如果没做验证，就不能说“adapter 已经生成完成”。

## 7. 生成结果至少应包含什么

无论最后生成成哪个文件或哪个设置项，结果至少应能表达：

- 当前工具名称
- 当前 carrier 类型
- 固定入口路径
- 必须执行的路由顺序
- 最小读取边界
- 创建确认规则
- 输出要求
- fallback 策略
- 最小验证步骤

## 8. Fallback 规则

如果当前工具不支持理想的 `carrier`，必须有回退策略。

推荐回退优先级：

1. 原生文件载体
2. 工作区 instruction
3. 可复用 prompt
4. 工程内保存的 adapter 文档

最低要求是：

- 即使工具不支持自动加载，也要留下一个可复制、可保存、可复用的工程内结果

推荐位置：

- `local_kb/adapters/<tool>/README.md`

## 9. 禁止事项

下面这些做法应视为不符合 spec。

### 9.1 把知识库正文塞进 adapter

不应该把大量 `pattern / case / principle` 正文复制到工具指令文件里。

### 9.2 绕过 `manifest`

不应该把某个领域文件永久写死成第一入口。

### 9.3 绕过创建确认

不应该因为工具支持自动写文件，就跳过用户确认。

### 9.4 混淆协议层和工具层

不应该把工具的专属限制，反向写进知识库本体规则里。

## 10. 最小验收清单

评审一个 adapter 实现时，至少检查这 8 条：

1. 是否把 `local_kb/kb_manifest.yaml` 作为唯一固定入口
2. 是否先判断 `intent` 再判断 `domain`
3. 是否只做最小化读取
4. 是否优先复用已有知识
5. 是否保留创建确认规则
6. 是否显式给出读取、复用、缺口、回写建议
7. 是否有 fallback 方案
8. 是否附带最小验证步骤

## 11. Trae 示例

如果当前工具是 `Trae`，一个符合 spec 的结果通常会表现为：

- 产出 `.trae/skills/local-kb-orchestrator/SKILL.md`
- 文件中不复制知识库正文
- 文件只保留协议映射和工具使用边界
- 文件把 `kb_manifest.yaml` 作为唯一固定入口

但这只是一个示例，不应被理解成标准只能这样实现。

本模块中的最小样例位置建议为：

- `local_kb/adapters/trae/SKILL.example.md`
- `local_kb/adapters/generic-chat-tool/PROJECT_PROMPT.example.md`

## 12. 和其他文档的关系

- `START_WITH_AI.md`
  - 第一阶段，先接入
- `GENERATE_ADAPTER_FOR_YOUR_AI.md`
  - 第二阶段，教你怎么生成 adapter
- `ADAPTER_SPEC.md`
  - 给实现者和评审者看的文字版 contract
- `ADAPTER_SCHEMA.yaml`
  - 给 AI、脚本或工具实现读取的结构化 contract

如果后面你们要一起继续整理，建议优先围绕这 4 个文件收敛，而不是继续分散加说明页。
