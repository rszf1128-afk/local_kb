#!/usr/bin/env python3
"""Dispatch workspace knowledge-base intents and domains."""

from __future__ import annotations

import argparse
from datetime import datetime
import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
KB_ROOT = ROOT / "local_kb"
MANIFEST_PATH = KB_ROOT / "kb_manifest.yaml"
DOMAINS_DIR = KB_ROOT / "domains"
DRAFTS_DIR = KB_ROOT / "drafts"
META_GOVERNANCE_KEYWORDS = {
    "优化知识库",
    "修改知识库",
    "元知识",
    "Obsidian",
    "图谱",
    "思想宫殿",
    "路由",
    "skill",
    "提示词",
}
MISSION_KEYWORDS = {
    "主线",
    "当前对话",
    "新对话",
    "架构主线",
    "使命层",
    "最高层目标",
    "公开目标",
    "公开定位",
    "公开私有知识",
    "私有知识内容",
    "全人类",
    "面向所有人",
    "恢复主线",
    "新对话续接",
    "续接新对话",
    "method",
    "技能装配",
    "skill orchestration",
    "protocol framework",
    "本地认知协作协议",
}
PROMPT_GOVERNANCE_KEYWORDS = {
    "提示词",
    "prompt",
    "bootstrap",
    "manifest",
    "路由原则",
    "固定文档",
    "固定文档名单",
    "最小化读取",
    "知识入口",
}
DELIVERY_KEYWORDS = {"同事", "交付", "培训", "开始用", "上手", "文档", "手册", "使用"}
DELIVERY_FILES = {
    "local_kb/kb_user_manual.md",
    "local_kb/kb_usage_guide.md",
}
GOVERNANCE_RULE_FILES = {
    "local_kb/domains/shared/knowledge_system_evolution.md",
    "local_kb/domains/shared/local_cognition_protocol.md",
    "local_kb/kb_creation_policy.md",
    "local_kb/kb_confirmation_workflow.md",
    "local_kb/kb_obsidian_conventions.md",
    "local_kb/kb_user_manual.md",
    "local_kb/kb_usage_guide.md",
}
MISSION_RULE_FILES = {"local_kb/domains/shared/local_cognition_protocol.md"}
OBSIDIAN_RULE_FILES = {"local_kb/kb_obsidian_conventions.md"}
GRAPH_KEYWORDS = {"frontmatter", "wikilink", "MOC", "图谱", "目录结构"}
CREATION_KEYWORDS = {"新主题", "新知识", "正式知识", "草稿", "创建", "确认创建", "不要自动创建"}
CONFIRMATION_KEYWORDS = {"--confirm", "确认", "试跑", "写文件", "误写", "安全边界", "落盘", "drafts"}
OBSIDIAN_KEYWORDS = {"Obsidian", "frontmatter", "wikilink", "图谱", "MOC", "语义", "目录结构"}
LONG_MEMORY_KEYWORDS = {"太长", "过长", "越来越长", "一条记忆", "单条记忆", "混在一起", "拆分", "重组"}
MISS_KEYWORDS = {"没命中", "命中不足", "缺少核心点", "没记录到核心点", "漏掉", "补充核心点", "补记", "更新记忆"}
ENTRYPOINT_KEYWORDS = {"入口", "wikilink", "frontmatter", "MOC", "图谱", "关联", "交织", "链接"}
ROUTING_KEYWORDS = {"路由", "检索", "命中", "找不到", "没有找到", "读不到", "读错"}
STRUCTURED_MARKER = "**结构化元信息**"

BOOTSTRAP_PROMPTS = {
    "full": (
        "你现在作为本地知识库协作代理工作：先读取 "
        "`local_kb/kb_manifest.yaml`，把它当作本工作区唯一的知识路由入口；"
        "每次收到用户输入时先判断意图属于 `retrieve/查用`、`capture/沉淀` 还是 `governance/治理`，"
        "再判断属于哪个已知领域、子知识包或是否为新的知识主题；随后按 `manifest` 和当前命中的最优入口，"
        "只读取最相关的总库或子库文件，优先复用已有经验，不重复总结，不预设固定要读哪些文档，也不要因为提示词里出现过某些示例文件就优先读取它们。"
        "已知领域只是当前种子示例，包括 `PX4`、`QGC/QGroundControl`、`embedded/嵌入式`、`shared/通用治理` 等，"
        "未来遇到新的知识领域也应按同一套方式处理。若当前请求已经命中某个具体领域，优先读取顺序应是："
        "该领域入口、该领域已有笔记、该领域 drafts、与当前问题直接命中的少量相关资料；不要过早扩展到整个工程仓库、"
        "无关代码改动、`git status` 或大范围关键字搜索，除非现有知识确实不足且用户明确需要代码级排查。"
        "若用户输入包含“总结、复盘、沉淀、记录、归档、回写、经验、记忆、写进知识库”等词，自动进入 `capture/沉淀` 模式，"
        "整理 `observation/观察`、`interpretation/解释`、`action/动作`、`verification/复测判据`，并生成可回写的知识草稿；"
        "若用户输入包含“操作手册、同事、技能、prompt、提示词、知识库结构、规范、治理、协议、框架、本地认知、协作系统”等词，"
        "自动进入 `governance/治理` 模式，但仍然只按当前问题最相关的本地知识进行最小化读取，而不是固定关注某几个文档。"
        "如果当前知识未命中现有领域，或命中了领域但缺少合适的现有知识条目，不要自动创建，必须先请求用户确认是否创建新领域或新知识笔记；"
        "如果用户已经明确确认创建，则使用 `create-from-confirmation` 流程生成 `Obsidian` 兼容的领域骨架或知识草稿。"
        "输出时必须说明读取了哪些知识、复用了哪些经验、当前缺了哪些知识，以及建议回写到哪里；如果是治理问题，"
        "还要优先判断当前应先完善体系、验证效果、增强连续性，还是再继续细化下层协议。"
    ),
    "minimal": (
        "先把 `local_kb/kb_manifest.yaml` 当作唯一知识入口，先判定意图和领域，再按当前问题最小化读取并复用经验；"
        "不要预设固定要读哪些文档。若已命中具体领域，先读该领域入口、该领域笔记和 drafts，不要过早扩展到整仓代码噪声。"
        "遇到“总结、复盘、沉淀、记录、写进知识库”等词时自动进入沉淀模式，生成知识草稿和回写建议；"
        "遇到新知识时先询问用户是否创建，确认后走 `create-from-confirmation`。"
    ),
}


def _load_manifest() -> dict[str, Any]:
    text = MANIFEST_PATH.read_text(encoding="utf-8")
    try:
        import yaml  # type: ignore

        data = yaml.safe_load(text)
        if isinstance(data, dict):
            return data
    except Exception:
        pass
    return _parse_simple_yaml(text)


def _parse_simple_yaml(text: str) -> dict[str, Any]:
    root: dict[str, Any] = {}
    stack: list[tuple[int, Any]] = [(-1, root)]
    lines = text.splitlines()

    for idx, raw_line in enumerate(lines):
        if not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue

        indent = len(raw_line) - len(raw_line.lstrip(" "))
        stripped = raw_line.strip()

        while len(stack) > 1 and indent <= stack[-1][0]:
            stack.pop()

        parent = stack[-1][1]

        if stripped.startswith("- "):
            value = _parse_scalar(stripped[2:].strip())
            if not isinstance(parent, list):
                raise ValueError(f"Invalid list position: {raw_line}")
            parent.append(value)
            continue

        if ":" not in stripped:
            continue

        key, value = stripped.split(":", 1)
        key = key.strip()
        value = value.strip()

        if value == "":
            next_container = _infer_next_container(lines, idx)
            if not isinstance(parent, dict):
                raise ValueError(f"Invalid mapping position: {raw_line}")
            parent[key] = next_container
            stack.append((indent, next_container))
        else:
            if not isinstance(parent, dict):
                raise ValueError(f"Invalid scalar position: {raw_line}")
            parent[key] = _parse_scalar(value)

    return root


