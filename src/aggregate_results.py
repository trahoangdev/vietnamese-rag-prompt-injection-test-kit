from __future__ import annotations

import argparse
import json
from pathlib import Path

from .rag_baseline import ROOT


DEFAULT_SUMMARIES = [
    ("Baseline", ROOT / "results" / "baseline_results.summary.json"),
    ("Mitigated prompt", ROOT / "results" / "mitigation_results.summary.json"),
    ("Sanitized context", ROOT / "results" / "sanitized_results.summary.json"),
]


def fmt(value: float) -> str:
    return f"{value:.4f}"


def load_summary(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def build_markdown(summaries: list[tuple[str, Path]]) -> str:
    loaded = [(label, load_summary(path)) for label, path in summaries]
    lines: list[str] = []
    lines.append("# Generated Results Tables")
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
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Aggregate result summary JSON files into Markdown tables.")
    parser.add_argument("--out", type=Path, default=ROOT / "results" / "GENERATED_TABLES.md")
    args = parser.parse_args()

    markdown = build_markdown(DEFAULT_SUMMARIES)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(markdown, encoding="utf-8")
    print(f"Wrote {args.out}")


if __name__ == "__main__":
    main()

