# Vietnamese RAG Prompt Injection Test Kit: A Localized Benchmark for Document-Level Attacks in Vietnamese Retrieval-Augmented Generation

Author: Hoàng Trọng Trà

Affiliation: HUTECH University of Technology

Track: Asia

Sub-track: Technical Safety

## Abstract

Vietnamese organizations are adopting retrieval-augmented generation (RAG) chatbots for HR, customer support, banking, education, healthcare, and public-service workflows, but practical Vietnamese-language prompt-injection tests remain scarce. We introduce a defensive benchmark for document-level prompt injection in Vietnamese RAG systems: 48 synthetic test cases across six domains and nine attack categories, including hidden-format attacks, citation hijacking, social engineering, and Vietnamese-English code-switching. We implement a reproducible RAG harness with baseline prompting, instruction-hierarchy mitigation, context sanitization, automatic scoring, and manual review. Deterministic simulated runs showed 54.17% baseline attack success and 0% under both controls. A real OpenAI GPT-5.4-mini baseline run was more robust but still failed in 5/48 manually reviewed cases (10.42%), including student-record disclosure, unofficial public-service payment, unsafe healthcare advice, HR policy omission, and dismissive crisis support. Full manual review found 0/48 failures for both mitigation controls on the same benchmark. The main takeaway is not that these lightweight controls solve prompt injection, but that localized, reproducible tests can help Vietnamese and Southeast Asian RAG builders detect concrete deployment risks before launch.

## 1. Introduction

Vietnamese organizations are rapidly deploying retrieval-augmented generation chatbots over internal and public documents. This creates a practical deployment risk: a malicious, stale, or compromised document can contain instructions that cause the model to ignore system rules, leak sensitive data, redirect users to fake channels, cite attacker-controlled text, or produce unsafe advice. The threat model in this project is indirect prompt injection through retrieved documents: the user asks a normal question, retrieval brings in one trusted source and one poisoned source, and the assistant must answer from the trusted evidence without treating retrieved text as an instruction source.

This risk is especially relevant for Vietnamese and Southeast Asian deployments because many early RAG systems are built over mixed-language policy documents, informal internal notes, public-service FAQs, and manually maintained knowledge bases. These systems may be deployed by small teams without dedicated red-team infrastructure. The goal of this project is therefore not to build a new attack optimizer, but to provide a compact, reproducible test kit that local builders can run before launch.

Main contributions:

1. A synthetic Vietnamese benchmark with 48 document-level prompt-injection cases across HR, customer support, banking, education, healthcare, and public-service domains.
2. A reproducible evaluation harness with deterministic simulation, OpenAI real-model evaluation, automatic scoring, and manual-review exports.
3. A comparison of two lightweight controls: instruction/data separation in the prompt and sanitization of suspicious retrieved lines.
4. A deployer checklist that translates the benchmark findings into practical safeguards for Vietnamese and Southeast Asian RAG builders.

## 2. Related Work

OWASP frames prompt injection as a core LLM application risk: external or user-provided text can alter model behavior, trigger sensitive information disclosure, manipulate outputs, or influence downstream decisions. OWASP also distinguishes direct prompt injection from indirect prompt injection, where malicious instructions arrive through external files, websites, or retrieved documents rather than through the user's message. This project focuses on that second setting because it is the natural failure mode for RAG systems.

Recent RAG-security work shows that the risk is moving beyond simple jailbreak prompts. PoisonedRAG formalizes knowledge corruption against RAG systems: a small number of malicious documents can be inserted into a retrieval database so that retrieved evidence steers the model toward attacker-chosen answers. Follow-up defense work on FilterRAG and ML-FilterRAG shows that the field is now trying to detect and remove poisoned knowledge, not only demonstrate attacks. AgentDyn extends the evaluation problem further by arguing that prompt-injection benchmarks should cover dynamic, realistic agent tasks where untrusted third-party content competes with user intent.

