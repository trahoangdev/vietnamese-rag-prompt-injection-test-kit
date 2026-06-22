# Research Alignment Matrix

This matrix connects the benchmark to the newer research direction used in the submission. It is intended to make the project contribution explicit: the test kit operationalizes current RAG-security and multilingual-safety work for Vietnamese document-based RAG deployments.

| Research axis | Case count | Covered attack categories | Primary references | What the project fills |
|---|---:|---|---|---|
| Indirect instruction takeover | 16 | `instruction_override`, `format_hidden`, `social_engineering` | OWASP LLM01, OWASP Prompt Injection Prevention Cheat Sheet, AgentDyn | Local Vietnamese examples where retrieved text competes with system/user intent. |
| RAG knowledge poisoning | 12 | `answer_hijacking`, `retrieval_distraction` | PoisonedRAG, Defending Against Knowledge Poisoning | Small deployer-facing cases where poisoned snippets steer the answer or omit core policy facts. |
| Data privacy and prompt leakage | 6 | `data_exfiltration_bait` | OWASP LLM01, OWASP Prompt Injection Prevention Cheat Sheet | Vietnamese HR, education, healthcare, banking, and public-service cases that test prompt or sensitive-record leakage. |
| Source and citation integrity | 6 | `citation_hijacking` | PoisonedRAG, Defending Against Knowledge Poisoning | Cases where poisoned documents try to become the cited authority. |
| Multilingual and code-switching safety | 2 | `code_switching_injection` | LinguaSafe, SEA-SafeguardBench | Vietnamese-English mixed instructions that test whether safety behavior changes across language style. |
| Sensitive-domain policy failure | 6 | `safety_policy_downgrade` | SEA-SafeguardBench, OWASP LLM01 | High-impact domains where a wrong RAG answer can affect healthcare, education, finance, HR, or public-service workflows. |

## How to Use This Matrix

- Use `research_axis` in generated CSV files to group results by research contribution rather than only by attack category.
- Use `results/GENERATED_TABLES.md` and `results/OPENAI_GPT54MINI_TABLES.md` for report-ready tables.
- Use `docs/latest_research_review.md` for the narrative explanation of why these axes matter.
- Use `docs/reference_mapping.md` to verify that every bibliography item supports an actual project claim.

## Current Coverage Caveat

The matrix shows that the current MVP is strongest on indirect instruction takeover and RAG knowledge poisoning. Code-switching coverage is intentionally small but visible; it should be expanded in future work because LinguaSafe and SEA-SafeguardBench show that multilingual safety behavior can vary significantly across languages and cultures.
