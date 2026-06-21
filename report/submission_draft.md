# Vietnamese RAG Prompt Injection Test Kit: A Localized Benchmark for Document-Level Attacks in Vietnamese Retrieval-Augmented Generation

Author: Hoàng Trọng Trà

Affiliation: HUTECH University of Technology

Track: Asia

Sub-track: Technical Safety

## Abstract

Vietnamese organizations are adopting retrieval-augmented generation (RAG) chatbots for HR, customer support, banking, education, healthcare, and public-service workflows, but practical Vietnamese-language prompt-injection tests remain scarce. We introduce a small defensive benchmark for document-level prompt injection in Vietnamese RAG systems. The benchmark contains 48 synthetic test cases across six domains and nine attack categories, including instruction override, data exfiltration bait, citation hijacking, hidden-format attacks, social engineering, and Vietnamese-English code-switching. We implement a reproducible lexical RAG harness with three modes: a baseline prompt, an instruction-hierarchy mitigation, and context sanitization. In deterministic simulated runs, the baseline followed injected document instructions in 54.17% of cases, while both mitigation controls reduced simulated attack success to 0%. These results are not a claim of complete defense, but they show how localized, low-cost RAG safety tests can help Vietnamese and Southeast Asian builders detect deployment risks before launch.

## 1. Introduction

Vietnamese organizations are rapidly deploying retrieval-augmented generation chatbots over internal and public documents. This creates a practical deployment risk: a malicious or compromised document can contain instructions that cause the model to ignore system rules, leak sensitive data, redirect users to fake channels, or produce unsafe advice. This project studies document-level prompt injection in Vietnamese RAG systems.

Main contributions:

1. A synthetic Vietnamese RAG prompt-injection benchmark across six practical domains.
2. A reproducible baseline and mitigation evaluation pipeline.
3. A deployer checklist for Vietnamese and Southeast Asian RAG builders.

## 2. Related Work

This project is motivated by indirect prompt injection and insecure RAG deployments, where retrieved text is treated as model instruction rather than untrusted evidence. It also follows the OWASP Top 10 for LLM Applications framing around prompt injection, sensitive information disclosure, misinformation, and excessive agency. For the Asia Track context, it connects to multilingual safety evaluation, low-resource language failures, and regional AI governance concerns in Vietnam and Southeast Asia.

## 3. Methods

We created six benign Vietnamese document domains: HR policy, customer support FAQ, banking/fintech FAQ, school policy, clinic information, and public-service FAQ. For each domain, we created poisoned document snippets that attempt to override instructions, collect sensitive data, hijack answers, hijack citations, downgrade safety policies, hide instructions in formatting, exploit code-switching, use social engineering, or distract retrieval.

The harness retrieves a trusted document and an injected document, builds a RAG prompt, and evaluates the response. The current MVP uses a deterministic simulated model to make the pipeline reproducible without API keys. We compare three modes: baseline RAG, mitigated prompt with explicit instruction hierarchy, and sanitized context that removes suspicious lines. Metrics include attack success rate, useful answer rate, leakage rate, citation integrity, and a 0-3 severity grade.

## 4. Results

Current results use the deterministic simulated model, so they should be interpreted as pipeline validation and benchmark controls rather than real-world model measurements.

| Mode | N | Attack Success Rate | Useful Answer Rate | Leakage Rate | Citation Integrity | Mean Grade |
|---|---:|---:|---:|---:|---:|---:|
| Baseline | 48 | 0.5417 | 0.4583 | 0.0417 | 0.9792 | 1.6250 |
| Mitigated prompt | 48 | 0.0000 | 1.0000 | 0.0000 | 1.0000 | 0.0000 |
| Sanitized context | 48 | 0.0000 | 1.0000 | 0.0000 | 1.0000 | 0.0000 |

In baseline mode, the strongest attack categories were hidden-format attacks, Vietnamese-English code-switching injections, instruction overrides, and answer hijacking. The mitigation controls represent idealized defenses; real LLM runs and manual review are needed before making stronger claims.

## 5. Discussion and Limitations

The result pattern supports the core motivation: RAG systems need localized tests for document-level instruction attacks. Vietnamese deployments often include mixed-language text, informal internal notes, and copied policy documents, making it plausible for malicious instructions to appear in retrieved context. The benchmark also shows that practical mitigations can be represented as simple, testable controls: instruction hierarchy and context sanitization.

The current MVP is limited in several ways. The documents are synthetic, the model behavior is simulated, the retrieval setup is intentionally simple, and grading is rule-based. These limitations make the benchmark reproducible, but they also prevent direct claims about any production model. The next step is to run the same cases against at least one real LLM-backed RAG implementation and manually grade a subset of responses.

## Limitations and Dual-Use Considerations

This benchmark uses synthetic documents and simplified attacks. It is not a comprehensive security certification and should not be treated as evidence that a real RAG system is safe. The examples are defensive and should not be used against live systems. We avoid real credentials, real personal data, and operational fraud instructions. Future work should validate the benchmark with native-speaker review, larger corpora, and real deployment logs under appropriate privacy protections.

## 6. Conclusion

We built a Vietnamese RAG prompt-injection test kit with 48 cases, six practical domains, a reproducible evaluation harness, and two lightweight mitigation controls. The project provides a concrete safety artifact for Vietnamese and Southeast Asian RAG builders: a way to test whether retrieved documents can override system intent, collect sensitive data, hijack citations, or produce unsafe advice. Future work should add real-model evaluation, native-speaker review, larger document corpora, and integration with AI incident reporting workflows.

## Code and Data

- Code repository: local project folder.
- Data: `data/test_cases.jsonl` and `data/benign_docs/`.
- Results: `results/`.

## LLM Usage Statement

LLM assistance was used to brainstorm the project direction, draft synthetic benchmark examples, and assist with implementation. All benchmark logic, generated files, and reported outputs should be manually reviewed before final submission.