def _contains_any_keyword(text: str | None, keywords: set[str]) -> bool:
    text_value = (text or "").lower()
    return any(keyword.lower() in text_value for keyword in keywords)


def _infer_next_container(lines: list[str], idx: int) -> Any:
    current_line = lines[idx]
    current_indent = len(current_line) - len(current_line.lstrip(" "))
    for next_line in lines[idx + 1 :]:
        if not next_line.strip() or next_line.lstrip().startswith("#"):
            continue
        next_indent = len(next_line) - len(next_line.lstrip(" "))
        if next_indent <= current_indent:
            return {}
        return [] if next_line.strip().startswith("- ") else {}
    return {}


def _parse_scalar(value: str) -> Any:
    if value.startswith('"') and value.endswith('"'):
        return value[1:-1]
    if value.startswith("'") and value.endswith("'"):
        return value[1:-1]
    if value.isdigit():
        return int(value)
    return value


def _normalize(text: str) -> str:
    return re.sub(r"\s+", "", text.lower())


def _score_keywords(text: str, keywords: list[str]) -> tuple[int, list[str]]:
    normalized = _normalize(text)
    score = 0
    matched: list[str] = []
    for keyword in keywords:
        token = _normalize(keyword)
        if token and token in normalized:
            score += 3
            matched.append(keyword)
    return score, matched


def _pick_best(text: str, routes: dict[str, Any]) -> list[dict[str, Any]]:
    ranked: list[dict[str, Any]] = []
    for name, spec in routes.items():
        if not isinstance(spec, dict):
            continue
        score, matched = _score_keywords(text, spec.get("keywords", []))
        if score <= 0:
            continue
        ranked.append(
            {
                "name": name,
                "score": score,
                "matched": matched,
                "read": spec.get("read", []),
                "action": spec.get("action"),
            }
        )
    ranked.sort(key=lambda item: (-item["score"], item["name"]))
    return ranked


def _normalize_match_text(text: str) -> str:
    return re.sub(r"[^a-z0-9\u4e00-\u9fff]+", " ", text.lower()).strip()


def _tokenize_text(text: str) -> list[str]:
    return re.findall(r"[a-z0-9_]+|[\u4e00-\u9fff]+", _normalize_match_text(text))


def _normalize_path(path_str: str) -> str:
    path_str = path_str.replace("\\", "/")
    if path_str.startswith("/home/"):
        return path_str
    return str((ROOT / path_str).resolve())


def _resolve_read_path(path_str: str) -> Path:
    return Path(_normalize_path(path_str))


def _strip_frontmatter(text: str) -> str:
    if not text.startswith("---\n"):
        return text

    lines = text.splitlines()
    end_idx = None
    for idx in range(1, len(lines)):
        if lines[idx].strip() == "---":
            end_idx = idx
            break

    if end_idx is None:
        return text
    return "\n".join(lines[end_idx + 1 :]).lstrip()


def _load_markdown_sections(path: Path) -> list[dict[str, str]]:
    text = _strip_frontmatter(path.read_text(encoding="utf-8"))
    sections: list[dict[str, str]] = []
    current_heading = path.stem
    current_lines: list[str] = []

    for line in text.splitlines():
        if line.startswith("#"):
            if current_lines:
                sections.append({"heading": current_heading, "body": "\n".join(current_lines).strip()})
            current_heading = line.lstrip("#").strip() or path.stem
            current_lines = []
            continue
        current_lines.append(line)

    if current_lines:
        sections.append({"heading": current_heading, "body": "\n".join(current_lines).strip()})

    return [section for section in sections if section["body"]]


def _compact_text(text: str, max_chars: int) -> str:
    compact = re.sub(r"\s+", " ", text).strip()
    if len(compact) <= max_chars:
        return compact
    return compact[: max_chars - 3].rstrip() + "..."


def _clean_inline_markup(text: str) -> str:
    return re.sub(r"\s+", " ", text.replace("`", "").strip())


def _ensure_list(value: Any) -> list[str]:
    if isinstance(value, list):
        return [_clean_inline_markup(str(item)) for item in value if str(item).strip()]
    if isinstance(value, str) and value.strip():
        return [_clean_inline_markup(value)]
    return []


def _token_overlap(left: list[str], right: list[str]) -> int:
    overlap = 0
    for left_item in left:
        for right_item in right:
            if left_item == right_item:
                overlap += 1
                break
            if left_item in right_item or right_item in left_item:
                overlap += 1
                break
    return overlap


