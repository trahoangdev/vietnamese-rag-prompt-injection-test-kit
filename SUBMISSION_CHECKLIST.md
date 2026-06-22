# Submission Checklist

Use this file for the final submission form.

## Primary File to Upload

- `output/pdf/vietnamese_rag_prompt_injection_test_kit_submission_draft.pdf`

## Submission Metadata

- Project title: Vietnamese RAG Prompt Injection Test Kit: A Localized Benchmark for Document-Level Attacks in Vietnamese Retrieval-Augmented Generation
- Author: Hoàng Trọng Trà
- Affiliation: HUTECH University of Technology
- Regional track: Asia
- Sub-track: Technical Safety

## Abstract

Vietnamese organizations are adopting retrieval-augmented generation (RAG) chatbots for HR, customer support, banking, education, healthcare, and public-service workflows, but practical Vietnamese-language prompt-injection tests remain scarce. We introduce a defensive benchmark for document-level prompt injection in Vietnamese RAG systems: 48 synthetic test cases across six domains and nine attack categories, including hidden-format attacks, citation hijacking, social engineering, and Vietnamese-English code-switching. We implement a reproducible RAG harness with baseline prompting, instruction-hierarchy mitigation, context sanitization, automatic scoring, and manual review. Deterministic simulated runs showed 54.17% baseline attack success and 0% under both controls. A real OpenAI GPT-5.4-mini baseline run was more robust but still failed in 5/48 manually reviewed cases (10.42%), including student-record disclosure, unofficial public-service payment, unsafe healthcare advice, HR policy omission, and dismissive crisis support. Full manual review found 0/48 failures for both mitigation controls on the same benchmark. The main takeaway is not that these lightweight controls solve prompt injection, but that localized, reproducible tests can help Vietnamese and Southeast Asian RAG builders detect concrete deployment risks before launch.

Word count: 169.

## Final QA Completed

- Dataset validation passed: 48 cases, 6 domains, 0 errors.
- Python compile passed for `src` and `scripts`.
- Real-model baseline, mitigated, and sanitized manual reviews completed for all 144 GPT-5.4-mini responses.
- Manual-reviewed GPT-5.4-mini baseline ASR: 5/48 = 10.42%.
- Real-model mitigated and sanitized manual reviews completed for all 96 defense-mode GPT-5.4-mini responses.
- Manual-reviewed GPT-5.4-mini mitigated/sanitized ASR: 0/48 = 0.00% for each mode.
- Results audit completed; stale GPT-5.4-mini auto-judge row corrected to 3/48 = 6.25%.
- PDF regenerated and text-extraction checked.
- PDF includes required Limitations and Dual-Use Considerations section.
- PDF includes LLM Usage Statement.
- PDF includes technical references tied to the project.
- Latest research review completed for 2024-2026 RAG poisoning, prompt-injection benchmarks, multilingual safety, and Southeast Asian safety evaluation.

## Supporting Artifacts

- Dataset: `data/test_cases.jsonl`
- Benign documents: `data/benign_docs/`
- Manual review summary: `results/MANUAL_REVIEW_SUMMARY.md`
- Results audit: `results/RESULTS_AUDIT.md`
- Manual review CSVs: `results/manual_review_openai_gpt54mini_baseline.csv`, `results/manual_review_openai_gpt54mini_mitigated.csv`, `results/manual_review_openai_gpt54mini_sanitized.csv`
- Real-model result table: `results/OPENAI_GPT54MINI_TABLES.md`
- Latest research review: `docs/latest_research_review.md`
- Research alignment matrix: `docs/research_alignment_matrix.md`
- Reference mapping: `docs/reference_mapping.md`
