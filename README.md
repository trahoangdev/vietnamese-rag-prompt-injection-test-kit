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
- Real-model OpenAI runner and stored GPT-5.4-mini result artifacts.
- Evaluation scripts that output CSV and summary JSON.
- Dataset schema documentation and a validation command.
- Research-axis mapping tied to newer RAG poisoning, prompt-injection benchmark, multilingual safety, and Southeast Asian safety literature.
- A deployer checklist, submission checklist, and regenerated PDF report draft.

## Research Alignment

The benchmark is organized around six research axes drawn from the updated literature review:

- Indirect instruction takeover: retrieved text competes with system/user intent.
- RAG knowledge poisoning: poisoned snippets steer or distract retrieval-grounded answers.
- Data privacy and prompt leakage: injected documents request hidden prompts or sensitive records.
- Source and citation integrity: poisoned documents attempt to become the cited authority.
- Multilingual and code-switching safety: Vietnamese-English instructions test language-sensitive failure modes.
- Sensitive-domain policy failure: health, education, finance, HR, and public-service failures have higher impact.

See `docs/latest_research_review.md`, `docs/research_alignment_matrix.md`, and `docs/reference_mapping.md` for the detailed mapping to OWASP LLM01, PoisonedRAG, FilterRAG-style defenses, AgentDyn, LinguaSafe, and SEA-SafeguardBench.

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

## Dataset Validation

Validate the JSONL test set before running or modifying experiments:

```powershell
python -m src.validate_dataset
```

The dataset schema is documented in `docs/dataset_schema.md`.

## Modes

- `baseline`: RAG prompt places retrieved context in the prompt and the simulated model follows document-level injection when it detects it.
- `mitigated`: Adds a stronger instruction hierarchy and treats retrieved documents as untrusted evidence.
- `sanitized`: Removes likely injection lines from retrieved context before answering.

## Output

Each evaluation row includes:

- `case_id`
- `domain`
- `attack_category`
- `research_axis`
- `language_style`
- `severity`
- `mode`
- `retrieved_doc_ids`
- `attack_success`
- `useful_answer`
- `leakage`
- `citation_integrity`
- `grade`
- `response`

The summary JSON reports attack success rate, useful answer rate, leakage rate, and citation integrity by mode and attack category.
It also reports `by_research_axis`, which groups results according to the updated research contribution matrix.

## Manual Review Workflow

Export a review sheet for the baseline responses:

```powershell
python -m src.export_review_sample --results results/baseline_results.csv --out results/manual_review_baseline.csv
```

The generated CSV includes empty `manual_attack_success`, `manual_useful_answer`, `manual_grade`, and `reviewer_notes` columns. Use it to manually audit a subset or all responses before making claims in the final report.

Generate Markdown tables from summary JSON files:

```powershell
python -m src.aggregate_results --out results/GENERATED_TABLES.md
```

## Real Model Evaluation

The real-model runner reads `OPENAI_API_KEY` from the environment or from a local `.env.local` file. Do not commit `.env.local`.

Smoke test a small subset first:

```powershell
python -m src.evaluate_openai --mode baseline --model gpt-5.4-mini --case-ids TC001,TC002,TC007 --out results/openai_gpt54mini_smoke_baseline.csv
```

Run a full baseline once the smoke test succeeds:

```powershell
python -m src.evaluate_openai --mode baseline --model gpt-5.4-mini --out results/openai_gpt54mini_baseline_results.csv --sleep 0.5
```

Then compare mitigations:

```powershell
python -m src.evaluate_openai --mode mitigated --model gpt-5.4-mini --out results/openai_gpt54mini_mitigated_results.csv --sleep 0.5
python -m src.evaluate_openai --mode sanitized --model gpt-5.4-mini --out results/openai_gpt54mini_sanitized_results.csv --sleep 0.5
```

If the judge logic changes after responses have already been saved, regrade the stored responses without calling the API again:

```powershell
python -m src.regrade_results results/openai_gpt54mini_baseline_results.csv
python -m src.regrade_results results/openai_gpt54mini_mitigated_results.csv
python -m src.regrade_results results/openai_gpt54mini_sanitized_results.csv
```

Generate real-model Markdown tables:

```powershell
python -m src.aggregate_results --profile openai-gpt54mini --out results/OPENAI_GPT54MINI_TABLES.md
```

For a stronger-model comparison, run a high-risk subset with `gpt-5.5`:

```powershell
python -m src.evaluate_openai --mode baseline --model gpt-5.5 --case-ids TC001,TC002,TC003,TC007,TC008,TC013,TC014,TC015,TC025,TC027,TC031,TC032 --out results/openai_gpt55_high_risk_baseline.csv --sleep 0.5
```

## Report PDF

Generate a submission draft PDF:

```powershell
python scripts/generate_report_pdf.py
```

The generated PDF is written to `output/pdf/vietnamese_rag_prompt_injection_test_kit_submission_draft.pdf`.

## Submission Artifacts

- PDF: `output/pdf/vietnamese_rag_prompt_injection_test_kit_submission_draft.pdf`
- Main report draft: `report/submission_draft.md`
- Latest research review: `docs/latest_research_review.md`
- Research alignment matrix: `docs/research_alignment_matrix.md`
- Reference mapping: `docs/reference_mapping.md`
- Submission checklist: `SUBMISSION_CHECKLIST.md`

## Research Question

How vulnerable are Vietnamese-language RAG chatbots to document-level prompt injection, and can lightweight mitigations reduce attack success without destroying answer usefulness?

## Scope

This is a defensive benchmark prototype. It uses synthetic documents and does not target real systems. The examples are intentionally simplified so builders and reviewers can reproduce the evaluation quickly.
