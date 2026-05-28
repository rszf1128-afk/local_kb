# Pure KB Module Quickstart

这是把 `pure_kb_module/` 拷到新工程后，最快跑通的一条路径。

## 这份文档负责什么

这份文档负责：

- 用分步骤方式带你跑通接入
- 告诉你怎么打开工程、初始化 AI、试跑 demo
- 给你一个从复制模块到最小验证的手动路径

这份文档不负责：

- 解释完整架构设计
- 详细说明真实工程替换哪些部分
- 定义 adapter 的实现标准

如果你只想直接复制粘贴给 AI，而不想先读分步骤说明，先看：

- `START_WITH_AI.md`

## 1. 拷贝

把整个 `pure_kb_module/` 目录复制到你的新工程里。

建议优先保留：

- `local_kb/`
- `README.md`
- `START_WITH_AI.md`
- `QUICKSTART.md`
- `ARCHITECTURE.md`
- `MODULE_PLAN.md`
- `examples/demo_workspace/`

可选保留：

- `.trae/skills/`

说明：

- `skill` 现在不是前置必带项
- 如果当前环境需要，可以在第一轮接入后再生成或再调整

## 2. 打开

把新工程目录作为工作区根目录打开。

不要只单独打开 `local_kb/` 子目录。

## 3. 初始化 AI

推荐优先做法：

- 直接把 `START_WITH_AI.md` 里的首贴提示词贴给 AI

如果你仍然想手动初始化，再使用：

- `local_kb/kb_bootstrap_prompt.md`

或执行：

```bash
python3 local_kb/tools/kb_dispatch.py bootstrap-prompt
```

如果你想先理解模块为什么这样组织，再开始跑 demo，先看：

- `ARCHITECTURE.md`

如果你已经准备把 demo 替换成真实工程知识，再看：

- `INTEGRATE_INTO_YOUR_PROJECT.md`

如果第一轮接入完成后，你还想让 AI 自动生成当前工具专属适配层，再看：

- `GENERATE_ADAPTER_FOR_YOUR_AI.md`

## 4. 先跑 demo

优先按下面顺序测试：

```bash
python3 local_kb/tools/kb_dispatch.py route --text "帮我分析 demo 机器人电机不转的问题" --format json
python3 local_kb/tools/kb_dispatch.py best-entry --text "demo 电机不转怎么排查" --format json
python3 local_kb/tools/kb_dispatch.py digest --text "把 demo 电机不转排查整理成最小摘要" --format json
python3 local_kb/tools/kb_dispatch.py capture --text "请总结 demo 电机不转这次排查，并写成知识草稿" --format json
```

更完整的测试清单见：

- `examples/demo_workspace/DEMO_QUICKTEST.md`

## 5. 预期结果

- `route` 命中 `demo`
- `best_entry` 命中 `local_kb/domains/demo/demo_motor_not_spinning_pattern.md`
- `digest` 返回 demo 条目和回写建议
- `capture` 返回指向 `local_kb/domains/demo/drafts/` 的草稿回写位置

## 6. 再替换成你的真实知识

当 demo 跑通后，再做这三步：

1. 保留 `local_kb/` 总库
2. 用你的真实领域入口替换或补充 `demo`
3. 再按你的工程语义更新 `kb_manifest.yaml`

## 7. 当前边界

这份模块只负责：

- 路由
- 主线恢复
- 最小化读取
- 草稿沉淀
- 回写建议

它不自带你的真实私有知识。
