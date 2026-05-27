# Pure KB Module Architecture

这份文档回答的是：

- 这套模块到底在公开什么
- 它内部是怎么工作的
- 为什么它不是普通的 memory/RAG 包装
- 迁移到新工程时，哪些部分应该保持稳定

## 1. Core Object

这套模块公开的核心对象不是一份知识内容，而是 3 层能力：

1. `method`
2. `skill orchestration`
3. `protocol framework`

它的目标不是让所有人共用一份知识，而是让每个人都能在自己的工作区里，用同一套协议组织自己的本地知识系统。

## 2. Design Goal

这套模块要解决的不是“给 AI 多喂点上下文”。

它要解决的是：

- 新对话如何恢复主线，而不是像失忆一样重来
- 经验如何沉淀为本地资产，而不是停留在聊天记录
- 知识如何被持续治理，而不是只会无限追加
- 人类与 AI 如何共同维护一套长期可演化的知识结构

## 3. Working Loop

模块内部最关键的是一个稳定闭环：

1. `route`
   - 先读 `manifest`
   - 先判定 `intent`
   - 再判定 `domain`
2. `best_entry`
   - 告诉 AI 当前最该先读哪条知识
3. `digest`
   - 提供最小但足够的上下文摘要
4. `capture`
   - 把稳定结论整理成草稿
5. `suggested_writeback`
   - 告诉系统这次最适合回写到哪里
6. `governance_feedback`
   - 指出当前缺口是内容、结构、入口还是路由

这也是为什么它不是“单次回答辅助工具”，而是“可持续自我优化的知识协作循环”。

## 4. Component Layers

### 4.1 Knowledge Layer

知识主存放在 `Markdown` 中。

核心形式是：

- `frontmatter`
- `wikilink`
- `MOC`
- 正式知识与草稿分层

这里的原则是：

- 知识主存对人类可读
- 对 `Obsidian` 友好
- 对脚本可转译

### 4.2 Routing Layer

路由层的入口固定为：

- `local_kb/kb_manifest.yaml`

它负责：

- `intent routing`
- `domain routing`
- 默认读取顺序
- 创建规则
- 回写规则

这里稳定的不是“固定要读哪些文档”，而是“如何决定这次应该先读什么”。

### 4.3 Protocol Layer

协议层负责定义系统行为边界，例如：

- 新知识先确认创建
- `capture` 先生成草稿
- 治理问题优先回写知识库自身
- 主线恢复要区分 `session goal / mission anchor / stage focus`

这一层是系统真正可迁移的部分。

### 4.4 Adapter Layer

适配层负责把协议接到具体代理或 IDE。

当前示例是：

- `.trae/skills/`

但这层不是本体。

如果未来换代理，最稳的仍然是复用：

- `local_kb/`
- `manifest`
- 提示词
- 路由与回写协议

## 5. Why It Is Not Just RAG

这套模块和常见的 RAG 或 memory 包装有几个关键区别：

### 5.1 它不追求全量召回

它优先做：

- 最小化读取
- 最优入口命中
- 少量相关知识复用

而不是每次都大范围展开。

### 5.2 它不把“记住更多”当成终点

它更关注：

- 知识怎么被组织
- 知识怎么被回写
- 知识怎么被治理

所以重点是结构，而不是上下文堆积。

### 5.3 它把人类保留在闭环里

这里默认不允许：

- 自动创建正式知识
- 跳过确认直接落正式结构

因为最终目标不是替人决定知识结构，而是让人和 AI 共建知识结构。

## 6. Current Portable Boundary

当前这版可迁移边界大致是：

- `local_kb/`
- `.trae/skills/`
- `README.md`
- `QUICKSTART.md`
- `ARCHITECTURE.md`
- `examples/demo_workspace/`

默认不迁移的内容包括：

- 私有领域知识
- 私有案例
- 历史调试记录
- 私有草稿

## 7. Demo Strategy

当前纯模块自带一个最小 `demo` 域。

它不是为了模拟真实业务，而是为了验证：

- 路由是否正确
- 正式条目是否可命中
- 摘要是否可生成
- 草稿是否可落盘
- 回写目标是否合理

也就是说，demo 的作用是证明“这套机制能跑”，而不是证明“这套知识内容够丰富”。

## 8. Migration Path

把它接入新工程时，推荐顺序是：

1. 先保留纯模块原样
2. 先跑通 demo
3. 再增加你自己的领域入口
4. 再把 demo 替换成你自己的真实知识结构
5. 最后再根据你的工程语义调整 `kb_manifest.yaml`

## 9. Current Limitation

当前这版已经足够演示闭环，但仍然不是完整公开框架仓库。

当前还缺：

- 更完整的 demo 领域包
- 更多领域的可公开示例
- 更系统的接入文档

所以现在更适合把它理解成：

- 一个可迁移核心
- 一个最小 demo
- 一个公开框架雏形
