from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

from .rag_baseline import DOMAIN_DOCS, ROOT, TARGET_RESPONSES, load_benign_docs, load_test_cases
from .research_alignment import ATTACK_CATEGORY_TO_AXIS, summarize_alignment


REQUIRED_FIELDS = [
    "case_id",
    "domain",
    "attack_category",
    "language_style",
    "user_question",
    "trusted_doc",
    "injected_doc_id",
    "injected_text",
    "expected_safe_behavior",
    "target_behavior",
    "severity",
]

ALLOWED_LANGUAGE_STYLES = {"vi", "vi_en", "en"}
ALLOWED_SEVERITIES = {"low", "medium", "high"}


def validate_cases(cases: list[dict]) -> tuple[dict, list[str]]:
    benign_docs = load_benign_docs()
    errors: list[str] = []

    case_ids = [case.get("case_id", "") for case in cases]
    injected_ids = [case.get("injected_doc_id", "") for case in cases]
    duplicate_case_ids = sorted(item for item, count in Counter(case_ids).items() if item and count > 1)
    duplicate_injected_ids = sorted(item for item, count in Counter(injected_ids).items() if item and count > 1)

    for case in cases:
        case_id = case.get("case_id", "<missing case_id>")
        for field in REQUIRED_FIELDS:
            if not case.get(field):
                errors.append(f"{case_id}: missing required field '{field}'")

        domain = case.get("domain")
        if domain and domain not in DOMAIN_DOCS:
            errors.append(f"{case_id}: unknown domain '{domain}'")

        trusted_doc = case.get("trusted_doc")
        if trusted_doc and trusted_doc not in benign_docs:
            errors.append(f"{case_id}: trusted_doc '{trusted_doc}' does not exist in data/benign_docs")

        target_behavior = case.get("target_behavior")
        if target_behavior and target_behavior not in TARGET_RESPONSES:
            errors.append(f"{case_id}: target_behavior '{target_behavior}' has no simulated target response")

        attack_category = case.get("attack_category")
        if attack_category and attack_category not in ATTACK_CATEGORY_TO_AXIS:
            errors.append(f"{case_id}: attack_category '{attack_category}' has no research-axis mapping")

        language_style = case.get("language_style")
        if language_style and language_style not in ALLOWED_LANGUAGE_STYLES:
            errors.append(f"{case_id}: unsupported language_style '{language_style}'")

        severity = case.get("severity")
        if severity and severity not in ALLOWED_SEVERITIES:
            errors.append(f"{case_id}: unsupported severity '{severity}'")

    for case_id in duplicate_case_ids:
        errors.append(f"duplicate case_id '{case_id}'")
    for injected_id in duplicate_injected_ids:
        errors.append(f"duplicate injected_doc_id '{injected_id}'")

    summary = {
        "cases": len(cases),
        "domains": dict(sorted(Counter(case["domain"] for case in cases if case.get("domain")).items())),
        "attack_categories": dict(sorted(Counter(case["attack_category"] for case in cases if case.get("attack_category")).items())),
        "research_alignment": summarize_alignment(cases),
        "language_styles": dict(sorted(Counter(case["language_style"] for case in cases if case.get("language_style")).items())),
        "severities": dict(sorted(Counter(case["severity"] for case in cases if case.get("severity")).items())),
        "errors": errors,
    }
    return summary, errors


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate the Vietnamese RAG prompt-injection JSONL dataset.")
    parser.add_argument("--cases", type=Path, default=ROOT / "data" / "test_cases.jsonl")
    args = parser.parse_args()

    cases = load_test_cases(args.cases)
    summary, errors = validate_cases(cases)
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    if errors:
        sys.exit(1)


if __name__ == "__main__":
    main()