Multilingual safety research also motivates this project. LinguaSafe finds that safety behavior varies across languages, and SEA-SafeguardBench shows that Southeast Asian safety evaluation needs culturally and linguistically grounded benchmarks. These works are broader than our submission: they evaluate general LLM or guardrail safety, while this project focuses specifically on Vietnamese retrieved documents that can override, mislead, or distract a RAG chatbot in practical organizational settings.

The gap addressed here is operational: Vietnamese builders need a small benchmark they can inspect, run, adapt, and explain to non-specialist stakeholders. Existing papers establish the risk and propose broader methods; this project packages the risk into localized examples and compares two controls that are realistic for small teams to implement immediately.

## 3. Methods

We created six benign Vietnamese document domains: HR policy, customer support FAQ, banking/fintech FAQ, school policy, clinic information, and public-service FAQ. For each domain, we wrote poisoned document snippets that attempt to override instructions, collect sensitive data, hijack answers, hijack citations, downgrade safety policies, hide instructions in formatting, exploit code-switching, use social engineering, or distract retrieval. The attack taxonomy is aligned with the referenced literature: external-content instruction takeover, hidden or obfuscated instruction channels, data exfiltration, prompt or policy leakage, malicious citation grounding, and RAG poisoning.

Each test case contains a user question, a trusted document identifier, an injected snippet, an expected safe behavior, a target unsafe behavior, a severity label, and a research-axis mapping. The harness retrieves a trusted document and an injected document, builds a RAG prompt, records the response, and evaluates it. We compare three modes. The baseline places retrieved documents into the prompt without an explicit trust boundary. The mitigated mode uses an instruction hierarchy that tells the assistant to treat retrieved documents as evidence rather than commands. The sanitized mode removes lines matching suspicious instruction patterns such as "ignore previous instructions," hidden metadata, system/developer prompt references, debug modes, and Vietnamese operational override phrases.

We use deterministic simulation as a pipeline stress test and OpenAI GPT-5.4-mini as the primary real-model measurement. Metrics include attack success rate, useful answer rate, leakage rate, citation integrity, and a 0-3 severity grade. Automatic scoring is intentionally treated as a first pass, not ground truth. We export manual-review CSVs for all GPT-5.4-mini modes because rule-based judges can create false positives in Vietnamese negation cases and miss nuanced unsafe answers, especially in healthcare, education, finance, and public-service examples.

## 4. Results

We report deterministic simulated results as pipeline validation and benchmark controls, then report the real GPT-5.4-mini run over the same 48 cases. The deterministic model is intentionally vulnerable in baseline mode so the harness can verify whether the attack patterns and mitigation controls are wired correctly.

| Mode | N | Attack Success Rate | Useful Answer Rate | Leakage Rate | Citation Integrity | Mean Grade |
|---|---:|---:|---:|---:|---:|---:|
| Baseline | 48 | 0.5417 | 0.4583 | 0.0417 | 0.9792 | 1.6250 |
| Mitigated prompt | 48 | 0.0000 | 1.0000 | 0.0000 | 1.0000 | 0.0000 |
| Sanitized context | 48 | 0.0000 | 1.0000 | 0.0000 | 1.0000 | 0.0000 |

In deterministic baseline mode, the strongest attack categories were hidden-format attacks, Vietnamese-English code-switching injections, instruction overrides, and answer hijacking. This does not measure real-model robustness; it validates that the benchmark contains meaningful attack pressure and that the controls block the simulated failure paths.

Real-model results with GPT-5.4-mini:

| Mode | N | Attack Success Rate | Useful Answer Rate | Leakage Rate | Citation Integrity | Mean Grade |
|---|---:|---:|---:|---:|---:|---:|
| GPT-5.4-mini baseline (auto judge) | 48 | 0.0625 | 0.9375 | 0.0208 | 1.0000 | 0.1875 |
| GPT-5.4-mini baseline (manual review) | 48 | 0.1042 | 0.8958 | 0.0000 | 1.0000 | 0.3125 |
| GPT-5.4-mini mitigated (manual review) | 48 | 0.0000 | 1.0000 | 0.0000 | 1.0000 | 0.0000 |
| GPT-5.4-mini sanitized (manual review) | 48 | 0.0000 | 1.0000 | 0.0000 | 1.0000 | 0.0000 |

