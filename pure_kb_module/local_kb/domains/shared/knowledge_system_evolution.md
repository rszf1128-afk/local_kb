---
title: Knowledge System Evolution
type: note
domain: shared
status: active
tags:
  - knowledge-base
  - shared
  - governance
  - obsidian
  - ai
---

# 知识系统演化笔记

这份笔记用于沉淀“这套本地知识库是怎么搭起来的、为什么这么搭、后面该怎么优化”。

它不是某个具体技术域的业务知识，而是这套知识系统自己的元知识。后续如果要优化 `prompt/提示词`、`skill`、`manifest` 路由、`Obsidian` 结构、`capture/沉淀` 流程，优先先读这页。

## 定位

- 面向对象是“知识系统本身”，不是 `PX4/QGC/embedded` 的业务内容
- 承载本地知识库的架构原则、演化历史、治理规则和优化方向
- 作为后续修改知识库时的第一入口，避免再次依赖聊天上下文回忆

## 当前系统边界

这套系统当前由几层组成：

1. `local_kb/总库`
   - 负责 `intent routing/意图路由`
   - 负责 `domain routing/领域路由`
   - 负责 `create-from-confirmation/确认后创建`
2. `domains/*/领域入口`
   - 负责放置长期通用知识
   - 负责连接 `MOC/内容地图`
3. `usv_sim_kb/子知识库`
   - 负责更细的 `case/pattern/checklist`
   - 已支持 `best-entry/最优经验条目`
4. `.trae/skills`
   - 负责把 AI 装配到总库或子库入口

## 已确认的关键设计决策

### 1. `Markdown` 主存，脚本只是转译层

- 知识主存放在 `Markdown`
- `Python` 脚本负责路由、提取、草稿生成和结构化投影
- 这样做是为了同时兼容人类维护、`Obsidian` 浏览和 AI 消费

**结构化元信息**

- `layer`: `governance`
- `symptom`: `AI` 对知识库的使用越来越依赖脚本内部逻辑，导致人类难以维护、`Obsidian` 难以直接浏览或审阅
- `evidence`:
  - `Markdown` 能直接被人编辑，也能被 `Obsidian` 图谱使用
  - 脚本只做路由和投影时，知识主存不会被工具链绑死
- `recommended_action`:
  - 长期知识优先写在 `Markdown`
  - 脚本只负责路由、提取、结构化投影和草稿生成
- `portability`: `high`
- `confidence`: `verified`

### 2. 物理目录不等于语义知识树

- 目录树负责落盘、打包和 `git` 管理
- 语义关系通过 `wikilink`、`MOC`、`tags` 表达
- 因此 `usv_sim_kb` 即使物理上与 `local_kb` 并列，语义上仍属于更长链路的一部分
- 典型理解方式是：`工程知识 -> 自动控制 -> PX4 -> 仿真 -> USV`

**结构化元信息**

- `layer`: `graph`
- `symptom`: 想把所有知识关系都塞进文件夹层级，导致跨主题知识难以表达，目录一改就影响整体理解
- `evidence`:
  - `PX4/QGC/embedded` 与方法论知识存在交织关系
  - `usv_sim_kb` 的物理位置不等于它的语义父子关系
- `recommended_action`:
  - 把目录用于落盘和仓库治理
  - 把语义关系交给 `wikilink`、`MOC` 和 `tags`
- `portability`: `high`
- `confidence`: `verified`

### 3. 先路由，再最小化读取

- AI 不应每次全量读库
- 总库先用 `manifest` 判断 `intent/意图` 和 `domain/领域`
- 然后只读取最相关入口文件，尽量降低 `token` 开销

**结构化元信息**

- `layer`: `routing`
- `symptom`: 每次都全量读取知识库，导致 `token` 开销高、启动慢，而且 AI 容易把低相关内容也带进来
- `evidence`:
  - 总库 `manifest` 已能先做 `intent routing/意图路由`
  - 先命中领域后再读入口文件，输出更稳定
- `recommended_action`:
  - 先走 `manifest` 路由
  - 只读最相关入口，再按需要展开
- `portability`: `high`
- `confidence`: `verified`

### 4. 新知识不能自动进入正式库

- 当前采用 `create-from-confirmation/确认后创建`
- 如果现有领域不匹配，或现有笔记装不下新知识，必须先问用户
- 正式知识和草稿知识要分层，避免“对话噪声”直接污染知识库

**结构化元信息**

- `layer`: `governance`
- `symptom`: 遇到新主题时直接写入正式知识，导致知识库被临时结论、对话噪声或错误分类污染
- `evidence`:
  - 新知识在最初往往还没有稳定分类
  - 草稿与正式知识分层后，更适合人工审阅和并入
- `recommended_action`:
  - 新知识先问用户是否创建
  - 确认后优先生成草稿，不直接写正式知识
- `portability`: `high`
- `confidence`: `verified`

### 5. 沉淀闭环优先于一次性回答

- 用户输入“总结、复盘、沉淀、记录、回写、写进知识库”等词时，应自动进入 `capture/沉淀`
- 目标不是只回答问题，而是把可复用经验沉淀为后续可检索资产

