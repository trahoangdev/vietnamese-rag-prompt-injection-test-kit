# Reference Mapping

This note records how each cited reference supports the project, so the bibliography remains tied to the actual benchmark rather than broad background.

| Reference | How it is used in this project |
|---|---|
| OWASP LLM01: Prompt Injection | Frames prompt injection as an LLM application vulnerability, including indirect injection through external content and RAG documents. Supports the threat model and impact categories. |
| PoisonedRAG, Zou et al. 2024 | Establishes RAG knowledge corruption as a database-level attack surface. Supports our poisoned retrieved document setup. |
| Edemacu et al. 2025 | Shows the field is moving toward detecting and filtering poisoned RAG knowledge. Supports our sanitization and future filtering direction. |
| AgentDyn, Li et al. 2026 | Shows prompt injection benchmarks are becoming dynamic and agentic. Helps position our work as a narrower, localized document-level RAG benchmark. |
| LinguaSafe, Ning et al. 2025 | Shows multilingual safety behavior varies by language and domain. Supports the need for Vietnamese-specific evaluation. |
| SEA-SafeguardBench, Tasawong et al. 2025 | Shows Southeast Asian safety evaluation needs culturally and linguistically grounded benchmarks. Supports the regional framing of this project. |
| OWASP Prompt Injection Prevention Cheat Sheet | Supports the mitigation design: structured prompts with data/instruction separation, sanitization, output monitoring, and adversarial testing. |

The removed references to broad AI governance and Vietnam AI law were not wrong as regional background, but they did not directly support the technical method or results in the current report.
