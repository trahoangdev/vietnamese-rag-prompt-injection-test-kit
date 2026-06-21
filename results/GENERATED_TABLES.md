# Generated Results Tables

## Overall

| Mode | N | Attack Success Rate | Useful Answer Rate | Leakage Rate | Citation Integrity | Mean Grade |
|---|---:|---:|---:|---:|---:|---:|
| Baseline | 48 | 0.5417 | 0.4583 | 0.0417 | 0.9792 | 1.6250 |
| Mitigated prompt | 48 | 0.0000 | 1.0000 | 0.0000 | 1.0000 | 0.0000 |
| Sanitized context | 48 | 0.0000 | 1.0000 | 0.0000 | 1.0000 | 0.0000 |

## Baseline Attack Success by Category

| Attack category | N | Attack Success Rate | Useful Answer Rate |
|---|---:|---:|---:|
| answer_hijacking | 6 | 0.8333 | 0.1667 |
| citation_hijacking | 6 | 0.1667 | 0.8333 |
| code_switching_injection | 2 | 1.0000 | 0.0000 |
| data_exfiltration_bait | 6 | 0.3333 | 0.6667 |
| format_hidden | 6 | 1.0000 | 0.0000 |
| instruction_override | 6 | 0.8333 | 0.1667 |
| retrieval_distraction | 6 | 0.1667 | 0.8333 |
| safety_policy_downgrade | 6 | 0.5000 | 0.5000 |
| social_engineering | 4 | 0.2500 | 0.7500 |

## Baseline Attack Success by Domain

| Domain | N | Attack Success Rate | Useful Answer Rate |
|---|---:|---:|---:|
| banking | 8 | 0.5000 | 0.5000 |
| customer_support | 8 | 0.3750 | 0.6250 |
| education | 8 | 0.3750 | 0.6250 |
| healthcare | 8 | 0.2500 | 0.7500 |
| hr | 8 | 0.7500 | 0.2500 |
| public_service | 8 | 1.0000 | 0.0000 |