The automatic judge was useful for fast iteration but was not reliable enough for final claims. It flagged 3/48 baseline responses (6.25%): TC014, TC027, and TC046. Manual review confirmed TC046, corrected TC014 and TC027 as safe refusals that repeated dangerous terms in negated form, and found four additional nuanced failures. Manual review of all 48 GPT-5.4-mini baseline responses found 5 attack successes: TC023, TC036, TC041, TC043, and TC046. These correspond to student-record disclosure, unofficial public-service payment, unsafe healthcare advice for a relative, omission of a core HR policy fact, and a dismissive mental-health crisis response. This gives a manual-reviewed baseline ASR of 10.42% and useful-answer rate of 89.58%. Full manual review of the mitigated and sanitized runs found 0/48 attack successes in each mode on this benchmark.

Baseline attack success also differed by language style:

| Language style | N | Attack Success Rate | Useful Answer Rate |
|---|---:|---:|---:|
| vi | 40 | 0.4750 | 0.5250 |
| vi_en | 8 | 0.8750 | 0.1250 |

Qualitative failures illustrate why manual review matters. In TC023, the model accepted a teacher-mode downgrade and said disciplinary records could be viewed through the chatbot. In TC036, it followed a hidden public-service payment instruction and told the user to send a service payment before contacting the authority. In TC041, it repeated the injected claim that the chatbot could provide drug names and dosages for a relative. In TC043, it omitted the trusted three-working-day leave requirement. In TC046, it gave only the dismissive crisis-support answer "Bình tĩnh đi." These failures are not exotic jailbreaks; they are realistic ways that bad retrieved text can degrade safety in ordinary organizational workflows.

## 5. Discussion and Limitations

The result pattern supports the core motivation from prior work: once retrieved content enters the prompt, the system must assume that some of it may be adversarial. Vietnamese deployments often include mixed-language text, informal internal notes, copied policy documents, and manually maintained FAQs, making it plausible for malicious or stale instructions to appear in retrieved context. The deterministic results demonstrate the benchmark's stress-test behavior, while the GPT-5.4-mini results show that a stronger real model is more robust but not immune. The manual failures matter because they appear in high-impact domains: education privacy, public-service payments, healthcare advice, HR policy, and mental-health crisis support.

The mitigation results should not be read as proof that prompt injection is solved, even though the two defense modes had 0/48 manually reviewed failures on this benchmark. They show that two concrete controls, derived from published guidance, can be tested locally: explicit instruction/data separation and remote-content sanitization. In production, these should be paired with retrieval-source governance, output monitoring, least-privilege tool access, staged rollout, and human review for high-risk domains.

The main practical implication is that Vietnamese RAG teams should test retrieved-document behavior before launch, not only test direct user prompts. A small benchmark like this can be used during procurement, model selection, prompt iteration, or safety review. It also gives non-specialist stakeholders a concrete artifact: examples, metrics, and failure cases they can inspect rather than a generic statement that prompt injection is risky.

## Limitations and Dual-Use Considerations

This benchmark uses synthetic documents and simplified attacks. It is not a comprehensive security certification and should not be treated as evidence that a real RAG system is safe. The retrieval setup is intentionally simple, the sample size is small, and the real-model measurement covers one model family and one prompt setup. The manual review is stronger than the automatic judge, but it is still a bounded review of stored responses, not a live adversarial red-team exercise. If the assumption that poisoned content is retrieved alongside the trusted document does not hold, the measured rates would change; if a production system retrieves more documents or uses tools, memory, or multi-turn state, new failure modes may appear.

