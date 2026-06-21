from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from .metrics import judge_case, summarize
from .rag_baseline import ROOT, load_test_cases, run_case


FIELDNAMES = [
    "case_id",
    "domain",
    "attack_category",
    "language_style",
    "severity",
    "mode",
    "retrieved_doc_ids",
    "attack_success",
    "useful_answer",
    "leakage",
    "citation_integrity",
    "grade",
    "response",
]


def evaluate(mode: str, out_path: Path, cases_path: Path | None = None) -> dict:
    cases = load_test_cases(cases_path)
    rows: list[dict] = []
    for case in cases:
        rag_response = run_case(case, mode=mode)
        judged = judge_case(case, rag_response.response)
        row = {
            "case_id": case["case_id"],
            "domain": case["domain"],
            "attack_category": case["attack_category"],
            "language_style": case["language_style"],
            "severity": case["severity"],
            "mode": mode,
            "retrieved_doc_ids": ";".join(rag_response.retrieved_doc_ids),
            "response": rag_response.response,
            **judged,
        }
        rows.append(row)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)

    summary = summarize(rows)
    summary_path = out_path.with_suffix(".summary.json")
    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate Vietnamese RAG prompt injection test cases.")
    parser.add_argument("--mode", choices=["baseline", "mitigated", "sanitized"], default="baseline")
    parser.add_argument("--out", type=Path, default=ROOT / "results" / "results.csv")
    parser.add_argument("--cases", type=Path, default=None)
    args = parser.parse_args()

    summary = evaluate(args.mode, args.out, args.cases)
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    print(f"Wrote results to {args.out}")
    print(f"Wrote summary to {args.out.with_suffix('.summary.json')}")


if __name__ == "__main__":
    main()

