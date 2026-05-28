# Demo Quick Test

这份清单用于验证纯知识库模块已经不只可路由，还能演示完整闭环。

## 这份文档负责什么

这份文档负责：

- 给你一组最小可执行命令
- 验证 `route / best-entry / digest / capture` 闭环
- 帮你判断纯模块是否已经能在新工程里跑通

这份文档不负责：

- 解释模块为什么这样设计
- 指导真实工程如何替换 `demo`
- 定义 adapter 的实现标准

## 测试 1：route

```bash
python3 local_kb/tools/kb_dispatch.py route --text "帮我分析 demo 机器人电机不转的问题" --format json
```

预期：

- `domain` 命中 `demo`
- `best_entry` 命中 `local_kb/domains/demo/demo_motor_not_spinning_pattern.md`

## 测试 2：best-entry

```bash
python3 local_kb/tools/kb_dispatch.py best-entry --text "demo 电机不转怎么排查" --format json
```

预期：

- 返回 demo 正式模式条目
- `recommended_action` 包含最小排查步骤

## 测试 3：digest

```bash
python3 local_kb/tools/kb_dispatch.py digest --text "把 demo 电机不转排查整理成最小摘要" --format json
```

预期：

- 返回 `best_entry`
- 返回 `suggested_writeback`
- 返回 demo 领域相关文件

## 测试 4：capture

```bash
python3 local_kb/tools/kb_dispatch.py capture --text "请总结 demo 电机不转这次排查，并写成知识草稿" --format json
```

预期：

- `suggested_writeback.target` 指向 `local_kb/domains/demo/drafts`
- 生成 observation / interpretation / action / verification

## 测试 5：capture 落盘

```bash
python3 local_kb/tools/kb_dispatch.py capture \
  --text "请总结 demo 电机不转这次排查，并写成知识草稿" \
  --save-draft \
  --confirm \
  --format json
```

预期：

- 在 `local_kb/domains/demo/drafts/` 生成一份草稿
- 纯模块完整演示从命中正式知识到落草稿的闭环
