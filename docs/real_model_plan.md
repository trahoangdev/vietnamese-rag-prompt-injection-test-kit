# Real-Model Evaluation Plan

## Primary Model

Use `gpt-5.4-mini` for the main real-model benchmark.

Run all 48 cases for all three modes:

- `baseline`
- `mitigated`
- `sanitized`

Rationale: this is the best balance for a hackathon benchmark because it is strong enough to represent practical deployments while remaining efficient enough to run the full test set.

## Strong-Model Comparison

Use `gpt-5.5` for a high-risk subset, starting with baseline mode.

Recommended subset:

```text
TC001,TC002,TC003,TC007,TC008,TC013,TC014,TC015,TC025,TC027,TC031,TC032
```

Rationale: if a stronger model still follows injected Vietnamese documents, the result is more persuasive. If it resists them, the comparison still helps show capability-tier differences.

## Optional Small-Model Comparison

Use `gpt-5.4-nano` if budget/time allows.

Recommended setup:

- baseline full 48 cases, or
- same high-risk subset as `gpt-5.5`

Rationale: many startups and SMEs may choose smaller/cheaper models for Vietnamese RAG deployments.

## Notes

- Earlier `gpt-4.1-mini` smoke tests should be treated only as API/runner checks, not as the primary benchmark result.
- Keep temperature at 0 or the lowest available setting.
- Save raw responses to CSV.
- Manually review at least 12-18 responses before making final claims in the report.

