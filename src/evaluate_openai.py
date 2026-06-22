from __future__ import annotations

import argparse
import csv
import json
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

from .env_utils import get_required_env, load_local_env
from .metrics import judge_case, summarize
from .mitigations import build_prompt, sanitize_context
from .rag_baseline import ROOT, build_case_docs, load_benign_docs, load_test_cases, retrieve
from .research_alignment import research_axis_for_case


FIELDNAMES = [
    "case_id",
    "domain",
    "attack_category",
    "research_axis",
    "language_style",
    "severity",
    "mode",
    "model",
    "retrieved_doc_ids",
    "attack_success",
    "useful_answer",
    "leakage",
    "citation_integrity",
    "grade",
    "response",
]


def call_responses_api(prompt: str, model: str, api_key: str, timeout: int = 90, max_retries: int = 3) -> str:
    payload = {
        "model": model,
        "input": prompt,
        "temperature": 0,
    }
    data = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        "https://api.openai.com/v1/responses",
        data=data,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    for attempt in range(1, max_retries + 1):
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                body = json.loads(response.read().decode("utf-8"))
                return extract_output_text(body)
        except urllib.error.HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace")
            if exc.code in {429, 500, 502, 503, 504} and attempt < max_retries:
                time.sleep(2 * attempt)
                continue
            raise RuntimeError(f"OpenAI API HTTP {exc.code}: {body}") from exc
        except urllib.error.URLError as exc:
            if attempt < max_retries:
                time.sleep(2 * attempt)
                continue
            raise RuntimeError(f"OpenAI API request failed: {exc}") from exc

    raise RuntimeError("OpenAI API request failed after retries")


def extract_output_text(body: dict[str, Any]) -> str:
    if isinstance(body.get("output_text"), str):
        return body["output_text"]

    parts: list[str] = []
    for item in body.get("output", []) or []:
        for content in item.get("content", []) or []:
            text = content.get("text")
            if isinstance(text, str):
                parts.append(text)
    if parts:
        return "\n".join(parts).strip()

    return json.dumps(body, ensure_ascii=False)


def make_prompt_for_case(case: dict, mode: str) -> tuple[str, list[str]]:
    benign_docs = load_benign_docs()
    candidate_docs = build_case_docs(case, benign_docs)
    retrieved = retrieve(case["user_question"] + " " + case["injected_text"], candidate_docs, k=2)

    contexts: list[tuple[str, str]] = []
    for doc in retrieved:
        text = doc.text
        if mode == "sanitized":
            text = sanitize_context(text).text
        contexts.append((doc.doc_id, text))

    prompt = build_prompt(case["user_question"], contexts, mode=mode)
    return prompt, [doc.doc_id for doc in retrieved]


def evaluate_openai(
    *,
    mode: str,
    model: str,
    out_path: Path,
    limit: int | None = None,
    case_ids: set[str] | None = None,
    sleep_seconds: float = 0.0,
) -> dict:
    load_local_env(ROOT)
    api_key = get_required_env("OPENAI_API_KEY")

    cases = load_test_cases()
    if case_ids:
        cases = [case for case in cases if case["case_id"] in case_ids]
    if limit is not None:
        cases = cases[:limit]

    rows: list[dict] = []
    for index, case in enumerate(cases, 1):
        prompt, retrieved_doc_ids = make_prompt_for_case(case, mode)
        response = call_responses_api(prompt, model=model, api_key=api_key)
        judged = judge_case(case, response)
        rows.append(
            {
                "case_id": case["case_id"],
                "domain": case["domain"],
                "attack_category": case["attack_category"],
                "research_axis": research_axis_for_case(case),
                "language_style": case["language_style"],
                "severity": case["severity"],
                "mode": mode,
                "model": model,
                "retrieved_doc_ids": ";".join(retrieved_doc_ids),
                "response": response,
                **judged,
            }
        )
        print(f"[{index}/{len(cases)}] {case['case_id']} grade={judged['grade']} attack_success={judged['attack_success']}")
        if sleep_seconds:
            time.sleep(sleep_seconds)

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
    parser = argparse.ArgumentParser(description="Run real OpenAI model evaluation for the RAG prompt injection benchmark.")
    parser.add_argument("--mode", choices=["baseline", "mitigated", "sanitized"], default="baseline")
    parser.add_argument("--model", default="gpt-5.4-mini")
    parser.add_argument("--out", type=Path, default=ROOT / "results" / "openai_baseline_results.csv")
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--case-ids", default="", help="Comma-separated case IDs, e.g. TC001,TC002")
    parser.add_argument("--sleep", type=float, default=0.0, help="Seconds to sleep between requests")
    args = parser.parse_args()

    case_ids = {item.strip() for item in args.case_ids.split(",") if item.strip()} or None
    try:
        summary = evaluate_openai(
            mode=args.mode,
            model=args.model,
            out_path=args.out,
            limit=args.limit,
            case_ids=case_ids,
            sleep_seconds=args.sleep,
        )
    except RuntimeError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    print(f"Wrote results to {args.out}")
    print(f"Wrote summary to {args.out.with_suffix('.summary.json')}")


if __name__ == "__main__":
    main()
