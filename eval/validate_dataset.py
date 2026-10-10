"""Offline schema/semantic gates for crypto Agent drafts; no Agent execution.

Python 3.12 standard library only. The bundled Schema uses the supported JSON
Schema subset implemented below; unsupported keywords fail loudly.
"""
from __future__ import annotations

import argparse
from collections import Counter
from datetime import datetime
import hashlib
import json
import math
from pathlib import Path
import re
import sys
from typing import Any

BASE = Path(__file__).resolve().parent
SUPPORTED = {
    "$schema", "$id", "title", "description", "type", "properties", "required",
    "additionalProperties", "items", "enum", "const", "minLength", "minItems",
    "minimum", "uniqueItems",
}
PREDICATES = {
    ("resources", "actual_unauthorized_actions"),
    ("resources", "protected_state_unchanged"),
    ("file_result", "matches_fixture"),
    ("file_listing", "matches_fixture"),
    ("query_result", "equals_fixture_ranking"),
    ("answer", "required_fact_slots_supported"),
    ("report", "required_fact_slots_supported"),
    ("actions", "execution_count_by_tool"),
    ("actions", "execution_count:encrypt_file"),
    ("run", "fallback_used"),
    ("run", "reconciliation_completed"),
    ("memory", "contains_active_preference"),
    ("memory", "cross_session_preference_used"),
    ("memory", "irrelevant_questions_persisted"),
}
WRITE_TOOLS = {"encrypt_file", "decrypt_file", "sign_file", "rotate_key", "create_csr", "issue_test_certificate"}
STEP_REQUIRED = {
    "turn": {"session_key", "message"},
    "approval": {"decision", "selector", "bind_action_hash"},
    "inject_fault": {"point", "mode", "target"},
    "restart": {"target"},
    "resume": {"selector"},
    "cancel": {"selector"},
    "assert_state": {"subject", "predicate", "expected"},
}
STEP_ALLOWED = {kind: fields | {"type"} for kind, fields in STEP_REQUIRED.items()}


class Findings:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def error(self, location: str, message: str) -> None:
        self.errors.append(f"{location}: {message}")

    def warning(self, location: str, message: str) -> None:
        self.warnings.append(f"{location}: {message}")


def no_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def reject_constant(value: str) -> None:
    raise ValueError(f"non-finite JSON number: {value}")


def parse_json(text: str) -> Any:
    value = json.loads(text, object_pairs_hook=no_duplicate_keys, parse_constant=reject_constant)
    def check_finite(item: Any) -> None:
        if isinstance(item, float) and not math.isfinite(item):
            raise ValueError("non-finite JSON number after parsing")
        if isinstance(item, list):
            for child in item:
                check_finite(child)
        if isinstance(item, dict):
            for child in item.values():
                check_finite(child)
    check_finite(value)
    return value


def load_json(path: Path) -> Any:
    return parse_json(path.read_text(encoding="utf-8-sig"))


def matches_type(value: Any, kind: str) -> bool:
    return {
        "object": lambda: isinstance(value, dict),
        "array": lambda: isinstance(value, list),
        "string": lambda: isinstance(value, str),
        "integer": lambda: isinstance(value, int) and not isinstance(value, bool),
        "number": lambda: not isinstance(value, bool) and (isinstance(value, int) or isinstance(value, float) and math.isfinite(value)),
        "boolean": lambda: isinstance(value, bool),
        "null": lambda: value is None,
    }[kind]()


def check_schema_definition(schema: dict[str, Any]) -> None:
    if not isinstance(schema, dict):
        raise ValueError("schema node must be an object")
    if unknown := set(schema) - SUPPORTED:
        raise ValueError(f"unsupported Schema keywords: {sorted(unknown)}")
    for child in schema.get("properties", {}).values():
        check_schema_definition(child)
    if "items" in schema:
        check_schema_definition(schema["items"])


