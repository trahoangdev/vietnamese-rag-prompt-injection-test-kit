from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from .metrics import judge_case, summarize
from .rag_baseline import ROOT, load_test_cases
from .research_alignment import research_axis_for_case


def regrade_results(results_path: Path, out_path: Path | None = None) -> dict:
    cases = {case["case_id"]: case for case in load_test_cases()}
    target_path = out_path or results_path

    with results_path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        fieldnames = reader.fieldnames or []
        rows = list(reader)

    if "research_axis" not in fieldnames:
        insert_at = fieldnames.index("language_style") if "language_style" in fieldnames else len(fieldnames)
        fieldnames = fieldnames[:insert_at] + ["research_axis"] + fieldnames[insert_at:]

    for row in rows:
        case = cases[row["case_id"]]
        row["research_axis"] = research_axis_for_case(case)
        judged = judge_case(case, row["response"])
        row.update(judged)

    with target_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    summary = summarize(rows)
    summary_path = target_path.with_suffix(".summary.json")
    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description="Re-grade saved result CSV rows from stored model responses.")
    parser.add_argument("results", type=Path)
    parser.add_argument("--out", type=Path, default=None)
    args = parser.parse_args()

    summary = regrade_results(args.results, args.out)
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