def _load_structured_entries(path: Path) -> list[dict[str, Any]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    entries: list[dict[str, Any]] = []
    current_h2 = ""
    current_h3 = ""
    idx = 0

    while idx < len(lines):
        line = lines[idx]
        stripped = line.strip()

        if line.startswith("## "):
            current_h2 = line[3:].strip()
            current_h3 = ""
        elif line.startswith("### "):
            current_h3 = line[4:].strip()

        if stripped != STRUCTURED_MARKER:
            idx += 1
            continue

        entry: dict[str, Any] = {
            "file": str(path.relative_to(ROOT)),
            "section": current_h2,
            "title": current_h3 or current_h2 or path.stem,
            "layer": "",
            "symptom": "",
            "evidence": [],
            "recommended_action": [],
            "portability": "",
            "confidence": "",
        }
        current_key = ""
        idx += 1

        while idx < len(lines):
            raw = lines[idx]
            stripped = raw.strip()

            if not stripped:
                idx += 1
                continue

            if raw.startswith("## ") or raw.startswith("### ") or stripped == STRUCTURED_MARKER:
                break
            if stripped.startswith("**") and stripped.endswith("**"):
                break

            field_match = re.match(r"-\s+`([^`]+)`:\s*(.*)$", stripped)
            if field_match:
                current_key = field_match.group(1).strip()
                raw_value = field_match.group(2).strip()
                value = raw_value.strip("`")
                if value:
                    entry[current_key] = _clean_inline_markup(value)
                else:
                    entry[current_key] = []
                idx += 1
                continue

            nested_match = re.match(r"-\s+(.*)$", stripped)
            if nested_match and current_key:
                item = nested_match.group(1).strip().strip("`")
                if not item:
                    idx += 1
                    continue
                current_value = entry.get(current_key)
                if isinstance(current_value, list):
                    current_value.append(item)
                elif current_value:
                    entry[current_key] = [str(current_value), item]
                else:
                    entry[current_key] = [item]
                idx += 1
                continue

            idx += 1

        entry["evidence"] = _ensure_list(entry.get("evidence"))
        entry["recommended_action"] = _ensure_list(entry.get("recommended_action"))
        entries.append(entry)

    return entries


def _score_structured_entry(entry: dict[str, Any], text: str, route_keywords: list[str] | None = None) -> int:
    text_norm = _normalize_match_text(text)
    text_tokens = _tokenize_text(text)
    title_text = str(entry.get("title", ""))
    score = 0

    symptom = str(entry.get("symptom", ""))
    symptom_norm = _normalize_match_text(symptom)
    symptom_tokens = _tokenize_text(symptom)

    if symptom_norm:
        if symptom_norm in text_norm or text_norm in symptom_norm:
            score += 8
        else:
            score += 2 * _token_overlap(text_tokens, symptom_tokens)

    haystack = _normalize_match_text(
        " ".join(
            [
                str(entry.get("title", "")),
                symptom,
                " ".join(_ensure_list(entry.get("evidence"))),
                " ".join(_ensure_list(entry.get("recommended_action"))),
                str(entry.get("layer", "")),
            ]
        )
    )

    for keyword in route_keywords or []:
        keyword_norm = _normalize_match_text(keyword)
        if keyword_norm and keyword_norm in haystack:
            score += 3

    if _contains_any_keyword(text, {"主线", "当前对话", "架构主线"}) and "主线" in title_text:
        score += 6

    for evidence_item in _ensure_list(entry.get("evidence")):
        overlap = _token_overlap(text_tokens, _tokenize_text(evidence_item))
        if overlap > 0:
            score += overlap

    if entry.get("confidence") == "verified":
        score += 2
    if entry.get("portability") == "high":
        score += 1

    if any(keyword in text for keyword in DELIVERY_KEYWORDS):
        if entry.get("layer") in {"delivery", "onboarding"}:
            score += 4
        if entry.get("file") in DELIVERY_FILES:
            score += 4

    if any(keyword in text for keyword in OBSIDIAN_KEYWORDS):
        if entry.get("file") in OBSIDIAN_RULE_FILES:
            score += 5
        if entry.get("layer") in {"graph", "format"}:
            score += 2

    if any(keyword in text for keyword in GRAPH_KEYWORDS):
        if entry.get("file") in OBSIDIAN_RULE_FILES:
            score += 4
        if entry.get("layer") == "graph":
            score += 3

    if _contains_any_keyword(text, MISSION_KEYWORDS):
        if entry.get("file") in MISSION_RULE_FILES:
            score += 8
        if "使命层" in title_text:
            score += 4

    return score


def _build_structured_why_matched(
    entry: dict[str, Any],
    text: str,
    route_keywords: list[str] | None = None,
    matched_terms: list[str] | None = None,
) -> dict[str, Any]:
    text_tokens = _tokenize_text(text)
    symptom = str(entry.get("symptom", ""))
    evidence = _ensure_list(entry.get("evidence"))
    recommended = _ensure_list(entry.get("recommended_action"))
    matched_fields: list[str] = []

    if _token_overlap(text_tokens, _tokenize_text(symptom)) > 0:
        matched_fields.append("symptom")

    if any(_token_overlap(text_tokens, _tokenize_text(item)) > 0 for item in evidence):
        matched_fields.append("evidence")

    if any(_token_overlap(text_tokens, _tokenize_text(item)) > 0 for item in recommended):
        matched_fields.append("recommended_action")

    keyword_hits: list[str] = []
    haystack = _normalize_match_text(
        " ".join(
            [
                str(entry.get("title", "")),
                symptom,
                " ".join(evidence),
                " ".join(recommended),
                str(entry.get("layer", "")),
            ]
        )
    )
    for keyword in route_keywords or []:
        keyword_norm = _normalize_match_text(keyword)
        if keyword_norm and keyword_norm in haystack and keyword not in keyword_hits:
            keyword_hits.append(keyword)

    field_haystacks = {
        "symptom": _normalize_match_text(symptom),
        "evidence": _normalize_match_text(" ".join(evidence)),
        "recommended_action": _normalize_match_text(" ".join(recommended)),
    }
    for keyword in keyword_hits:
        keyword_norm = _normalize_match_text(keyword)
        if not keyword_norm:
            continue
        for field_name, field_text in field_haystacks.items():
            if keyword_norm in field_text and field_name not in matched_fields:
                matched_fields.append(field_name)

    return {
        "matched_text": text,
        "matched_terms": matched_terms or [],
        "matched_keywords": keyword_hits,
        "matched_fields": matched_fields,
    }


def _find_structured_entries_for_files(
    files: list[str],
    text: str,
    route_keywords: list[str] | None = None,
    matched_terms: list[str] | None = None,
    max_entries: int = 3,
) -> list[dict[str, Any]]:
    ranked: list[dict[str, Any]] = []
    seen: set[tuple[str, str]] = set()

    for file_path in files:
        path = _resolve_read_path(file_path)
        if not path.exists() or path.suffix.lower() != ".md":
            continue
        for entry in _load_structured_entries(path):
            score = _score_structured_entry(entry, text, route_keywords)
            if score <= 0:
                continue
            dedupe_key = (entry["file"], entry["title"])
            if dedupe_key in seen:
                continue
            seen.add(dedupe_key)
            ranked.append(
                {
                    "type": "structured",
                    "score": score,
                    "file": entry["file"],
                    "title": entry["title"],
                    "section": entry.get("section", ""),
                    "layer": entry.get("layer", ""),
                    "symptom": entry.get("symptom", ""),
                    "evidence": _ensure_list(entry.get("evidence"))[:3],
                    "recommended_action": _ensure_list(entry.get("recommended_action"))[:3],
                    "portability": entry.get("portability", ""),
                    "confidence": entry.get("confidence", ""),
                    "why_matched": _build_structured_why_matched(
                        entry,
                        text,
                        route_keywords=route_keywords,
                        matched_terms=matched_terms,
                    ),
                }
            )

    ranked.sort(key=lambda item: (-item["score"], item["file"], item["title"]))
    return ranked[:max_entries]


def _score_markdown_section(
    file_path: str,
    section: dict[str, str],
    text: str,
    route_keywords: list[str] | None = None,
    preferred_files: set[str] | None = None,
) -> int:
    heading_norm = _normalize_match_text(section.get("heading", ""))
    body_norm = _normalize_match_text(section.get("body", ""))
    path_norm = _normalize_match_text(file_path)
    combined = f"{heading_norm} {body_norm} {path_norm}".strip()
    score = 0

    query_norm = _normalize_match_text(text)
    if query_norm and query_norm in combined:
        score += 8

    for keyword in route_keywords or []:
        keyword_norm = _normalize_match_text(keyword)
        if not keyword_norm:
            continue
        if keyword_norm in combined:
            score += 4
        if keyword_norm in heading_norm:
            score += 3

    for token in _tokenize_text(text):
        if len(token) <= 1:
            continue
        if token in heading_norm:
            score += 7
        elif token in body_norm:
            score += 3
        elif token in path_norm:
            score += 2

    if preferred_files and file_path in preferred_files:
        score += 8
        for keyword in route_keywords or []:
            if keyword in META_GOVERNANCE_KEYWORDS:
                score += 5

    if _contains_any_keyword(text, MISSION_KEYWORDS):
        if file_path in MISSION_RULE_FILES:
            score += 8
        if "使命层" in section.get("heading", ""):
            score += 4

    return score


def _find_best_entries_for_files(
    files: list[str],
    text: str,
    route_keywords: list[str] | None = None,
    matched_terms: list[str] | None = None,
    preferred_files: set[str] | None = None,
    max_entries: int = 3,
) -> list[dict[str, Any]]:
    ranked: list[dict[str, Any]] = []
    seen: set[tuple[str, str]] = set()

    for file_path in files:
        path = _resolve_read_path(file_path)
        if not path.exists() or path.suffix.lower() != ".md":
            continue
        for section in _load_markdown_sections(path):
            score = _score_markdown_section(file_path, section, text, route_keywords, preferred_files)
            if score <= 0:
                continue
            key = (file_path, section["heading"])
            if key in seen:
                continue
            seen.add(key)
            ranked.append(
                {
                    "type": "markdown",
                    "file": file_path,
                    "heading": section["heading"],
                    "excerpt": _compact_text(section["body"], 220),
                    "score": score,
                    "why_matched": {
                        "matched_text": text,
                        "matched_terms": matched_terms or [],
                        "matched_keywords": route_keywords or [],
                        "matched_fields": ["heading" if any(token in _normalize_match_text(section["heading"]) for token in _tokenize_text(text)) else "body"],
                    },
                }
            )

    ranked.sort(key=lambda item: (-item["score"], item["file"], item["heading"]))
    return ranked[:max_entries]


def _entry_target_file(entry: dict[str, Any] | None) -> str | None:
    if not entry:
        return None
    file_path = entry.get("file")
    return str(file_path) if file_path else None


def _build_suggested_next_read(
    best_entry: dict[str, Any] | None,
    related_entries: list[dict[str, Any]],
    source_files: list[str],
) -> list[str]:
    ordered: list[str] = []
    seen: set[str] = set()

    for candidate in [_entry_target_file(best_entry)]:
        if candidate and candidate not in seen:
            seen.add(candidate)
            ordered.append(candidate)

    for entry in related_entries:
        candidate = _entry_target_file(entry)
        if candidate and candidate not in seen:
            seen.add(candidate)
            ordered.append(candidate)

    for file_path in source_files:
        if file_path not in seen:
            seen.add(file_path)
            ordered.append(file_path)

    return ordered[:3]


def _classify_governance_writeback(
    text: str | None,
    best_entry: dict[str, Any] | None,
) -> dict[str, Any] | None:
    entry_file = _entry_target_file(best_entry)
    entry_layer = str((best_entry or {}).get("layer", ""))
    entry_title = str((best_entry or {}).get("title", ""))
    text_value = text or ""

    def _has_any(tokens: set[str]) -> bool:
        return any(token in text_value for token in tokens)

    has_confirmation = _has_any(CONFIRMATION_KEYWORDS)
    has_creation = _has_any(CREATION_KEYWORDS)
    has_obsidian = _has_any(OBSIDIAN_KEYWORDS)
    has_prompt_governance = _has_any(PROMPT_GOVERNANCE_KEYWORDS)

    if (
        entry_file == "local_kb/domains/shared/knowledge_system_evolution.md"
        or (
            has_prompt_governance
            and not has_confirmation
            and not has_creation
            and not has_obsidian
        )
    ):
        return {
            "target": "local_kb/domains/shared/knowledge_system_evolution.md",
            "reason": "当前请求更接近提示词、路由原则或知识系统本身的演化规则，应优先回写到知识系统演化文档。",
        }

    if (
        entry_file == "local_kb/kb_confirmation_workflow.md"
        or entry_layer in {"workflow", "drafting", "safety"}
        or "安全边界" in entry_title
        or has_confirmation
    ):
        return {
            "target": "local_kb/kb_confirmation_workflow.md",
            "reason": "当前请求更接近确认后创建、试跑、落盘或安全边界，应优先回写到确认工作流。",
        }

    if (
        has_obsidian
        or entry_file == "local_kb/kb_obsidian_conventions.md"
        or entry_layer in {"graph", "format"}
    ):
        return {
            "target": "local_kb/kb_obsidian_conventions.md",
            "reason": "当前请求更接近 Obsidian 编写规范、图谱表达或目录/语义关系，应优先回写到 Obsidian 规范。",
        }

    if (
        entry_file == "local_kb/kb_creation_policy.md"
        or has_creation
        or ("新知识" in entry_title or "核心原则" in entry_title)
    ):
        return {
            "target": "local_kb/kb_creation_policy.md",
            "reason": "当前请求更接近新知识创建边界与正式/草稿分层，应优先回写到创建策略。",
        }

    if entry_file == "local_kb/kb_usage_guide.md" or any(token in text_value for token in {"交付", "培训", "最小方案", "阅读顺序"}):
        return {
            "target": "local_kb/kb_usage_guide.md",
            "reason": "当前请求更接近交付方式、阅读顺序或最小使用路径，应优先回写到使用办法。",
        }

    if entry_file == "local_kb/kb_user_manual.md" or entry_layer in {"delivery", "onboarding", "output"} or _has_any(DELIVERY_KEYWORDS):
        return {
            "target": "local_kb/kb_user_manual.md",
            "reason": "当前请求更接近用户上手、日常使用或输出约定，应优先回写到用户手册。",
        }

    return None


def _build_suggested_writeback(
    text: str | None,
    intent: dict[str, Any] | None,
    domain: dict[str, Any] | None,
    best_entry: dict[str, Any] | None,
) -> dict[str, Any]:
    intent_name = (intent or {}).get("name")
    domain_name = (domain or {}).get("name")
    entry_file = _entry_target_file(best_entry)
    governance_writeback = _classify_governance_writeback(text, best_entry)

    if intent_name == "capture":
        draft_target = f"local_kb/domains/{domain_name}/drafts" if domain_name else "local_kb/drafts"
        return {
            "target": draft_target,
            "reason": "Capture/沉淀请求优先进入草稿，再人工并入正式知识。",
        }

    if intent_name == "package_or_governance" and governance_writeback:
        return governance_writeback

    if governance_writeback and (
        domain_name == "shared"
        or entry_file in {
            "local_kb/domains/shared/knowledge_system_evolution.md",
            "local_kb/kb_creation_policy.md",
            "local_kb/kb_confirmation_workflow.md",
            "local_kb/kb_obsidian_conventions.md",
            "local_kb/kb_user_manual.md",
            "local_kb/kb_usage_guide.md",
        }
    ):
        return governance_writeback

    if intent_name == "package_or_governance":
        return {
            "target": entry_file or "local_kb/domains/shared/knowledge_system_evolution.md",
            "reason": "当前请求属于总库治理问题，但不属于更细的手册/创建/图谱子类，优先回写到对应元知识或规则文档。",
        }

    if domain_name == "shared":
        return {
            "target": entry_file or "local_kb/domains/shared/README.md",
            "reason": "当前请求更接近 shared/通用治理知识，优先回写到 shared 规则文档。",
        }

    return {
        "target": entry_file or "local_kb/README.md",
        "reason": "默认优先复用当前命中的知识入口，必要时再扩展到更具体文档。",
    }


def _build_governance_feedback(
    text: str | None,
    intent: dict[str, Any] | None,
    domain: dict[str, Any] | None,
    best_entry: dict[str, Any] | None,
    related_entries: list[dict[str, Any]] | None,
    fallback: dict[str, Any] | None,
    suggested_writeback: dict[str, Any] | None,
) -> dict[str, Any] | None:
    text_value = text or ""
    intent_name = (intent or {}).get("name")
    domain_name = (domain or {}).get("name")
    entry_file = _entry_target_file(best_entry)
    entry_layer = str((best_entry or {}).get("layer", ""))
    writeback_target = str((suggested_writeback or {}).get("target", ""))
    related_files = {_entry_target_file(item) for item in (related_entries or []) if _entry_target_file(item)}

    def _has_any(tokens: set[str]) -> bool:
        return any(token in text_value for token in tokens)

    signals: list[str] = []

    if fallback:
        if domain_name and domain_name != "shared":
            signals.extend(["已命中领域", "没有可复用 best_entry", "领域正式知识不足"])
            return {
                "gap": "content",
                "action": "promote",
                "reason": "已经命中具体领域，但没有形成可复用条目，说明领域知识需要从草稿或零散经验提升为正式节点。",
                "target": writeback_target or f"local_kb/domains/{domain_name}/drafts",
                "signals": signals,
                "confidence": "working",
            }

        signals.extend(["没有命中可复用条目", "当前更像入口缺失或路由不足"])
        return {
            "gap": "routing",
            "action": "link",
            "reason": "当前没有稳定命中知识条目，优先补入口、链接或路由线索，再决定是否补内容。",
            "target": writeback_target or "local_kb/domains/shared/knowledge_system_evolution.md",
            "signals": signals,
            "confidence": "working",
        }

    if _has_any(LONG_MEMORY_KEYWORDS):
        signals.extend(["用户明确提到记忆过长或需要拆分", "当前更像结构问题而不是单点补写"])
        return {
            "gap": "structure",
            "action": "split",
            "reason": "当前问题更像单条记忆承载了过多信息，应拆成更小节点并通过链接重组，而不是继续追加长度。",
            "target": writeback_target or entry_file or "local_kb/domains/shared/knowledge_system_evolution.md",
            "signals": signals,
            "confidence": "working",
        }

    if (
        domain_name
        and domain_name != "shared"
        and intent_name == "capture"
        and entry_file == f"local_kb/domains/{domain_name}/README.md"
    ):
        signals.extend(["已命中具体领域", "当前主要命中领域入口而非领域正式知识"])
        return {
            "gap": "content",
            "action": "promote",
            "reason": "当前已识别到具体领域，但主要还是命中领域入口，说明该领域需要把本轮高频经验提升为正式知识节点。",
            "target": writeback_target or f"local_kb/domains/{domain_name}/drafts",
            "signals": signals,
            "confidence": "working",
        }

    if domain_name and domain_name != "shared" and entry_file in GOVERNANCE_RULE_FILES:
        signals.extend(["已命中具体领域", "best_entry 仍来自治理文档"])
        action = "promote" if intent_name == "capture" else "patch"
        reason = (
            "当前已识别到具体领域，但最优条目仍来自治理文档，说明该领域缺少足够稳定的正式知识节点。"
            if action == "promote"
            else "当前已识别到具体领域，但最优条目仍来自治理文档，说明该领域知识入口已存在，但关键内容仍需补丁式增强。"
        )
        return {
            "gap": "content",
            "action": action,
            "reason": reason,
            "target": writeback_target or f"local_kb/domains/{domain_name}/drafts",
            "signals": signals,
            "confidence": "working",
        }

    if _has_any(ENTRYPOINT_KEYWORDS) or entry_layer in {"graph", "format"} or writeback_target in OBSIDIAN_RULE_FILES:
        signals.extend(["出现入口或图谱关键词", "当前更接近链接或入口设计问题"])
        return {
            "gap": "entrypoint",
            "action": "link",
            "reason": "当前问题更接近缺少入口、wikilink、MOC 或 frontmatter，应优先补链接化记忆结构。",
            "target": writeback_target or "local_kb/kb_obsidian_conventions.md",
            "signals": signals,
            "confidence": "working",
        }

    if _has_any(MISS_KEYWORDS):
        signals.extend(["用户明确提到命中不足或漏掉核心点", "当前更接近已有知识需要补关键判据"])
        return {
            "gap": "content",
            "action": "patch",
            "reason": "当前更像已有知识缺少关键证据、判据或核心点，应优先补丁式更新，而不是新增长文档。",
            "target": writeback_target or entry_file or "local_kb/domains/shared/knowledge_system_evolution.md",
            "signals": signals,
            "confidence": "working",
        }

    if _has_any(ROUTING_KEYWORDS):
        signals.extend(["用户关注命中或检索问题", "当前更接近入口与路由层优化"])
        return {
            "gap": "routing",
            "action": "link",
            "reason": "当前更接近路由或入口命中问题，应先补领域入口、图谱链接或 manifest 线索，再决定是否补正文内容。",
            "target": writeback_target or "local_kb/domains/shared/knowledge_system_evolution.md",
            "signals": signals,
            "confidence": "working",
        }

    if len(related_files) == 1 and next(iter(related_files), "") in GOVERNANCE_RULE_FILES and domain_name and domain_name != "shared":
        signals.extend(["相关条目集中在治理文档", "领域知识图谱仍偏薄"])
        return {
            "gap": "content",
            "action": "promote",
            "reason": "当前领域请求主要还是靠治理文档支撑，说明领域正式知识仍偏薄，适合把高频经验提升为稳定节点。",
            "target": writeback_target or f"local_kb/domains/{domain_name}/drafts",
            "signals": signals,
            "confidence": "working",
        }

    return {
        "gap": "content",
        "action": "patch",
        "reason": "当前已有可复用知识入口，优先通过小步补丁式更新保持知识节点清晰，而不是继续堆长记忆。",
        "target": writeback_target or entry_file or "local_kb/README.md",
        "signals": ["已有可复用 best_entry", "默认采用最小增量更新"],
        "confidence": "working",
    }


def _is_governance_optimization_request(
    text: str | None,
    intent: dict[str, Any] | None,
    best_entry: dict[str, Any] | None,
    governance_feedback: dict[str, Any] | None,
) -> bool:
    text_value = text or ""
    intent_name = (intent or {}).get("name")
    entry_file = _entry_target_file(best_entry)
    governance_tokens = (
        META_GOVERNANCE_KEYWORDS
        | DELIVERY_KEYWORDS
        | CREATION_KEYWORDS
        | CONFIRMATION_KEYWORDS
        | OBSIDIAN_KEYWORDS
        | LONG_MEMORY_KEYWORDS
        | MISS_KEYWORDS
        | ENTRYPOINT_KEYWORDS
        | ROUTING_KEYWORDS
        | {"知识库", "记忆", "命中", "核心点", "自我优化"}
    )
    return bool(
        intent_name == "package_or_governance"
        or any(token in text_value for token in governance_tokens)
        or entry_file in GOVERNANCE_RULE_FILES
        or governance_feedback is not None
    )


def _choose_best_entry(
    *,
    top_domain: dict[str, Any] | None,
    text: str,
    source_files: list[str],
    matched_keywords: list[str],
    preferred_files: set[str],
    structured_entries: list[dict[str, Any]],
    max_entries: int,
) -> tuple[dict[str, Any] | None, list[dict[str, Any]], list[dict[str, Any]]]:
    markdown_entries = _find_best_entries_for_files(
        source_files,
        text,
        matched_keywords,
        matched_terms=matched_keywords,
        preferred_files=preferred_files,
        max_entries=max_entries,
    )

    if not structured_entries:
        return (markdown_entries[0] if markdown_entries else None, markdown_entries, markdown_entries)

    best_structured = structured_entries[0]
    domain_name = (top_domain or {}).get("name")
    if (
        domain_name
        and domain_name != "shared"
        and _entry_target_file(best_structured) in GOVERNANCE_RULE_FILES
        and markdown_entries
        and _entry_target_file(markdown_entries[0]) in preferred_files
        and markdown_entries[0].get("score", 0) >= 8
    ):
        combined: list[dict[str, Any]] = [markdown_entries[0]]
        seen_keys = {
            (
                markdown_entries[0].get("type"),
                _entry_target_file(markdown_entries[0]),
                markdown_entries[0].get("heading") or markdown_entries[0].get("title"),
            )
        }
        for entry in structured_entries + markdown_entries[1:]:
            key = (entry.get("type"), _entry_target_file(entry), entry.get("heading") or entry.get("title"))
            if key in seen_keys:
                continue
            seen_keys.add(key)
            combined.append(entry)
            if len(combined) >= max_entries:
                break
        return markdown_entries[0], combined, markdown_entries

    return best_structured, structured_entries, markdown_entries


def _files_for_digest(manifest: dict[str, Any], args: argparse.Namespace) -> list[str]:
    if getattr(args, "file", None):
        return [args.file]

    text = getattr(args, "text", None)
    if text:
        payload = _build_best_entry_payload(manifest, text, max_entries=max(args.max_entries, 1))
        files = payload.get("source_files", [])
        if files:
            return files

    return manifest.get("default_read_order", [])


def cmd_digest(args: argparse.Namespace) -> int:
    manifest = _load_manifest()
    files = _files_for_digest(manifest, args)
    best_payload = _build_best_entry_payload(manifest, args.text, max_entries=args.max_entries) if args.text else {
        "text": None,
        "intent": None,
        "domain": None,
        "best_entry": None,
        "related_entries": [],
        "suggested_next_read": files[:3],
        "suggested_writeback": None,
        "fallback": None,
    }

    payload_files: list[dict[str, Any]] = []
    for file_entry in files:
        path = _resolve_read_path(file_entry)
        if not path.exists() or path.suffix.lower() != ".md":
            continue

        sections = _load_markdown_sections(path)[: args.max_sections]
        compact_sections = [
            {
                "heading": section["heading"],
                "excerpt": _compact_text(section["body"], args.max_chars),
            }
            for section in sections
        ]

        structured_entries = _find_structured_entries_for_files(
            [file_entry],
            args.text or path.stem,
            route_keywords=(best_payload.get("domain") or {}).get("matched", []) + (best_payload.get("intent") or {}).get("matched", []),
            matched_terms=(best_payload.get("domain") or {}).get("matched", []) + (best_payload.get("intent") or {}).get("matched", []),
            max_entries=args.max_entries,
        )

        payload_files.append(
            {
                "path": str(path.relative_to(ROOT)),
                "sections": compact_sections,
                "structured_entries": structured_entries,
            }
        )

    payload = {
        "text": args.text,
        "intent": best_payload.get("intent"),
        "domain": best_payload.get("domain"),
        "best_entry": best_payload.get("best_entry"),
        "related_entries": best_payload.get("related_entries", []),
        "files": payload_files,
        "suggested_next_read": best_payload.get("suggested_next_read", []),
        "suggested_writeback": best_payload.get("suggested_writeback"),
        "governance_feedback": best_payload.get("governance_feedback"),
        "fallback": best_payload.get("fallback"),
    }
    _emit(payload, args.format)
    return 0


def _build_best_entry_payload(manifest: dict[str, Any], text: str, max_entries: int = 3) -> dict[str, Any]:
    domains = _pick_best(text, manifest.get("domain_routing", {}))
    intents = _pick_best(text, manifest.get("intent_routing", {}))
    top_domain = domains[0] if domains else None
    top_intent = intents[0] if intents else None

    preferred_files = set(top_domain.get("read", [])) if top_domain else set()
    source_files: list[str] = []
    for item in top_domain.get("read", []) if top_domain else []:
        if item not in source_files:
            source_files.append(item)
    if (top_domain or {}).get("name") == "shared" and _contains_any_keyword(text, MISSION_KEYWORDS):
        for item in MISSION_RULE_FILES:
            if item not in source_files:
                source_files.append(item)
            preferred_files.add(item)
    for item in manifest.get("default_read_order", []):
        if item not in source_files:
            source_files.append(item)

    matched_keywords: list[str] = []
    for token in (top_domain or {}).get("matched", []):
        if token not in matched_keywords:
            matched_keywords.append(token)
    for token in (top_intent or {}).get("matched", []):
        if token not in matched_keywords:
            matched_keywords.append(token)

    structured_entries = _find_structured_entries_for_files(
        source_files,
        text,
        route_keywords=matched_keywords,
        matched_terms=matched_keywords,
        max_entries=max_entries,
    )
    best_entry, related_entries, markdown_entries = _choose_best_entry(
        top_domain=top_domain,
        text=text,
        source_files=source_files,
        matched_keywords=matched_keywords,
        preferred_files=preferred_files,
        structured_entries=structured_entries,
        max_entries=max_entries,
    )

    fallback = None
    if best_entry is None:
        fallback = {
            "reason": "No markdown section scored above zero; fall back to routed files.",
            "suggested_reads": source_files,
            "matched_keywords": matched_keywords,
        }

    suggested_writeback = _build_suggested_writeback(text, top_intent, top_domain, best_entry)
    return {
        "text": text,
        "intent": top_intent,
        "domain": top_domain,
        "source_files": source_files,
        "best_entry": best_entry,
        "related_entries": related_entries,
        "suggested_next_read": _build_suggested_next_read(best_entry, related_entries, source_files),
        "suggested_writeback": suggested_writeback,
        "governance_feedback": _build_governance_feedback(
            text,
            top_intent,
            top_domain,
            best_entry,
            related_entries,
            fallback,
            suggested_writeback,
        ),
        "fallback": fallback,
    }


def _suggest_slug(text: str) -> str:
    cleaned = text.lower()
    stop_phrases = [
        "帮我",
        "整理",
        "总结",
        "今天",
        "并写进知识库",
        "写进知识库",
        "知识库",
        "经验",
        "问题",
        "一下",
        "这是",
        "一个",
        "新的",
        "主题",
        "请先问我",
        "要不要创建",
        "并",
    ]
    for phrase in stop_phrases:
        cleaned = cleaned.replace(phrase, " ")

    raw_tokens = re.findall(r"[a-z0-9]+|[\u4e00-\u9fff]+", cleaned)
    stopwords = set()
    tokens = [token for token in raw_tokens if token not in stopwords]
    if not tokens:
        return "new-domain"
    return "_".join(tokens[:3])


def _note_slug(text: str) -> str:
    slug = _suggest_slug(text)
    return slug or "new-note"


def _creation_proposal(
    manifest: dict[str, Any],
    text: str,
    matched_domain: dict[str, Any] | None,
    candidate_domains: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    policy = manifest.get("creation_policy", {})
    templates = policy.get("templates", {})
    if matched_domain is None:
        create_type = "new_domain_or_note"
        reason = "No existing domain matched the current request."
    else:
        create_type = "new_note"
        reason = f"Domain '{matched_domain['name']}' matched, but this request may still require a new knowledge note."

    slug = _suggest_slug(text)
    return {
        "requires_user_confirmation": True,
        "reason": reason,
        "question": "当前知识未被现有结构完整覆盖，是否要创建新的知识条目或新领域入口？",
        "suggested_creation_type": create_type,
        "suggested_domain_slug": slug if matched_domain is None else matched_domain["name"],
        "candidate_domains": [item["name"] for item in (candidate_domains or [])],
        "suggested_paths": {
            "domain_template": templates.get("new_domain"),
            "note_template": templates.get("new_note"),
            "suggested_domain_home": f"local_kb/domains/{slug}/README.md" if matched_domain is None else None,
            "suggested_note_dir": f"local_kb/domains/{matched_domain['name']}/drafts" if matched_domain else "local_kb/drafts",
        },
    }


def _render_domain_home(slug: str, title: str, summary: str) -> str:
    display_title = title or slug
    summary_line = summary or "一句话说明这个新领域要管理什么知识。"
    return (
        "---\n"
        f"title: {display_title} Domain Home\n"
        "type: moc\n"
        f"domain: {slug}\n"
        "status: draft\n"
        "tags:\n"
        "  - knowledge-base\n"
        "  - moc\n"
        "  - domain\n"
        "---\n\n"
        f"# {display_title} 领域入口\n\n"
        "## 领域说明\n\n"
        f"{summary_line}\n\n"
        "## 推荐首批知识主题\n\n"
        "1. 待补充。\n"
        "2. 待补充。\n"
        "3. 待补充。\n\n"
        "## 与现有领域的关系\n\n"
        "- 待补充。\n\n"
        "## 回写规则\n\n"
        "- 先写草稿。\n"
        "- 先人工审阅。\n"
        "- 再并入正式知识结构。\n"
    )


def _render_note_draft(domain: str, title: str, text: str, summary: str | None) -> str:
    display_title = title or text
    summary_line = summary or "一句话概括本轮要沉淀的经验。"
    return (
        "---\n"
        f"title: {display_title}\n"
        "type: capture\n"
        f"domain: {domain}\n"
        "status: draft\n"
        "tags:\n"
        "  - knowledge-base\n"
        "  - capture\n"
        "---\n\n"
        "# 标题\n\n"
        f"{display_title}\n\n"
        "## 元信息\n\n"
        "- `intent`: capture\n"
        f"- `domain`: {domain}\n"
        "- `layer`: \n"
        "- `source_project`: \n"
        "- `source_model`: \n"
        "- `confidence`: working-hypothesis\n\n"
        "## 摘要\n\n"
        f"{summary_line}\n\n"
        "## Source Request / 来源请求\n\n"
        f"- {text}\n\n"
        "## Observation / 观察\n\n"
        "- 待补充。\n\n"
        "## Interpretation / 解释\n\n"
        "- 待补充。\n\n"
        "## Action / 动作\n\n"
        "1. 待补充。\n\n"
        "## Evidence / 最小证据\n\n"
        "- 待补充。\n\n"
        "## Verification / 复测判据\n\n"
        "- 待补充。\n\n"
        "## Suggested Writeback / 建议回写\n\n"
        "- `target_note`: \n"
        "- `reason`: 这是由 create-from-confirmation 自动创建的草稿，建议人工审阅后再并入正式知识。\n"
    )


def _slugify(text: str) -> str:
    compact = re.sub(r"[^0-9a-zA-Z\u4e00-\u9fff]+", "_", text).strip("_").lower()
    return compact or "capture"


def _resolve_draft_dir_for_domain(domain: str) -> Path:
    domain_dir = _resolve_domain_dir(domain)
    if domain_dir.exists():
        return domain_dir / "drafts"
    return DRAFTS_DIR


def _default_capture_title(text: str, layer: str) -> str:
    compact = re.sub(r"\s+", " ", text).strip()
    if len(compact) > 48:
        compact = compact[:45].rstrip() + "..."
    return f"{layer} | {compact}"


def _capture_list_or_default(values: list[str] | None, fallback: list[str]) -> list[str]:
    cleaned = [item.strip() for item in (values or []) if item.strip()]
    return cleaned or fallback


def _build_capture_markdown_draft(
    *,
    title: str,
    domain: str,
    layer: str,
    source_model: str,
    text: str,
    summary: str,
    best_entry: dict[str, Any] | None,
    observations: list[str],
    interpretations: list[str],
    actions: list[str],
    evidence: list[str],
    verification: list[str],
    suggested_writeback: dict[str, Any] | None,
) -> str:
    tags = "\n".join(
        [
            "  - knowledge-base",
            "  - capture",
            f"  - {domain}",
        ]
    )
    best_entry_lines: list[str] = []
    if best_entry:
        best_entry_lines.append(f"`file`: {best_entry.get('file', '')}")
        if best_entry.get("title"):
            best_entry_lines.append(f"`title`: {best_entry.get('title')}")
        if best_entry.get("layer"):
            best_entry_lines.append(f"`layer`: {best_entry.get('layer')}")
        for item in best_entry.get("recommended_action", [])[:3]:
            best_entry_lines.append(f"`recommended_action`: {item}")

    def _bullet_block(items: list[str]) -> str:
        return "\n".join(f"- {item}" for item in items) if items else "- 待补充。"

    def _ordered_block(items: list[str]) -> str:
        return "\n".join(f"{idx}. {item}" for idx, item in enumerate(items, start=1)) if items else "1. 待补充。"

    writeback_target = (suggested_writeback or {}).get("target", "")
    writeback_reason = (suggested_writeback or {}).get("reason", "")

    return (
        "---\n"
        f"title: {title}\n"
        "type: capture\n"
        f"domain: {domain}\n"
        "status: draft\n"
        "tags:\n"
        f"{tags}\n"
        "---\n\n"
        "# 标题\n\n"
        f"{title}\n\n"
        "## 元信息\n\n"
        "- `intent`: capture\n"
        f"- `domain`: {domain}\n"
        f"- `layer`: {layer}\n"
        "- `source_project`: local_kb\n"
        f"- `source_model`: {source_model}\n"
        "- `confidence`: working\n\n"
        "## 摘要\n\n"
        f"{summary}\n\n"
        "## Source Request / 来源请求\n\n"
        f"- {text}\n\n"
        "## Related Knowledge / 复用知识\n\n"
        f"{_bullet_block(best_entry_lines)}\n\n"
        "## Observation / 观察\n\n"
        f"{_bullet_block(observations)}\n\n"
        "## Interpretation / 解释\n\n"
        f"{_bullet_block(interpretations)}\n\n"
        "## Action / 动作\n\n"
        f"{_ordered_block(actions)}\n\n"
        "## Evidence / 最小证据\n\n"
        f"{_bullet_block(evidence)}\n\n"
        "## Verification / 复测判据\n\n"
        f"{_bullet_block(verification)}\n\n"
        "## Suggested Writeback / 建议回写\n\n"
        f"- `target_note`: {writeback_target}\n"
        f"- `reason`: {writeback_reason}\n"
    )


def _resolve_domain_dir(slug: str) -> Path:
    return DOMAINS_DIR / slug


def cmd_create_from_confirmation(args: argparse.Namespace) -> int:
    creation_type = args.creation_type
    if not args.confirm:
        payload = {
            "requires_confirmation": True,
            "message": "This command writes files only when --confirm is provided.",
            "suggested_creation_type": creation_type,
            "text": args.text,
        }
        _emit(payload, args.format)
        return 0

    created_files: list[str] = []

    if creation_type == "new-domain":
        slug = args.domain or _suggest_slug(args.text)
        domain_dir = _resolve_domain_dir(slug)
        domain_home = domain_dir / "README.md"
        drafts_dir = domain_dir / "drafts"
        if domain_home.exists():
            raise SystemExit(f"Domain already exists: {domain_home}")

        domain_dir.mkdir(parents=True, exist_ok=True)
        drafts_dir.mkdir(parents=True, exist_ok=True)
        content = _render_domain_home(slug=slug, title=args.title or slug, summary=args.summary or "")
        domain_home.write_text(content, encoding="utf-8")
        created_files.extend([str(domain_home), str(drafts_dir)])

        payload = {
            "created": True,
            "creation_type": creation_type,
            "domain": slug,
            "created_files": created_files,
            "next_steps": [
                "Review the new domain home note.",
                "Add seed notes or capture drafts under the new domain.",
                "Update kb_manifest.yaml if you want this domain to participate in keyword routing.",
            ],
        }
        _emit(payload, args.format)
        return 0

    if creation_type == "new-note":
        domain = args.domain
        if not domain:
            raise SystemExit("new-note requires --domain")

        domain_dir = _resolve_domain_dir(domain)
        if not domain_dir.exists():
            raise SystemExit(f"Domain does not exist: {domain_dir}")

        drafts_dir = domain_dir / "drafts"
        drafts_dir.mkdir(parents=True, exist_ok=True)
        title = args.title or args.text
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        note_name = f"{timestamp}_{_note_slug(title)}.md"
        note_path = drafts_dir / note_name
        if note_path.exists():
            raise SystemExit(f"Note already exists: {note_path}")

        content = _render_note_draft(domain=domain, title=title, text=args.text, summary=args.summary)
        note_path.write_text(content, encoding="utf-8")
        created_files.append(str(note_path))

        payload = {
            "created": True,
            "creation_type": creation_type,
            "domain": domain,
            "created_files": created_files,
            "next_steps": [
                "Review the draft note in Obsidian or your editor.",
                "Fill observation, interpretation, action, and evidence sections.",
                "Merge into a formal note after review.",
            ],
        }
        _emit(payload, args.format)
        return 0

    raise SystemExit(f"Unsupported creation type: {creation_type}")


def cmd_bootstrap_prompt(args: argparse.Namespace) -> int:
    if args.format == "text":
        sys.stdout.write(BOOTSTRAP_PROMPTS[args.style] + "\n")
        return 0
    _emit({"style": args.style, "prompt": BOOTSTRAP_PROMPTS[args.style]}, args.format)
    return 0


def cmd_intent(args: argparse.Namespace) -> int:
    manifest = _load_manifest()
    ranked = _pick_best(args.text, manifest.get("intent_routing", {}))
    payload = ranked[: args.top]
    _emit(payload, args.format)
    return 0


def cmd_route(args: argparse.Namespace) -> int:
    manifest = _load_manifest()
    domains = _pick_best(args.text, manifest.get("domain_routing", {}))
    intents = _pick_best(args.text, manifest.get("intent_routing", {}))
    top_domain = domains[0] if domains else None
    best_entry_payload = _build_best_entry_payload(manifest, args.text, max_entries=min(args.top, 5))
    governance_feedback = best_entry_payload.get("governance_feedback")
    payload = {
        "text": args.text,
        "intent": intents[0] if intents else None,
        "domains": domains[: args.top],
        "default_read_order": manifest.get("default_read_order", []),
        "best_entry": best_entry_payload.get("best_entry"),
        "related_entries": best_entry_payload.get("related_entries", []),
        "source_files": best_entry_payload.get("source_files", []),
        "suggested_next_read": best_entry_payload.get("suggested_next_read", []),
        "suggested_writeback": best_entry_payload.get("suggested_writeback"),
        "governance_feedback": governance_feedback,
        "fallback": best_entry_payload.get("fallback"),
        "creation_proposal": (
            None
            if domains
            or _is_governance_optimization_request(args.text, intents[0] if intents else None, best_entry_payload.get("best_entry"), governance_feedback)
            else _creation_proposal(manifest, args.text, top_domain, domains[: args.top])
        ),
    }
    _emit(payload, args.format)
    return 0


def cmd_best_entry(args: argparse.Namespace) -> int:
    manifest = _load_manifest()
    payload = _build_best_entry_payload(manifest, args.text, max_entries=args.max_entries)
    _emit(payload, args.format)
    return 0


def cmd_capture(args: argparse.Namespace) -> int:
    manifest = _load_manifest()
    best_payload = _build_best_entry_payload(manifest, args.text, max_entries=args.max_entries)

    top_domain = best_payload.get("domain")
    domain_name = args.domain or (top_domain or {}).get("name") or "shared"
    best_entry = best_payload.get("best_entry")
    layer = args.layer or (best_entry or {}).get("layer") or "governance"
    title = args.title or _default_capture_title(args.text, layer)
    summary = args.summary or f"围绕“{args.text}”整理的总库治理经验草稿。"

    observations = _capture_list_or_default(
        args.observation,
        [f"当前请求被识别为 `{((best_payload.get('intent') or {}).get('name') or 'unknown')}` 场景。"],
    )
    interpretations = _capture_list_or_default(
        args.interpretation,
        [f"当前优先复用了 `{(best_entry or {}).get('title', '暂无最优知识入口')}`。"],
    )
    actions = _capture_list_or_default(
        args.action,
        list((best_entry or {}).get("recommended_action", []))[:3] or ["按 suggested_next_read 继续阅读并人工审阅。"],
    )
    evidence = _capture_list_or_default(
        args.evidence,
        list((best_entry or {}).get("evidence", []))[:3] or [f"best_entry: {(best_entry or {}).get('file', 'N/A')}"],
    )
    verification = _capture_list_or_default(
        args.verification,
        ["人工审阅草稿后，再并入正式知识文档。"],
    )

    markdown_draft = _build_capture_markdown_draft(
        title=title,
        domain=domain_name,
        layer=layer,
        source_model=args.source_model,
        text=args.text,
        summary=summary,
        best_entry=best_entry,
        observations=observations,
        interpretations=interpretations,
        actions=actions,
        evidence=evidence,
        verification=verification,
        suggested_writeback=best_payload.get("suggested_writeback"),
    )

    payload = {
        "text": args.text,
        "title": title,
        "intent": best_payload.get("intent"),
        "domain": domain_name,
        "layer": layer,
        "best_entry": best_entry,
        "related_entries": best_payload.get("related_entries", []),
        "suggested_next_read": best_payload.get("suggested_next_read", []),
        "suggested_writeback": best_payload.get("suggested_writeback"),
        "governance_feedback": best_payload.get("governance_feedback"),
        "markdown_draft": markdown_draft,
        "requires_confirmation_for_write": bool(args.save_draft and not args.confirm),
    }

    if args.save_draft and args.confirm:
        draft_dir = _resolve_draft_dir_for_domain(domain_name)
        draft_dir.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        draft_path = draft_dir / f"{timestamp}_{_slugify(title)}.md"
        draft_path.write_text(markdown_draft, encoding="utf-8")
        payload["draft_file"] = str(draft_path)

    _emit(payload, args.format)
    return 0


def cmd_propose_create(args: argparse.Namespace) -> int:
    manifest = _load_manifest()
    domains = _pick_best(args.text, manifest.get("domain_routing", {}))
    top_domain = domains[0] if domains else None
    payload = _creation_proposal(manifest, args.text, top_domain if args.force_note else None, domains)
    if args.force_note and top_domain is None:
        payload["reason"] = "The request was forced into note creation, but no existing domain matched."
    _emit(payload, args.format)
    return 0


def _emit(payload: Any, fmt: str) -> None:
    if fmt == "json":
        json.dump(payload, sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")
        return
    if fmt == "compact":
        sys.stdout.write(json.dumps(payload, ensure_ascii=False, separators=(",", ":")) + "\n")
        return
    sys.stdout.write(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    bootstrap = subparsers.add_parser("bootstrap-prompt", help="Print the recommended bootstrap prompt.")
    bootstrap.add_argument("--style", choices=["full", "minimal"], default="full")
    bootstrap.add_argument("--format", choices=["text", "json", "compact"], default="text")
    bootstrap.set_defaults(func=cmd_bootstrap_prompt)

    intent = subparsers.add_parser("intent", help="Detect the user's high-level knowledge-base intent.")
    intent.add_argument("--text", required=True)
    intent.add_argument("--top", type=int, default=3)
    intent.add_argument("--format", choices=["text", "json", "compact"], default="json")
    intent.set_defaults(func=cmd_intent)

    route = subparsers.add_parser("route", help="Detect both user intent and likely domains.")
    route.add_argument("--text", required=True)
    route.add_argument("--top", type=int, default=3)
    route.add_argument("--format", choices=["text", "json", "compact"], default="json")
    route.set_defaults(func=cmd_route)

    best_entry = subparsers.add_parser("best-entry", help="Return the best matched knowledge entry from the workspace KB.")
    best_entry.add_argument("--text", required=True)
    best_entry.add_argument("--max-entries", type=int, default=3)
    best_entry.add_argument("--format", choices=["text", "json", "compact"], default="json")
    best_entry.set_defaults(func=cmd_best_entry)

    digest = subparsers.add_parser("digest", help="Emit a compact workspace KB digest for AI consumption.")
    digest.add_argument("--text", help="Route by text before digesting.")
    digest.add_argument("--file", help="Digest a specific markdown file.")
    digest.add_argument("--max-sections", type=int, default=3)
    digest.add_argument("--max-entries", type=int, default=3)
    digest.add_argument("--max-chars", type=int, default=220)
    digest.add_argument("--format", choices=["text", "json", "compact"], default="json")
    digest.set_defaults(func=cmd_digest)

    capture = subparsers.add_parser("capture", help="Build a governance capture draft for the workspace KB.")
    capture.add_argument("--text", required=True)
    capture.add_argument("--title")
    capture.add_argument("--summary")
    capture.add_argument("--domain")
    capture.add_argument("--layer")
    capture.add_argument("--source-model", default="gpt")
    capture.add_argument("--observation", action="append")
    capture.add_argument("--interpretation", action="append")
    capture.add_argument("--action", action="append")
    capture.add_argument("--evidence", action="append")
    capture.add_argument("--verification", action="append")
    capture.add_argument("--max-entries", type=int, default=3)
    capture.add_argument("--save-draft", action="store_true")
    capture.add_argument("--confirm", action="store_true")
    capture.add_argument("--format", choices=["text", "json", "compact"], default="json")
    capture.set_defaults(func=cmd_capture)

    propose = subparsers.add_parser("propose-create", help="Propose how to create new knowledge after user confirmation.")
    propose.add_argument("--text", required=True)
    propose.add_argument("--force-note", action="store_true", help="Force note-level proposal when a domain already exists.")
    propose.add_argument("--format", choices=["text", "json", "compact"], default="json")
    propose.set_defaults(func=cmd_propose_create)

    create = subparsers.add_parser(
        "create-from-confirmation",
        help="Create a new domain or note draft after the user has confirmed creation.",
    )
    create.add_argument("--creation-type", required=True, choices=["new-domain", "new-note"])
    create.add_argument("--text", required=True, help="Original user request or theme text.")
    create.add_argument("--domain", help="Domain slug. Required for new-note; optional for new-domain.")
    create.add_argument("--title", help="Display title for the created note or domain.")
    create.add_argument("--summary", help="Short summary for the created content.")
    create.add_argument("--confirm", action="store_true", help="Actually create files.")
    create.add_argument("--format", choices=["text", "json", "compact"], default="json")
    create.set_defaults(func=cmd_create_from_confirmation)

    return parser


def main() -> int:
    if not MANIFEST_PATH.exists():
        print(f"Manifest not found: {MANIFEST_PATH}", file=sys.stderr)
        return 1
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