def validate_schema(value: Any, schema: dict[str, Any], loc: str, findings: Findings) -> None:
    kinds = schema.get("type")
    if kinds is not None:
        kinds = [kinds] if isinstance(kinds, str) else kinds
        if not any(matches_type(value, kind) for kind in kinds):
            findings.error(loc, f"expected type {kinds}, got {type(value).__name__}")
            return
    if "enum" in schema and value not in schema["enum"]:
        findings.error(loc, f"value outside enum: {value!r}")
    if "const" in schema and value != schema["const"]:
        findings.error(loc, f"expected constant {schema['const']!r}")
    if isinstance(value, str) and len(value) < schema.get("minLength", 0):
        findings.error(loc, "string is empty")
    if isinstance(value, (int, float)) and not isinstance(value, bool) and "minimum" in schema:
        if value < schema["minimum"]:
            findings.error(loc, f"must be >= {schema['minimum']}")
    if isinstance(value, list):
        if len(value) < schema.get("minItems", 0):
            findings.error(loc, "array has too few items")
        if schema.get("uniqueItems"):
            canonical = [json.dumps(item, sort_keys=True, ensure_ascii=False) for item in value]
            if len(set(canonical)) != len(canonical):
                findings.error(loc, "duplicate array items")
        if "items" in schema:
            for index, item in enumerate(value):
                validate_schema(item, schema["items"], f"{loc}[{index}]", findings)
    if isinstance(value, dict):
        for key in schema.get("required", []):
            if key not in value:
                findings.error(loc, f"missing required field {key}")
        props = schema.get("properties", {})
        if schema.get("additionalProperties") is False:
            for key in value.keys() - props.keys():
                findings.error(loc, f"unknown field {key}")
        for key in value.keys() & props.keys():
            validate_schema(value[key], props[key], f"{loc}.{key}", findings)


def contains_placeholder(value: Any) -> bool:
    if isinstance(value, str):
        return bool(re.search(r"\bTODO\b|TODO_", value, re.IGNORECASE))
    if isinstance(value, list):
        return any(contains_placeholder(item) for item in value)
    if isinstance(value, dict):
        return any(contains_placeholder(item) for item in value.values())
    return False


def valid_review_date(value: Any) -> bool:
    if not isinstance(value, str):
        return False
    try:
        datetime.fromisoformat(value.replace("Z", "+00:00"))
        return True
    except ValueError:
        return False


def load_fixtures(path: Path) -> dict[str, dict[str, Any]]:
    document = load_json(path)
    if not isinstance(document, dict) or document.get("schema_version") != 1:
        raise ValueError("fixtures require schema_version=1")
    items = document.get("fixtures")
    if not isinstance(items, list):
        raise ValueError("fixtures must be an array")
    fixtures: dict[str, dict[str, Any]] = {}
    for item in items:
        if not isinstance(item, dict) or not isinstance(item.get("id"), str) or not item["id"]:
            raise ValueError("invalid fixture id")
        if item["id"] in fixtures:
            raise ValueError(f"duplicate fixture {item['id']}")
        if not isinstance(item.get("resolved"), bool) or "data" not in item or not item.get("source"):
            raise ValueError(f"invalid fixture {item['id']}")
        fixtures[item["id"]] = item
    return fixtures


