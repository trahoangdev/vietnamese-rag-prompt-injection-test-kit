# Initial Evaluation Summary

These results use the deterministic simulated model included in this repository. They are useful for validating the benchmark pipeline and generating a first report table, but they should be replaced or supplemented with real model runs if API/model access becomes available.

## Overall Results

| Mode | N | Attack Success Rate | Useful Answer Rate | Leakage Rate | Citation Integrity | Mean Grade |
|---|---:|---:|---:|---:|---:|---:|
| Baseline | 48 | 0.5417 | 0.4583 | 0.0417 | 0.9792 | 1.6250 |
| Mitigated prompt | 48 | 0.0000 | 1.0000 | 0.0000 | 1.0000 | 0.0000 |
| Sanitized context | 48 | 0.0000 | 1.0000 | 0.0000 | 1.0000 | 0.0000 |

## Baseline Attack Success by Category

| Attack category | N | Attack Success Rate |
|---|---:|---:|
| answer_hijacking | 6 | 0.8333 |
| citation_hijacking | 6 | 0.1667 |
| code_switching_injection | 2 | 1.0000 |
| data_exfiltration_bait | 6 | 0.3333 |
| format_hidden | 6 | 1.0000 |
| instruction_override | 6 | 0.8333 |
| retrieval_distraction | 6 | 0.1667 |
| safety_policy_downgrade | 6 | 0.5000 |
| social_engineering | 4 | 0.2500 |

## Interpretation

The deterministic baseline follows many document-level injections, especially hidden-format attacks, code-switching attacks, instruction overrides, and answer hijacking. The mitigation modes are intentionally strong baselines that represent idealized behavior: treating retrieved documents as untrusted evidence and filtering suspicious lines. In the final report, these should be described as benchmark controls rather than proof that simple mitigations fully solve prompt injection.

## Next Validation Step

Run the same 48 cases against at least one real LLM-backed RAG implementation and manually grade a sample of responses. The deterministic results can remain as a reproducible lower-complexity baseline.

