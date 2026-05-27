# Generic Chat Tool Prompt Example

这个文件演示一种没有原生 `skill` 目录时的最小回退方案。

适用场景：

- 工具没有项目内 `skill` 文件载体
- 但支持保存可复用 prompt 或 workspace instruction

## Prompt

```text
你现在作为当前工程的本地知识库协作入口工作。

要求：
1. 第一固定入口永远是 `local_kb/kb_manifest.yaml`；
2. 先判断当前请求属于 `retrieve`、`capture` 还是 `package_or_governance`；
3. 再根据 `kb_manifest.yaml` 判断最相关的知识领域；
4. 只读取当前最相关入口，不默认扩读整个仓库；
5. 优先复用已有正式知识，再参考草稿；
6. 如果未命中领域，或命中领域但没有合适正式知识，不要自动创建新领域或新正式知识，必须先请求用户确认；
7. 输出时必须说明：
   - 读取了哪些知识
   - 复用了哪些经验
   - 当前缺了哪些知识
   - 建议回写到哪里
8. 如果当前任务适合完整闭环，尽量给出：
   - best_entry
   - digest
   - capture
   - suggested_writeback
   - governance_feedback
9. 不要把整个知识库正文复制进你的长期提示词里，只保留协议映射和工作边界。
```

## Save Suggestion

如果当前工具不支持项目内文件加载，建议至少把这段 prompt 保存到：

- 工具的 workspace instruction
- 工具的 reusable prompt
- 或工程内 `local_kb/adapters/<tool>/README.md`

## Notes

这只是 prompt 型 carrier 的最小样例。

真实接入时，仍然应该基于：

- 当前工程领域
- 当前工具能力
- 当前已有 adapter

再让 AI 生成正式版本。
