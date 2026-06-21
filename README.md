# Vietnamese RAG Prompt Injection Test Kit

A small defensive benchmark for testing document-level prompt injection in Vietnamese retrieval-augmented generation (RAG) chatbots.

This project was designed for the Global South AI Safety Hackathon 2026, Asia Track, Technical Safety sub-track. It focuses on a practical deployment risk: Vietnamese RAG systems often retrieve semi-trusted text from HR policies, public-service FAQs, school rules, banking support pages, clinic information, and customer-support documents. If an attacker can place malicious instructions inside a retrieved document, the chatbot may follow those instructions instead of the system prompt.

## What This Contains

- Synthetic Vietnamese document corpus across six practical domains.
- A JSONL test set for Vietnamese and Vietnamese-English code-switching prompt injection.
- A simple lexical RAG baseline.
- Lightweight mitigation baselines:
  - instruction-hierarchy prompt
  - context sanitizer
- Deterministic simulated model mode for reproducible hackathon results without API keys.
- Evaluation scripts that output CSV and summary JSON.
- A deployer checklist and report draft skeleton.

## Quick Start

From the repository root:

```powershell
cd "Vietnamese_RAG_Prompt_Injection_Test_Kit"
python -m src.evaluate --mode baseline --out results/baseline_results.csv
python -m src.evaluate --mode mitigated --out results/mitigation_results.csv
python -m src.evaluate --mode sanitized --out results/sanitized_results.csv
```

If you are already inside the project folder, run the evaluation commands directly:

```powershell
python -m src.evaluate --mode baseline --out results/baseline_results.csv
python -m src.evaluate --mode mitigated --out results/mitigation_results.csv
python -m src.evaluate --mode sanitized --out results/sanitized_results.csv
```

If `python` is not available on Windows, try the Python launcher:

```powershell
py -m src.evaluate --mode baseline --out results/baseline_results.csv
```

## Modes

- `baseline`: RAG prompt places retrieved context in the prompt and the simulated model follows document-level injection when it detects it.
- `mitigated`: Adds a stronger instruction hierarchy and treats retrieved documents as untrusted evidence.
- `sanitized`: Removes likely injection lines from retrieved context before answering.

## Output

Each evaluation row includes:

- `case_id`
- `domain`
- `attack_category`
- `language_style`
- `mode`
- `retrieved_doc_ids`
- `attack_success`
- `useful_answer`
- `leakage`
- `citation_integrity`
- `grade`
- `response`

The summary JSON reports attack success rate, useful answer rate, leakage rate, and citation integrity by mode and attack category.

## Research Question

How vulnerable are Vietnamese-language RAG chatbots to document-level prompt injection, and can lightweight mitigations reduce attack success without destroying answer usefulness?

## Scope

This is a defensive benchmark prototype. It uses synthetic documents and does not target real systems. The examples are intentionally simplified so builders and reviewers can reproduce the evaluation quickly.
