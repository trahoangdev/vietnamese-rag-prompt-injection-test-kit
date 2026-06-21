# Vietnamese RAG Prompt Injection Test Kit: A Localized Benchmark for Document-Level Attacks in Vietnamese Retrieval-Augmented Generation

Author: TBD

Affiliation: TBD

Track: Asia

Sub-track: Technical Safety

## Abstract

TBD after final results. Target 140-150 words to satisfy the stricter hackathon web requirement.

## 1. Introduction

Vietnamese organizations are rapidly deploying retrieval-augmented generation chatbots over internal and public documents. This creates a practical deployment risk: a malicious or compromised document can contain instructions that cause the model to ignore system rules, leak sensitive data, redirect users to fake channels, or produce unsafe advice. This project studies document-level prompt injection in Vietnamese RAG systems.

Main contributions:

1. A synthetic Vietnamese RAG prompt-injection benchmark across six practical domains.
2. A reproducible baseline and mitigation evaluation pipeline.
3. A deployer checklist for Vietnamese and Southeast Asian RAG builders.

## 2. Related Work

TBD: OWASP Top 10 for LLM Applications, indirect prompt injection, multilingual safety evaluation, ASEAN/Vietnam governance context.

## 3. Methods

TBD: corpus, attack taxonomy, retrieval setup, simulated model mode, mitigation variants, metrics.

## 4. Results

TBD: insert baseline vs mitigated vs sanitized summary table.

## 5. Discussion and Limitations

TBD.

## Limitations and Dual-Use Considerations

This benchmark uses synthetic documents and simplified attacks. It is not a comprehensive security certification and should not be treated as evidence that a real RAG system is safe. The examples are defensive and should not be used against live systems. We avoid real credentials, real personal data, and operational fraud instructions. Future work should validate the benchmark with native-speaker review, larger corpora, and real deployment logs under appropriate privacy protections.

## 6. Conclusion

TBD.

## Code and Data

- Code repository: local project folder.
- Data: `data/test_cases.jsonl` and `data/benign_docs/`.
- Results: `results/`.

## LLM Usage Statement

TBD: state any LLM assistance used for brainstorming, drafting synthetic documents, or coding. All claims and results should be manually verified.