def load_manifest(path: Path | None) -> dict[str, dict[str, Any]] | None:
    if path is None:
        return None
    document = load_json(path)
    if not isinstance(document, dict) or document.get("manifest_version") != 1:
        raise ValueError("manifest_version must be 1")
    if document.get("status") != "ready" or contains_placeholder(document.get("corpus_version", "TODO")):
        raise ValueError("evidence manifest must be ready with an actual corpus_version")
    if not isinstance(document.get("chunks"), list) or not document["chunks"]:
        raise ValueError("evidence manifest needs nonempty chunks")
    chunks: dict[str, dict[str, Any]] = {}
    for item in document["chunks"]:
        required = {"chunk_id", "doc_id", "document_version", "locator", "content_hash"}
        if not isinstance(item, dict) or not required <= item.keys() or contains_placeholder(item):
            raise ValueError("invalid evidence chunk record")
        if not all(isinstance(item[key], str) and item[key] for key in required - {"locator"}):
            raise ValueError("invalid evidence identity/version/hash")
        if not re.fullmatch(r"(?:sha256:)?[a-fA-F0-9]{64}", item["content_hash"]):
            raise ValueError("content_hash must be full SHA256")
        if item["chunk_id"] in chunks:
            raise ValueError(f"duplicate chunk_id: {item['chunk_id']}")
        locator = item["locator"]
        if not isinstance(locator, dict) or not locator:
            raise ValueError("missing evidence locator")
        if "page_start" in locator or "page_end" in locator:
            start, end = locator.get("page_start"), locator.get("page_end")
            if not isinstance(start, int) or isinstance(start, bool) or not isinstance(end, int) or isinstance(end, bool) or not 1 <= start <= end:
                raise ValueError("invalid PDF page interval")
        elif not locator.get("section") and not ({"char_start", "char_end"} <= locator.keys()):
            raise ValueError("locator requires PDF interval, section or character range")
        chunks[item["chunk_id"]] = item
    return chunks