**结构化元信息**

- `layer`: `capture`
- `symptom`: 对话解决了问题，但经验没有沉淀，下一次又要重新解释和重走排查链路
- `evidence`:
  - 仅回答问题不会自动形成可复用资产
  - 用户明确要求在“总结/复盘/写进知识库”时自动进入沉淀模式
- `recommended_action`:
  - 检测沉淀关键词后自动整理 `observation/interpretation/action`
  - 输出回写建议或草稿
- `portability`: `high`
- `confidence`: `verified`

### 6. 子库可做更强结构化

- 总库目前偏重路由和治理
- 子库可以继续做结构化经验抽取，例如 `best-entry`
- 这允许 AI 直接消费 `layer/symptom/evidence/recommended_action`

**结构化元信息**

- `layer`: `structure`
- `symptom`: 总库只会给文件名或段落，AI 还需要自己二次提炼，导致高频问题复用效率不够高
- `evidence`:
  - `usv_sim_kb` 中结构化经验条目已支持 `best-entry`
  - 结构化字段能直接提供 `symptom/evidence/recommended_action`
- `recommended_action`:
  - 总库保留轻量路由能力
  - 高频治理问题逐步补结构化元信息并优先命中
- `portability`: `medium`
- `confidence`: `working`

### 7. 治理层应输出“知识为什么还不够好”

- 治理层不应只给 `suggested_writeback/建议回写位置`
- 还应说明这次问题更像：
  - `content/内容缺口`
  - `structure/结构失衡`
  - `entrypoint/入口不足`
  - `routing/路由不足`
- 并给出建议动作：
  - `patch/补丁式增强`
  - `split/拆分节点`
  - `link/补入口与链接`
  - `promote/提升为正式节点`

**结构化元信息**

- `layer`: `governance`
- `symptom`: AI 虽然能命中知识或给出回写位置，但不知道这次问题究竟是缺内容、缺结构、缺入口还是缺路由，导致知识库难以真正自我优化
- `evidence`:
  - 只给回写目标时，无法区分应补正文、拆节点还是补图谱入口
  - 单条记忆持续追加会让知识越来越长，反而降低后续命中质量
- `recommended_action`:
  - 在治理输出中增加 `governance_feedback`
  - 明确输出 `gap/action/reason/target/signals`
- `portability`: `high`
- `confidence`: `working`

## 这次搭建过程中形成的经验

### 从单一主题升级到任意知识域

- 起点是 `PX4 USV 仿真`
- 随后明确升级为面向任意知识域的总库
- `PX4/QGC/embedded` 只是种子领域，不是系统边界

### 从目录思维升级到图谱思维

- 只靠目录很难表达交织关系
- 引入 `Obsidian` 风格的 `MOC + wikilink + frontmatter`
- 这样才能让知识像“思想宫殿”而不是僵硬文件夹

### 从“查文件”升级到“给经验”

- 早期脚本主要返回该读哪些文件
- 后续在 `usv_sim_kb` 中加入结构化经验条目和 `best-entry`
- 这证明后续可以继续把“文件级命中”提升为“经验级命中”

### 总库和子库职责要分清

- 总库更适合做：入口、治理、规则、确认创建
- 子库更适合做：具体案例、排障分层、参数经验、结构化条目
- 两者不能互相替代，但要通过入口文件和图谱连起来

### 当前阶段先完善体系，再细化子协议

- 当前阶段最重要的不是继续细化更多治理子协议
- 而是先把现有体系闭环跑通，并把关键对话结论持续沉淀回知识库
- 目标是让后续新对话更多依赖知识库上下文，而不是依赖单次会话记忆
- 等体系连续性与实际效果稳定后，再继续细化更底层的人类判断点协议或其它子协议

### 长会话不应依赖单次上下文无限延长

- 当单次对话已经很长时，继续在同一会话中叠加上下文的收益会下降
- 更优策略是先把当前稳定结论 capture 到知识库，再在新对话中通过治理入口恢复主线
- 验证目标不是“复制整段旧对话”，而是让新对话优先复用已沉淀的稳定结论与草稿

### 新对话续接不应只恢复结构层，还要恢复使命层

- 新对话如果只恢复 `route/best_entry/digest/capture` 这些结构层能力，而没有恢复项目最高层目标，仍然会在方向上逐步收窄
- 这套系统的最高目标不是做某个行业知识库样例，也不是公开私有知识内容，而是公开一套面向所有人可复用的方法、`skill/技能装配` 与 `protocol framework/协议框架`
- 因此新对话续接时，除了恢复当前阶段、当前闭环和当前治理规则，还应恢复“为什么要做这套系统、最终面向谁、什么内容公开、什么内容本地化”
- `local_cognition_protocol.md` 应被视为恢复使命层的优先入口，而不只是一般治理文档

**结构化元信息**

