from __future__ import annotations

import argparse
import csv
from pathlib import Path

from .rag_baseline import ROOT, load_test_cases


FIELDNAMES = [
    "case_id",
    "domain",
    "attack_category",
    "language_style",
    "severity",
    "user_question",
    "injected_text",
    "expected_safe_behavior",
    "auto_attack_success",
    "auto_useful_answer",
    "auto_grade",
    "response",
    "manual_attack_success",
    "manual_useful_answer",
    "manual_grade",
    "reviewer_notes",
]


def load_results(path: Path) -> dict[str, dict]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return {row["case_id"]: row for row in csv.DictReader(handle)}


def export_review_sample(results_path: Path, out_path: Path, limit: int | None = None) -> int:
    cases = {case["case_id"]: case for case in load_test_cases()}
    results = load_results(results_path)

    rows = []
    for case_id in sorted(results):
        case = cases[case_id]
        result = results[case_id]
        rows.append(
            {
                "case_id": case_id,
                "domain": case["domain"],
                "attack_category": case["attack_category"],
                "language_style": case["language_style"],
                "severity": case["severity"],
                "user_question": case["user_question"],
                "injected_text": case["injected_text"],
                "expected_safe_behavior": case["expected_safe_behavior"],
                "auto_attack_success": result["attack_success"],
                "auto_useful_answer": result["useful_answer"],
                "auto_grade": result["grade"],
                "response": result["response"],
                "manual_attack_success": "",
                "manual_useful_answer": "",
                "manual_grade": "",
                "reviewer_notes": "",
            }
        )

    if limit is not None:
        rows = rows[:limit]

    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)
    return len(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description="Export a CSV for manual review of model responses.")
    parser.add_argument("--results", type=Path, default=ROOT / "results" / "baseline_results.csv")
    parser.add_argument("--out", type=Path, default=ROOT / "results" / "manual_review_baseline.csv")
    parser.add_argument("--limit", type=int, default=None)
    args = parser.parse_args()

    n = export_review_sample(args.results, args.out, args.limit)
    print(f"Wrote {n} rows to {args.out}")


if __name__ == "__main__":
    main()

