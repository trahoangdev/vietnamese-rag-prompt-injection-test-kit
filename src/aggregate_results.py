from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from .rag_baseline import ROOT
from .research_alignment import research_axis_label


DEFAULT_SUMMARIES = [
    ("Baseline", ROOT / "results" / "baseline_results.summary.json"),
    ("Mitigated prompt", ROOT / "results" / "mitigation_results.summary.json"),
    ("Sanitized context", ROOT / "results" / "sanitized_results.summary.json"),
]

OPENAI_GPT54MINI_SUMMARIES = [
    ("GPT-5.4-mini baseline", ROOT / "results" / "openai_gpt54mini_baseline_results.summary.json"),
    ("GPT-5.4-mini mitigated", ROOT / "results" / "openai_gpt54mini_mitigated_results.summary.json"),
    ("GPT-5.4-mini sanitized", ROOT / "results" / "openai_gpt54mini_sanitized_results.summary.json"),
]


def fmt(value: float) -> str:
    return f"{value:.4f}"


def load_summary(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def load_rows(path: Path) -> list[dict]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def bool_value(value: str) -> bool:
    return value.strip().lower() == "true"


def grouped_rates(rows: list[dict], field: str) -> dict[str, dict]:
    groups: dict[str, list[dict]] = {}
    for row in rows:
        groups.setdefault(row[field], []).append(row)

    out = {}
    for key, items in sorted(groups.items()):
        n = len(items)
        out[key] = {
            "n": n,
            "attack_success_rate": sum(1 for row in items if bool_value(row["attack_success"])) / n if n else 0.0,
            "useful_answer_rate": sum(1 for row in items if bool_value(row["useful_answer"])) / n if n else 0.0,
        }
    return out


def failure_examples(rows: list[dict], limit: int = 5) -> list[dict]:
    selected = []
    seen_categories = set()
    for row in rows:
        if not bool_value(row["attack_success"]):
            continue
        category = row["attack_category"]
        if category in seen_categories:
            continue
        selected.append(row)
        seen_categories.add(category)
        if len(selected) >= limit:
            break
    return selected


def build_markdown(
    summaries: list[tuple[str, Path]],
    *,
    title: str = "Generated Results Tables",
    baseline_rows_path: Path = ROOT / "results" / "baseline_results.csv",
) -> str:
    loaded = [(label, load_summary(path)) for label, path in summaries]
    baseline_rows = load_rows(baseline_rows_path)
    lines: list[str] = []
    lines.append(f"# {title}")
    lines.append("")
    lines.append("## Overall")
    lines.append("")
    lines.append("| Mode | N | Attack Success Rate | Useful Answer Rate | Leakage Rate | Citation Integrity | Mean Grade |")
    lines.append("|---|---:|---:|---:|---:|---:|---:|")
    for label, summary in loaded:
        overall = summary["overall"]
        lines.append(
            "| "
            + " | ".join(
                [
                    label,
                    str(overall["n"]),
                    fmt(overall["attack_success_rate"]),
                    fmt(overall["useful_answer_rate"]),
                    fmt(overall["leakage_rate"]),
                    fmt(overall["citation_integrity_rate"]),
                    fmt(overall["mean_grade"]),
                ]
            )
            + " |"
        )

    if loaded:
        baseline = loaded[0][1]
        lines.append("")
        lines.append("## Baseline Attack Success by Category")
        lines.append("")
        lines.append("| Attack category | N | Attack Success Rate | Useful Answer Rate |")
        lines.append("|---|---:|---:|---:|")
        for category, values in baseline["by_attack_category"].items():
            lines.append(
                f"| {category} | {values['n']} | {fmt(values['attack_success_rate'])} | {fmt(values['useful_answer_rate'])} |"
            )

        if "by_research_axis" in baseline:
            lines.append("")
            lines.append("## Baseline Attack Success by Research Axis")
            lines.append("")
            lines.append("| Research axis | N | Attack Success Rate | Useful Answer Rate |")
            lines.append("|---|---:|---:|---:|")
            for axis, values in baseline["by_research_axis"].items():
                lines.append(
                    f"| {research_axis_label(axis)} | {values['n']} | {fmt(values['attack_success_rate'])} | {fmt(values['useful_answer_rate'])} |"
                )

        lines.append("")
        lines.append("## Baseline Attack Success by Domain")
        lines.append("")
        lines.append("| Domain | N | Attack Success Rate | Useful Answer Rate |")
        lines.append("|---|---:|---:|---:|")
        for domain, values in baseline["by_domain"].items():
            lines.append(
                f"| {domain} | {values['n']} | {fmt(values['attack_success_rate'])} | {fmt(values['useful_answer_rate'])} |"
            )

        lines.append("")
        lines.append("## Baseline Attack Success by Language Style")
        lines.append("")
        lines.append("| Language style | N | Attack Success Rate | Useful Answer Rate |")
        lines.append("|---|---:|---:|---:|")
        for style, values in grouped_rates(baseline_rows, "language_style").items():
            lines.append(
                f"| {style} | {values['n']} | {fmt(values['attack_success_rate'])} | {fmt(values['useful_answer_rate'])} |"
            )

        lines.append("")
        lines.append("## Qualitative Failure Examples")
        lines.append("")
        for row in failure_examples(baseline_rows):
            lines.append(f"### {row['case_id']} - {row['attack_category']} ({row['domain']}, {row['language_style']})")
            lines.append("")
            if row.get("research_axis"):
                lines.append(f"- Research axis: {research_axis_label(row['research_axis'])}")
            lines.append(f"- Baseline response: {row['response']}")
            lines.append(f"- Auto grade: {row['grade']}")
            lines.append(f"- Interpretation: baseline response followed the injected target behavior for this category.")
            lines.append("")

    lines.append("")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Aggregate result summary JSON files into Markdown tables.")
    parser.add_argument("--profile", choices=["deterministic", "openai-gpt54mini"], default="deterministic")
    parser.add_argument("--out", type=Path, default=ROOT / "results" / "GENERATED_TABLES.md")
    args = parser.parse_args()

    if args.profile == "openai-gpt54mini":
        markdown = build_markdown(
            OPENAI_GPT54MINI_SUMMARIES,
            title="OpenAI GPT-5.4-mini Results Tables",
            baseline_rows_path=ROOT / "results" / "openai_gpt54mini_baseline_results.csv",
        )
    else:
        markdown = build_markdown(DEFAULT_SUMMARIES)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(markdown, encoding="utf-8")
    print(f"Wrote {args.out}")


if __name__ == "__main__":
    main()
