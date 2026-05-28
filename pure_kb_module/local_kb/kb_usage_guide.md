# 本地知识库使用办法

## 1. 目的

这份文档面向维护者。

目标是说明：

- 这套系统怎么接入
- 平时怎么用
- 新知识怎么创建
- 常用命令有哪些

## 2. 最小接入条件

确保下面文件存在：

- `local_kb/kb_manifest.yaml`
- `local_kb/kb_bootstrap_prompt.md`
- `local_kb/tools/kb_dispatch.py`
- `.trae/skills/local-kb-orchestrator/SKILL.md`

## 3. 最小接入方式

1. 打开 `local_kb_workspace/`
2. 把 `kb_bootstrap_prompt.md` 发给 AI
3. 之后直接正常提需求

如果换到其他代理，最稳的方式仍然是“打开工作区 + 粘贴提示词”。

## 4. 核心规则

- 唯一固定入口是 `local_kb/kb_manifest.yaml`
- 先判断 `intent`
- 再判断 `domain`
- 只做最小化读取
- 优先复用已有知识
- 新知识先确认创建

## 5. 常用命令

```bash
python3 local_kb/tools/kb_dispatch.py bootstrap-prompt
python3 local_kb/tools/kb_dispatch.py intent --text "帮我总结今天的 QGC 调试"
python3 local_kb/tools/kb_dispatch.py route --text "帮我分析 STM32H73 串口 DMA 异常"
python3 local_kb/tools/kb_dispatch.py best-entry --text "继续优化知识库主线恢复"
python3 local_kb/tools/kb_dispatch.py digest --text "把这套知识库整理成最小交付方案"
python3 local_kb/tools/kb_dispatch.py capture --text "把这段旧对话整理成知识草稿"
python3 local_kb/tools/kb_dispatch.py propose-create --text "这是一个新的知识主题"
python3 local_kb/tools/kb_dispatch.py create-from-confirmation --creation-type new-note --text "新的知识主题" --domain shared --confirm
```

## 6. 输出预期

知识库相关任务完成后，输出最好包含：

- `best_entry`
- `digest`
- `capture`
- `suggested_writeback`
- `governance_feedback`

如果不是完整闭环任务，也至少说明：

- 读取了什么
- 复用了什么
- 缺了什么
- 下一步最该推进什么

## 7. 回写原则

- 稳定结论优先写正式知识
- 未收敛内容优先保留草稿
- 治理问题优先回写知识库自身
- 新主题默认先确认，不自动创建正式知识
