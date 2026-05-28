# 确认后创建工作流

## 1. 目标

这份文档定义“AI 先询问用户，用户确认后再自动创建”的总库级流程。

它用于处理两类事情：

1. 创建新领域
2. 创建新知识草稿

## 2. 原则

默认顺序固定为：

1. 先查现有知识
2. 若未命中或无法容纳
3. 先请求用户确认
4. 用户确认后执行 `create-from-confirmation`

**结构化元信息**

- `layer`: `workflow`
- `symptom`: 识别到新知识后直接创建文件，绕过用户确认，导致误创建和知识污染
- `evidence`:
  - `create-from-confirmation` 明确要求用户确认后才执行
  - 没有 `--confirm` 时脚本不应写文件
- `recommended_action`:
  - 固定执行“先查用、再确认、后创建”的顺序
  - 将创建动作收敛到 `create-from-confirmation`
- `portability`: `high`
- `confidence`: `verified`

## 3. 命令

### 3.1 创建新领域

```bash
python3 local_kb/tools/kb_dispatch.py create-from-confirmation \
  --creation-type new-domain \
  --text "ROS2 桥接经验" \
  --domain ros2_桥接 \
  --title "ROS2 Bridge" \
  --summary "用于管理 ROS2 桥接、通信和集成相关知识。" \
  --confirm
```

### 3.2 在已有领域里创建新知识草稿

```bash
python3 local_kb/tools/kb_dispatch.py create-from-confirmation \
  --creation-type new-note \
  --text "QGC 参数面板经验" \
  --domain qgc \
  --title "QGC 参数面板调试草稿" \
  --summary "记录参数面板显示、绑定和调试经验。" \
  --confirm
```

## 4. 产物

### 4.1 新领域

会创建：

- `local_kb/domains/<slug>/README.md`
- `local_kb/domains/<slug>/drafts/`

### 4.2 新知识草稿

会创建：

- `local_kb/domains/<domain>/drafts/<timestamp>_<slug>.md`

**结构化元信息**

- `layer`: `drafting`
- `symptom`: 用户确认后仍然不知道系统会落盘到哪里，导致后续审阅和并入流程断裂
- `evidence`:
  - 新领域和新笔记的落盘位置不同
  - 草稿路径稳定后，更方便 `Obsidian` 审阅和人工并入
- `recommended_action`:
  - 在创建前后都显式说明目标路径
  - 优先把新知识落到 `drafts/`，再人工并入正式笔记
- `portability`: `high`
- `confidence`: `verified`

## 5. 安全边界

如果没有显式传入：

- `--confirm`

脚本不会写入任何文件，只会返回提示，防止误创建。

**结构化元信息**

- `layer`: `safety`
- `symptom`: 执行创建命令时担心误写文件，尤其是在批量试错或对流程还不熟时
- `evidence`:
  - 没有 `--confirm` 时脚本只返回提示
  - 安全边界清晰时，用户更敢试运行创建流程
- `recommended_action`:
  - 默认先无 `--confirm` 试跑
  - 确认输出路径和创建类型正确后，再加 `--confirm`
- `portability`: `high`
- `confidence`: `verified`