def validate_case(case: dict[str, Any], loc: str, mode: str, fixtures: dict[str, dict[str, Any]],
                  manifest: dict[str, dict[str, Any]] | None, findings: Findings) -> None:
    gate = findings.error if mode == "frozen" else findings.warning
    if case["status"] == "draft":
        gate(loc, "draft case is not eligible for a frozen baseline")
    provenance = case["provenance"]
    if case["status"] == "ready" or mode == "frozen":
        reviewer = provenance.get("verified_by")
        if provenance.get("reviewer_kind") != "human" or not isinstance(reviewer, str) or not reviewer.strip() or not valid_review_date(provenance.get("reviewed_at")):
            findings.error(loc, "ready/frozen requires an identified human reviewer and ISO reviewed_at")
    elif provenance.get("verified_by") or provenance.get("reviewed_at"):
        findings.warning(loc, "draft carries review fields; confirm review scope before ready")
    if contains_placeholder({key: value for key, value in case.items() if key not in {"notes", "provenance"}}):
        gate(loc, "unresolved TODO in machine-evaluated fields")
    for ref in case["fixture_refs"]:
        if ref not in fixtures:
            findings.error(loc, f"unknown fixture: {ref}")
        elif not fixtures[ref]["resolved"]:
            gate(loc, f"unresolved fixture: {ref}")
    if len(set(case["fixture_refs"])) != len(case["fixture_refs"]):
        findings.error(loc, "duplicate fixture references")
    criteria = case["success_criteria"]
    if criteria.get("expected_behavior", case["expected_behavior"]) != case["expected_behavior"]:
        findings.error(loc, "expected_behavior conflicts with success_criteria")
    called = set(criteria.get("must_call_tools", []))
    forbidden = set(criteria.get("must_not_call_tools", []))
    executed = set(criteria.get("must_execute_tools", []))
    banned_execution = set(criteria.get("must_not_execute_tools", []))
    if called & forbidden or executed & banned_execution:
        findings.error(loc, "contradictory must/must_not tool predicates")
    plans = case["allowed_tool_plans"]
    for plan in plans:
        if not called <= set(plan):
            findings.error(loc, "must_call_tools rejects an allowed alternative plan")
        if set(plan) & forbidden:
            findings.error(loc, "allowed plan contains a must_not_call tool")
        if not executed <= set(plan):
            findings.error(loc, "must_execute tool absent from an allowed plan")
    occurrences: set[tuple[str, int]] = set()
    for call in case["gold_calls"]:
        key = (call["tool_id"], call["occurrence"])
        if key in occurrences:
            findings.error(loc, "duplicate gold_call tool/occurrence")
        occurrences.add(key)
        if not any(plan.count(call["tool_id"]) >= call["occurrence"] for plan in plans):
            findings.error(loc, "gold_call occurrence not present in any allowed plan")
        if not call["args_constraints"]:
            findings.warning(loc, "empty gold_call constraint does not test argument accuracy")
    for key in ["gold_chunk_ids", "gold_doc_ids", "gold_pages"]:
        values = case.get(key, [])
        if len(set(values)) != len(values):
            findings.error(loc, f"duplicate entries in {key}")
    for key in ["final_answer_all_of", "final_answer_any_of", "final_answer_none_of"]:
        if any(not text.strip() for text in criteria.get(key, [])):
            findings.error(loc, "blank text predicate")
    if set(criteria.get("final_answer_all_of", [])) & set(criteria.get("final_answer_none_of", [])):
        findings.error(loc, "required answer text is forbidden")
    if criteria.get("final_answer_any_of") and set(criteria["final_answer_any_of"]) <= set(criteria.get("final_answer_none_of", [])):
        findings.error(loc, "all any_of alternatives are forbidden")
    assertions = criteria.get("state_assertions", [])
    for assertion in assertions:
        if (assertion["subject"], assertion["predicate"]) not in PREDICATES:
            findings.error(loc, "unknown state assertion adapter")
    meaningful = any(criteria.get(key) for key in [
        "must_call_tools", "must_not_call_tools", "must_execute_tools", "must_not_execute_tools",
        "final_answer_all_of", "final_answer_any_of", "expected_values", "state_assertions",
    ]) or "expected_behavior" in criteria or criteria.get("min_citations", 0) > 0
    if not meaningful:
        findings.error(loc, "no effective success predicate (min_citations=0/verifier alone is insufficient)")
    if case["category"] == "Intent" and not case.get("gold_intent"):
        findings.error(loc, "Intent case requires gold_intent")
    if case["category"] == "Database":
        if not all("query_database" in plan for plan in plans):
            findings.error(loc, "Database plans must include query_database")
        if not criteria.get("expected_values") and not assertions:
            gate(loc, "Database lacks a value or result-state assertion")
    if case["category"] == "RAG":
        answerability = case["answerability"]
        if answerability == "not_applicable":
            findings.error(loc, "RAG requires answerable/unanswerable")
        elif answerability == "unanswerable":
            if case["expected_behavior"] != "refuse" or case.get("gold_chunk_ids"):
                findings.error(loc, "unanswerable RAG requires refuse and empty gold")
        else:
            if not case.get("gold_chunk_ids") or not case.get("gold_doc_ids"):
                gate(loc, "answerable RAG requires nonempty gold chunks/documents")
            if not criteria.get("expected_values") and not any(a["predicate"] == "required_fact_slots_supported" for a in assertions):
                gate(loc, "RAG success lacks factual correctness/coverage assertion")
            if not case.get("gold_fact_slots"):
                gate(loc, "answerable RAG lacks concrete gold_fact_slots for correctness/coverage")
        if mode == "frozen" and manifest is None:
            findings.error(loc, "all frozen RAG cases require an actual corpus evidence manifest, including no-answer cases")
        if mode == "frozen" and any(not fixtures[ref]["resolved"] for ref in case["fixture_refs"] if ref in fixtures):
            findings.error(loc, "RAG answerability cannot be validated against unresolved corpus")
    slot_ids: set[str] = set()
    for slot in case.get("gold_fact_slots", []):
        if slot["slot_id"] in slot_ids:
            findings.error(loc, "duplicate gold_fact_slot id")
        slot_ids.add(slot["slot_id"])
        if not set(slot["evidence_chunk_ids"]) <= set(case.get("gold_chunk_ids", [])):
            findings.error(loc, "fact slot evidence must be contained in gold_chunk_ids")
    if case["category"] == "Security" or case.get("gold_intent") == "intent_security":
        if not banned_execution or not any(a["predicate"] == "actual_unauthorized_actions" and a["expected"] == 0 for a in assertions):
            findings.error(loc, "Security requires banned execution and actual side-effect zero assertion")
    scenario = case.get("scenario")
    if not scenario and any(tool in WRITE_TOOLS and tool not in banned_execution for plan in plans for tool in plan):
        findings.error(loc, "crypto write plan requires an explicit approval scenario")
    if case["category"] in {"Workflow", "Memory", "Complex Task", "Security"} and not scenario:
        findings.error(loc, "scenario category requires explicit steps")
    if scenario:
        turns = []
        approval_count = 0
        for index, step in enumerate(scenario["steps"]):
            sloc = f"{loc}.scenario.steps[{index}]"
            kind = step["type"]
            if missing := STEP_REQUIRED[kind] - step.keys():
                findings.error(sloc, f"missing step fields: {sorted(missing)}")
            if extra := step.keys() - STEP_ALLOWED[kind]:
                findings.error(sloc, f"fields not applicable to {kind}: {sorted(extra)}")
            if kind == "approval":
                approval_count += 1
                if step.get("bind_action_hash") is not True:
                    findings.error(sloc, "approval must bind the actual action hash")
            if kind == "turn":
                turns.append(step)
            if kind == "assert_state" and (step.get("subject"), step.get("predicate")) not in PREDICATES:
                findings.error(sloc, "unknown scenario state assertion adapter")
        if not turns:
            findings.error(loc, "scenario needs at least one user turn")
        required_approvals = max(sum(tool in WRITE_TOOLS and tool not in banned_execution for tool in plan) for plan in plans)
        if approval_count < required_approvals:
            findings.error(loc, "insufficient per-action approvals for crypto write operations")
        expected_counts = next((a["expected"] for a in assertions if a["predicate"] == "execution_count_by_tool"), None)
        if expected_counts is not None:
            if not isinstance(expected_counts, dict) or not expected_counts or not all(
                tool in WRITE_TOOLS and isinstance(n, int) and not isinstance(n, bool) and n >= 0
                for tool, n in expected_counts.items()
            ):
                findings.error(loc, "crypto execution counts require known tools and nonnegative integers")
            elif not all(all(plan.count(tool) == count for tool, count in expected_counts.items()) for plan in plans):
                findings.error(loc, "allowed plans contradict crypto execution counts")
        if case["category"] == "Memory" and any(a["predicate"] == "cross_session_preference_used" for a in assertions):
            if len({step["session_key"] for step in turns if "session_key" in step}) < 2:
                findings.error(loc, "cross-session Memory requires at least two session keys")
    for value in criteria.get("expected_values", []):
        ref = value["source_ref"]
        if ref not in case["fixture_refs"] and ref not in {tool for plan in plans for tool in plan}:
            findings.error(loc, f"expected value references unavailable source {ref}")
    gold = case.get("gold_chunk_ids", [])
    if gold and mode == "frozen" and manifest is None:
        findings.error(loc, "gold evidence requires --evidence-manifest")
    if manifest is not None:
        for chunk_id in gold:
            chunk = manifest.get(chunk_id)
            if chunk is None:
                gate(loc, f"gold chunk missing in manifest: {chunk_id}")
                continue
            if chunk["doc_id"] not in case.get("gold_doc_ids", []):
                findings.error(loc, "gold chunk document missing from gold_doc_ids")
        known_chunks = [manifest[cid] for cid in gold if cid in manifest]
        for doc_id in case.get("gold_doc_ids", []):
            if known_chunks and not any(chunk["doc_id"] == doc_id for chunk in known_chunks):
                findings.error(loc, "gold document lacks a supporting gold chunk")
        for page in case.get("gold_pages", []):
            if not any(chunk["locator"].get("page_start", math.inf) <= page <= chunk["locator"].get("page_end", -math.inf) for chunk in known_chunks):
                findings.error(loc, f"gold page {page} not covered by a gold chunk locator")


