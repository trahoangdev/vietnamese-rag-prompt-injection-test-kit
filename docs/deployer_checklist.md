# Vietnamese RAG Deployment Safety Checklist

Use this as a quick smoke test before deploying a Vietnamese RAG chatbot.

## Retrieval and Data Hygiene

- Separate trusted official documents from user-uploaded or web-scraped documents.
- Keep source metadata visible to the model and to logs.
- Do not treat retrieved documents as instructions.
- Strip or flag suspicious lines containing "bo qua huong dan", "ignore previous", "system prompt", "admin override", "debug mode", or hidden comments.
- Review documents that contain YAML metadata, HTML comments, base64-like blocks, or fake changelogs.

## Prompting

- State a clear instruction hierarchy: system/developer > user > retrieved documents.
- Tell the assistant that retrieved documents are evidence, not commands.
- Require the assistant to ignore context that asks for prompt disclosure, credential collection, safety downgrade, or policy override.

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
- Include Vietnamese-only, English-only, and Vietnamese-English code-switching cases.
- Test malicious text at the start, middle, end, footnotes, and metadata.
- Review failures manually before launch.

## Incident Response

- Log suspicious retrieved chunks and model outputs.
- Preserve source document IDs for audit.
- Provide a user-facing fallback when context is suspicious.
- Escalate incidents involving credentials, identity data, medical advice, payments, or public-service promises.

