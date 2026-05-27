# Adapters Directory

这个目录专门放“工具专属投影层”的最小样例或回退载体。

## 这个目录负责什么

这个目录负责：

- 演示同一套 `local_kb` 协议如何投影到不同 AI 工具
- 放最小可参考的 `skill / prompt / instruction` 样例
- 在没有工具原生目录时，提供工程内可保存的回退位置

这个目录不负责：

- 承载知识库本体
- 复制大量正式知识正文
- 取代 `kb_manifest.yaml` 的总路由角色

## 当前包含什么

- `trae/`
  - `SKILL.example.md`
  - 演示文件型 carrier 的最小样例
- `generic-chat-tool/`
  - `PROJECT_PROMPT.example.md`
  - 演示 prompt 型 carrier 的最小样例

## 怎么理解这些样例

这些文件的作用是：

- 看看结果大概长什么样
- 对齐 adapter 应该保留哪些协议骨架
- 帮助实现者开始做自己的工具适配

这些文件的作用不是：

- 直接替代真实工程里的正式 adapter
- 原样复制后就当作最终实现

## 使用顺序

推荐顺序是：

1. 先看根目录 `START_WITH_AI.md`
2. 完成第一轮最小接入
3. 再看 `GENERATE_ADAPTER_FOR_YOUR_AI.md`
4. 再参考这里的最小样例

## 当前边界

这里优先放：

- 最小样例
- 最小回退载体
- 工具专属说明入口

如果未来某个工具需要更完整实现，建议仍然保持：

- 知识库本体在 `local_kb/`
- 工具差异只在 `adapters/`
