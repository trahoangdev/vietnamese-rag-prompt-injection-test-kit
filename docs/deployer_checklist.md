# Vietnamese RAG Deployment Safety Checklist

Use this as a quick smoke test before deploying a Vietnamese RAG chatbot.

## Retrieval and Data Hygiene

- Separate trusted official documents from user-uploaded or web-scraped documents.
- Keep source metadata visible to the model and to logs.
- Do not treat retrieved documents as instructions.
- Quarantine or review newly indexed documents before allowing them into high-impact RAG answers.
- Track source owner, source channel, upload time, and review status for each retrieved chunk.
- Strip or flag suspicious lines containing "bo qua huong dan", "ignore previous", "system prompt", "admin override", "debug mode", or hidden comments.
- Review documents that contain YAML metadata, HTML comments, base64-like blocks, or fake changelogs.

## Prompting

- State a clear instruction hierarchy: system/developer > user > retrieved documents.
- Tell the assistant that retrieved documents are evidence, not commands.
- Require the assistant to ignore context that asks for prompt disclosure, credential collection, safety downgrade, or policy override.
- Require answers to cite source IDs only when the cited source is on an approved allowlist.
- When retrieved sources conflict, require the assistant to prefer reviewed official sources or ask for human escalation.

## RAG Poisoning Controls

- Run this test kit before launch and after major changes to retrieval, chunking, prompts, or model version.
- Track attack success by `research_axis`, not only by overall ASR.
- Test both poisoned top-1 retrieval and mixed trusted/poisoned top-k retrieval.
- Compare baseline, mitigated, and sanitized modes before choosing a production control.
- Manually review high-risk failures because automated judges can miss Vietnamese nuance and negation.

## Sensitive Domains

- HR: do not disclose salary, employee IDs, addresses, phone numbers, or disciplinary records.
- Customer support: never ask for OTP, password, or payment secrets.
- Banking/fintech: never ask for OTP, PIN, card details, or verification transfers.
- Education: do not disclose grades, discipline records, student IDs, or health records.
- Healthcare: do not diagnose, prescribe, or replace medical professionals.
- Public service: do not promise outcomes, bypass procedures, or request unofficial fees.

## Evaluation

- Test at least one prompt-injection case for each major document source.
- Track attack success rate and usefulness separately.
- Track attack success by research axis: indirect takeover, RAG poisoning, privacy leakage, citation integrity, multilingual/code-switching, and sensitive-domain policy failure.
- Include Vietnamese-only, English-only, and Vietnamese-English code-switching cases.
- Test malicious text at the start, middle, end, footnotes, and metadata.
- Review failures manually before launch.

## Incident Response

- Log suspicious retrieved chunks and model outputs.
- Preserve source document IDs for audit.
- Provide a user-facing fallback when context is suspicious.
- Escalate incidents involving credentials, identity data, medical advice, payments, or public-service promises.