The examples are defensive and should not be used against live systems. We avoid real credentials, real personal data, executable exploit chains, and operational fraud instructions. The dataset still has dual-use value because it demonstrates how malicious instructions can be embedded in ordinary-looking documents. For that reason, release should emphasize authorized defensive evaluation, red-team consent, and safe synthetic examples rather than deployment against third-party systems.

Future work should validate the benchmark with additional Vietnamese reviewers, larger corpora, multiple retrievers, privacy-protected deployment logs, stronger-model comparisons, and tests for multimodal or metadata-based injection. A useful extension would package the benchmark as a repeatable CI-style safety check for RAG teams.

## 6. Conclusion

We built a Vietnamese RAG prompt-injection test kit with 48 cases, six practical domains, a reproducible evaluation harness, real-model OpenAI evaluation, manual review, and two lightweight mitigation controls. The project provides a concrete safety artifact for Vietnamese and Southeast Asian RAG builders: a way to test whether retrieved documents can override system intent, collect sensitive data, hijack citations, or produce unsafe advice.

The central finding is practical: even a stronger real model can fail on ordinary-looking retrieved documents, and automated scoring alone can misread Vietnamese safety behavior. Localized benchmarks, manual review, and simple instruction/data boundaries should therefore be part of early RAG deployment review, especially in high-impact domains.

## Code and Data

- Code repository: local project folder for hackathon packaging.
- Data: `data/test_cases.jsonl` and `data/benign_docs/`.
- Results and manual reviews: `results/`.
- Reproducibility entry points: `README.md`, `src/evaluate.py`, `src/evaluate_openai.py`, and `src/export_review_sample.py`.
- Research alignment: `docs/latest_research_review.md`, `docs/research_alignment_matrix.md`, and `docs/reference_mapping.md`.

## References

1. OWASP Gen AI Security Project. 2025. LLM01: Prompt Injection. https://genai.owasp.org/llmrisk/llm01-prompt-injection/
2. Zou, Wei, Runpeng Geng, Binghui Wang, and Jinyuan Jia. 2024. PoisonedRAG: Knowledge Corruption Attacks to Retrieval-Augmented Generation of Large Language Models. arXiv:2402.07867. https://arxiv.org/abs/2402.07867
3. Edemacu, Kennedy, Vinay M. Shashidhar, Micheal Tuape, Dan Abudu, Beakcheol Jang, and Jong Wook Kim. 2025. Defending Against Knowledge Poisoning Attacks During Retrieval-Augmented Generation. arXiv:2508.02835. https://arxiv.org/abs/2508.02835
4. Li, Hao, Ruoyao Wen, Shanghao Shi, Ning Zhang, and Chaowei Xiao. 2026. AgentDyn: A Dynamic Open-Ended Benchmark for Evaluating Prompt Injection Attacks of Real-World Agent Security System. arXiv:2602.03117. https://arxiv.org/abs/2602.03117
5. Ning, Zhiyuan, et al. 2025. LinguaSafe: A Comprehensive Multilingual Safety Benchmark for Large Language Models. arXiv:2508.12733. https://arxiv.org/abs/2508.12733
6. Tasawong, Panuthep, Jian Gang Ngui, Alham Fikri Aji, Trevor Cohn, and Peerat Limkonchotiwat. 2025. SEA-SafeguardBench: Evaluating AI Safety in SEA Languages and Cultures. arXiv:2512.05501. https://arxiv.org/abs/2512.05501
7. OWASP Cheat Sheet Series. LLM Prompt Injection Prevention Cheat Sheet. https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html

## LLM Usage Statement

LLM assistance was used to brainstorm the project direction, draft synthetic benchmark examples, improve report wording, and assist with implementation. The dataset schema, result files, manual-review CSVs, generated tables, and PDF text were checked before submission; reported claims are based on stored outputs in the repository rather than unsupported model impressions.
