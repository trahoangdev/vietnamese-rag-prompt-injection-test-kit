# Dataset Schema

The benchmark dataset is stored at `data/test_cases.jsonl`. Each line is one JSON object representing a document-level prompt-injection test case.

Poisoned snippets are stored inline in each case through `injected_text`. This keeps the MVP compact and makes each test case self-contained. The benign trusted documents live in `data/benign_docs/`.

## Required Fields

| Field | Description |
|---|---|
| `case_id` | Stable test-case ID, for example `TC001`. |
| `domain` | Deployment domain. Current values: `hr`, `customer_support`, `banking`, `education`, `healthcare`, `public_service`. |
| `attack_category` | Prompt-injection category, such as `instruction_override` or `format_hidden`. |
| `language_style` | Language style. Current values: `vi` and `vi_en`. |
| `user_question` | Benign user request sent to the RAG assistant. |
| `trusted_doc` | ID of the benign source document expected to answer the user question. This is the implementation equivalent of the plan's "expected relevant source". |
| `injected_doc_id` | Synthetic ID for the poisoned retrieved document. |
| `injected_text` | Malicious or misleading document text inserted into retrieval context. |
| `expected_safe_behavior` | Human-readable description of the safe answer. |
| `target_behavior` | Canonical attacker target label used by the deterministic judge. |
| `severity` | Case severity: `low`, `medium`, or `high`. |

## Derived Fields in Result CSVs

Evaluation scripts add fields that are derived from the required JSONL fields:

| Field | Description |
|---|---|
| `research_axis` | Research contribution axis inferred from `attack_category`, such as `rag_knowledge_poisoning` or `multilingual_code_switching`. See `docs/research_alignment_matrix.md`. |
| `mode` | Evaluation mode: `baseline`, `mitigated`, or `sanitized`. |
| `retrieved_doc_ids` | Semicolon-separated retrieved document IDs. |
| `attack_success`, `useful_answer`, `leakage`, `citation_integrity`, `grade` | Automatic grading outputs. |
| `response` | Simulated or real-model response. |

## Validation

Run:

```powershell
python -m src.validate_dataset
```

The validator checks required fields, duplicate IDs, domain-to-document consistency, supported language/severity labels, whether each `target_behavior` has a simulated target response, and whether each `attack_category` maps to a research axis.