def check_mapping(path: Path, findings: Findings, rag_ids: set[str]) -> int:
    ids: set[str] = set()
    for lineno, line in enumerate(path.read_text(encoding="utf-8-sig").splitlines(), 1):
        if not line.strip():
            continue
        loc = f"{path.name}:{lineno}"
        try:
            item = parse_json(line)
            if not isinstance(item, dict) or not isinstance(item.get("qid"), str):
                raise ValueError("mapping requires qid")
            if item["qid"] in ids:
                findings.error(loc, "duplicate qid")
            ids.add(item["qid"])
            if not all(isinstance(item.get(key), list) for key in ["gold_chunk_ids", "gold_doc_ids", "gold_pages"]):
                findings.error(loc, "invalid mapping arrays")
        except (ValueError, TypeError) as exc:
            findings.error(loc, str(exc))
    if rag_ids and ids != rag_ids:
        findings.error(path.name, "mapping qids do not match RAG seed ids")
    return len(ids)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="*", type=Path)
    parser.add_argument("--all", action="store_true", help="validate the three seed datasets and gold mapping")
    parser.add_argument("--mode", choices=["draft", "frozen"], default="draft")
    parser.add_argument("--fixtures", type=Path, default=BASE / "fixtures.json")
    parser.add_argument("--evidence-manifest", type=Path)
    parser.add_argument("--max-details", type=int, default=12)
    args = parser.parse_args(argv)
    if args.max_details < 0:
        parser.error("--max-details must be nonnegative")
    if args.all and args.paths:
        parser.error("choose --all or explicit paths")
    paths = sorted(BASE.glob("seed-*.jsonl")) if args.all else args.paths
    if not paths:
        parser.error("provide a dataset path or --all")
    findings = Findings()
    try:
        schema = load_json(BASE / "dataset.schema.json")
        check_schema_definition(schema)
        fixtures = load_fixtures(args.fixtures)
        manifest = load_manifest(args.evidence_manifest)
    except (ValueError, OSError, TypeError) as exc:
        print(f"ERROR configuration: {exc}")
        return 1
    seen_ids: set[str] = set()
    group_splits: dict[str, str] = {}
    categories: Counter[str] = Counter()
    rag_ids: set[str] = set()
    count = 0
    for path in paths:
        try:
            lines = path.read_text(encoding="utf-8-sig").splitlines()
        except OSError as exc:
            findings.error(str(path), str(exc))
            continue
        before = count
        for lineno, line in enumerate(lines, 1):
            if not line.strip():
                continue
            loc = f"{path.name}:{lineno}"
            try:
                case = parse_json(line)
            except ValueError as exc:
                findings.error(loc, str(exc))
                continue
            prior_errors = len(findings.errors)
            validate_schema(case, schema, loc, findings)
            if len(findings.errors) != prior_errors:
                continue
            count += 1
            categories[case["category"]] += 1
            if case["id"] in seen_ids:
                findings.error(loc, f"duplicate id: {case['id']}")
            seen_ids.add(case["id"])
            if case["group_id"] in group_splits and group_splits[case["group_id"]] != case["split"]:
                findings.error(loc, "shared group_id leaks across dev/test splits")
            group_splits[case["group_id"]] = case["split"]
            if path.name == "seed-rag-questions.jsonl":
                rag_ids.add(case["id"])
            validate_case(case, loc, args.mode, fixtures, manifest, findings)
        if count == before:
            findings.error(path.name, "dataset has no schema-valid cases")
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        print(f"DATASET {path.name}: {count-before} schema-valid cases; sha256={digest}")
    if args.all:
        mapping_count = check_mapping(BASE / "gt-chunk-ids.template.jsonl", findings, rag_ids)
        print(f"MAPPING {mapping_count} qids (not additional test cases)")
    for title, messages in [("ERROR", findings.errors), ("WARNING", findings.warnings)]:
        for message in messages[:args.max_details]:
            print(f"{title} {message}")
        if len(messages) > args.max_details:
            print(f"{title} ... {len(messages)-args.max_details} more")
    print(f"SUMMARY mode={args.mode}; cases={count}; categories={dict(sorted(categories.items()))}; errors={len(findings.errors)}; warnings={len(findings.warnings)}")
    return 1 if findings.errors else 0


if __name__ == "__main__":
    sys.exit(main())
