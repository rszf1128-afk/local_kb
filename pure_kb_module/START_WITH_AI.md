# Start With AI

如果你不想先读一堆文档，直接用这个。

## 这份文档负责什么

这份文档只负责第一阶段：

- 把模块复制到你的工程里
- 把首贴提示词直接交给 AI
- 让 AI 完成第一轮最小接入

这份文档不负责：

- 详细解释整体架构
- 展开分步骤手动接入说明
- 生成当前工具专属 adapter

做法只有两步：

1. 把 `pure_kb_module/` 复制到你的新工程根目录
2. 把下面这段话直接贴给 AI

## 复制给 AI 的首贴提示词

```text
请把当前工程接入这套本地知识库模块。

要求：
1. 先读取 `local_kb/kb_manifest.yaml`，把它当作唯一固定入口；
2. 不要先让我阅读很多文档，优先直接给出你要执行的最小步骤；
3. 先判断当前工程属于哪个已有领域；如果没有合适领域，只先创建领域入口草稿，不要直接写正式知识；
4. 帮我完成第一轮最小接入：
   - 检查当前工程目录结构
   - 识别最合适的领域入口
   - 必要时调整 `local_kb/kb_manifest.yaml` 的领域路由
   - 生成或补齐 `local_kb/domains/<domain>/README.md`
   - 给出最小测试步骤
5. 如果涉及新知识或新领域，先请求我确认，不要自动创建正式知识；
6. 如果当前环境需要 skill 适配层，再基于现在的知识库状态生成 `.trae/skills/local-kb-orchestrator/SKILL.md`，否则先不要把 skill 当作前置条件；
7. 输出时请明确说明：
   - 你读取了哪些知识
   - 你复用了哪些经验
   - 当前还缺哪些知识
   - 建议下一步回写到哪里
```

## 接入完成后，再生成当前工具专属 adapter

如果第一轮接入已经完成，并且你想让 AI 再自动生成当前工程专属的工具适配层，再看：

- `GENERATE_ADAPTER_FOR_YOUR_AI.md`

它对应的是第二阶段：

- 先接入
- 再按当前 AI 工具生成 `skill / instruction / prompt / command wrapper`

## 预期效果

贴完这段话后，AI 应该先做这些事：

- 读取 `local_kb/kb_manifest.yaml`
- 判断当前工程是否已经有合适领域
- 给出第一轮最小接入动作
- 在需要时再生成或建议生成 `skill`

## 什么时候再看别的文档

只有在你需要更细信息时，再按需看：

- `QUICKSTART.md`
- `ARCHITECTURE.md`
- `INTEGRATE_INTO_YOUR_PROJECT.md`
- `local_kb/kb_obsidian_conventions.md`

## 核心原则

第一入口应该是：

- `copy`
- `paste`
- `let AI adapt`

而不是先学习完整文档体系。