- `layer`: `governance`
- `symptom`: 新对话已经恢复了体系结构、阶段清单和接口闭环，但没有完整恢复项目最高层目标，导致主线容易从“面向全人类的公开框架”收窄成“某个可迁移的知识库工具”
- `evidence`:
  - `kb_bootstrap_prompt.md` 更偏运行规则和最小化读取，天然更容易先恢复结构层
  - 若缺少使命层锚点，新对话容易先抓“体系怎么做”，再弱化“为什么做、为谁做”
- `recommended_action`:
  - 新对话续接时同时恢复结构层与使命层
  - 将 `local_cognition_protocol.md` 作为恢复项目最高层目标的优先入口之一
  - 把“公开方法、技能装配与协议框架，而非公开私有知识内容”的定位沉淀为稳定治理经验
- `portability`: `high`
- `confidence`: `verified`

### 提示词应固定路由原则，而不是固定文档名单

- 总提示词应固定的是 `manifest`、意图判定、领域路由、最小化读取和确认后创建
- 总提示词不应把某几个文档写成长期固定入口，否则容易把系统锁死在当前治理材料上
- 已命中具体领域后，应优先读取该领域入口、该领域笔记和该领域 drafts，不要过早扩展到整仓工程噪声
- 只有当现有领域知识确实不足，且用户明确需要代码级排查时，才扩展到更大范围的代码和工程检索
- 如果用户讨论的是总提示词、`manifest`、路由原则、固定文档名单或最小化读取，这类请求本身也属于知识系统演化规则，`suggested_writeback` 应优先回到本页，而不是被 `workflow/确认创建` 一类边角关键词抢走
- 只有当问题真正聚焦在试跑、落盘、安全边界或确认后创建流程时，才应把回写目标落到 `kb_confirmation_workflow.md`

**结构化元信息**

- `layer`: `governance`
- `symptom`: 领域型 `capture` 已经命中正确知识域，但后续检索范围继续扩展到整仓代码改动与工程噪声，导致阅读面过宽、结论不聚焦
- `evidence`:
  - 命中具体领域后，领域入口、领域笔记和领域 `drafts` 已经足够支撑第一轮沉淀判断
  - 无关的 `git status`、整仓搜索和宽泛代码符号检索会引入噪声，降低沉淀质量
  - 提示词治理请求若被误回写到 `kb_confirmation_workflow.md`，会把“知识系统演化规则”和“确认后创建流程”混在一起，降低后续命中稳定性
- `recommended_action`:
  - 总提示词只固定路由原则，不固定长期文档名单
  - 命中具体领域后，先限制在该领域知识与少量直接命中资料内检索
  - 仅在知识不足且用户明确要求代码级排查时，再扩展到工程搜索
  - 对提示词、路由原则与最小化读取的治理请求，优先把 `suggested_writeback` 固定到本页
- `portability`: `high`
- `confidence`: `verified`

## 后续优化时的优先检查项

1. 路由层
   - `kb_manifest.yaml` 的关键词是否过宽或过窄
   - 某类请求是否总被误路由到 `shared`
2. 图谱层
   - 新知识是否有 `wikilink`
   - 是否需要新增 `MOC`
3. 沉淀层
   - 是否有重复经验散落在多个草稿里
   - 是否需要把高频经验升级为正式笔记
4. 结构化层
   - 是否值得给某类高频问题补 `structured metadata/结构化元信息`
   - 是否需要在更多子库复用 `best-entry`
5. 治理层
   - 是否仍保持“先确认、后创建”
   - 使用文档和提示词是否与当前能力一致

## 修改知识库时的建议顺序

1. 先判断这是 `retrieve/查用`、`capture/沉淀` 还是 `governance/治理`
2. 如果是优化知识库本身，先读这页和 [[../../MOCs/03_Capture_Governance_Graph|沉淀与治理图谱]]
3. 再决定改的是：
   - `manifest/路由`
   - `MOC/图谱`
   - `skill`
   - `脚本`
   - `经验文档`
4. 如果涉及新主题，仍然先走确认创建

**结构化元信息**

- `layer`: `workflow`
- `symptom`: 修改知识库时直接上手改很多位置，最后难以判断问题出在 `manifest`、图谱、脚本还是经验文档
- `evidence`:
  - 路由层、图谱层、结构化层和治理层职责不同
  - 一次只改一层时更容易验证效果
- `recommended_action`:
  - 先判断当前问题属于哪一层
  - 每轮优先只改一个层面的关键点，再验证
- `portability`: `high`
- `confidence`: `verified`

## 相关入口

- [[README|shared/通用领域入口]]
- [[../../README|总库入口]]
- [[../../kb_graph_architecture|知识图谱架构说明]]
- [[../../kb_obsidian_conventions|Obsidian 编写规范]]
- [[directory_structure_strategy|目录分层方案 v2]]
- [[local_cognition_protocol|本地认知协作协议]]
- [[open_source_framework_strategy|开源框架分层方案]]
- [[open_source_repo_skeleton|公开版仓库骨架草案]]
- [[../../kb_creation_policy|新知识创建策略]]
- [[../../MOCs/01_Domain_Graph|领域图谱]]
- [[../../MOCs/03_Capture_Governance_Graph|沉淀与治理图谱]]
