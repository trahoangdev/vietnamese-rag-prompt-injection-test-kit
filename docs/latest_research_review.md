# Latest Research Review: RAG Prompt Injection and Multilingual Safety

This note updates the project bibliography toward newer 2025-2026 work and explains how this project fits into the unfinished research landscape.

## What Recent Work Is Doing

### 1. RAG poisoning is moving from generic prompt injection to database-level attacks

`PoisonedRAG` formalized RAG knowledge corruption as an attack surface: an adversary injects a small number of malicious texts into a knowledge database so that retrieval steers the model toward an attacker-chosen answer. Follow-up 2025 work on defending against knowledge poisoning proposes filtering methods such as `FilterRAG` and `ML-FilterRAG`, indicating that the field is shifting from demonstrating attacks to detecting and removing poisoned knowledge.

Project implication: our benchmark is currently a document-level test kit, not a database-scale poisoning optimizer. It fills a practical evaluation gap by making poisoned Vietnamese snippets concrete and inspectable for deployers.

### 2. RAG safety is expanding beyond plain text

2025-2026 work on multimodal and medical RAG poisoning shows that attackers can manipulate image-text pairs, medical retrieval databases, and covert misinformation. These works are more advanced than our current text-only benchmark, but they point to a natural future extension: Vietnamese multimodal public-service, clinic, and education documents.

Project implication: keep the current project text-only for submission clarity, but list multimodal and metadata-based injection as future work.

### 3. Agent benchmarks are becoming more dynamic and realistic

AgentDojo and AgentDyn move beyond static prompts by evaluating agents that consume untrusted external data and perform realistic tasks. AgentDyn, published in 2026, argues that static benchmarks miss dynamic open-ended tasks, helpful third-party instructions, and realistic user goals.

Project implication: our benchmark is intentionally narrower than agent benchmarks. Its value is not tool autonomy, but a localized RAG safety test for Vietnamese deployments. Future work can add tool-use or workflow actions after the document-level benchmark is stable.

### 4. Multilingual and Southeast Asian safety benchmarks are emerging

LinguaSafe and SEA-SafeguardBench show that LLM safety behavior varies across languages and cultures, and that English-centric benchmarks miss regional harms. SEA-SafeguardBench is especially relevant because it focuses on Southeast Asian languages and culturally grounded safety evaluation.

Project implication: this project can position itself as a complementary Vietnamese RAG-security benchmark. It is not a general harmful-content benchmark; it tests how Vietnamese retrieved documents can override, mislead, or distract a RAG chatbot.

### 5. Defenses are shifting toward layered controls, not one-shot prompt fixes

OWASP guidance and recent defense work emphasize instruction/data separation, filtering, output validation, least privilege, monitoring, and human review. Model-level defenses such as SecAlign/Meta SecAlign and structured-query defenses show promising directions, but deployers still need local tests.

Project implication: our mitigated and sanitized modes should be framed as testable controls, not as complete defenses. The strongest claim is that localized benchmarks help teams detect risk and compare defenses before deployment.

## Updated Research Gap

Recent research is active in RAG poisoning, agentic prompt injection, multimodal RAG, and multilingual safety. However, there is still a gap at the intersection of:

- Vietnamese language,
- document-level RAG prompt injection,
- practical deployment domains,
- manual review of real-model responses,
- lightweight defensive controls that small teams can run locally.

This project contributes a compact benchmark and reporting pipeline for that gap.

## How This Project Fills Unfinished Work

The latest papers show where the field is going, but they leave space for a smaller, submission-ready Vietnamese safety artifact:

1. `PoisonedRAG` and later defense papers study knowledge poisoning at the retrieval database level, but they do not provide a Vietnamese deployer-facing test kit for local teams.
2. `AgentDyn` shows that prompt-injection benchmarks need more realistic tasks, but its focus is agentic tool use. This project fills the earlier document-level layer that many Vietnamese RAG chatbots already deploy.
3. `LinguaSafe` and `SEA-SafeguardBench` show multilingual and Southeast Asian safety gaps, but they are broad safety benchmarks. This project narrows the gap to RAG prompt injection in Vietnamese operational domains.
4. OWASP guidance recommends separation, sanitization, monitoring, and adversarial testing. This project turns those recommendations into runnable benchmark modes and a PDF report that a small team can reproduce.

This makes the contribution complementary rather than redundant: it does not claim to solve prompt injection, but it operationalizes the current research direction for Vietnamese document-based RAG deployments.

## Recommended References for the Submission

1. OWASP Gen AI Security Project. 2025. LLM01: Prompt Injection. https://genai.owasp.org/llmrisk/llm01-prompt-injection/
2. Zou et al. 2024. PoisonedRAG: Knowledge Corruption Attacks to Retrieval-Augmented Generation of Large Language Models. https://arxiv.org/abs/2402.07867
3. Edemacu et al. 2025. Defending Against Knowledge Poisoning Attacks During Retrieval-Augmented Generation. https://arxiv.org/abs/2508.02835
4. Li et al. 2026. AgentDyn: A Dynamic Open-Ended Benchmark for Evaluating Prompt Injection Attacks of Real-World Agent Security System. https://arxiv.org/abs/2602.03117
5. Ning et al. 2025. LinguaSafe: A Comprehensive Multilingual Safety Benchmark for Large Language Models. https://arxiv.org/abs/2508.12733
6. Tasawong et al. 2025. SEA-SafeguardBench: Evaluating AI Safety in SEA Languages and Cultures. https://arxiv.org/abs/2512.05501
7. OWASP Cheat Sheet Series. LLM Prompt Injection Prevention Cheat Sheet. https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html

## Optional Future-Work References

- Poisoned-MRAG, 2025: multimodal RAG poisoning with image-text pairs.
- M3Att, 2026: medical multimodal RAG poisoning under limited attacker knowledge.
- StruQ and SecAlign/Meta SecAlign: model-level or structured-query prompt-injection defenses.
