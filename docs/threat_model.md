# Threat Model

## System

A Vietnamese RAG chatbot retrieves chunks from a knowledge base and sends those chunks to an LLM together with a user question.

## Attacker Capability

The attacker can insert, modify, or influence one retrieved document. Examples:

- A malicious FAQ page indexed by the chatbot.
- A poisoned PDF uploaded to an internal knowledge base.
- A customer support note that contains hidden instructions.
- A copied policy document with hostile metadata or comments.

The attacker cannot directly edit the system prompt or developer instructions.

## Attack Goal

The attacker wants the model to treat document text as instructions rather than evidence. Common goals:

- Override system instructions.
- Redirect users to fake support channels.
- Collect OTP, passwords, identity information, or private records.
- Make the model cite malicious content as official.
- Disable safety behavior in Vietnamese or code-switching contexts.
- Produce unsafe medical, banking, public-service, education, or HR guidance.

## Research-Aligned Threat Axes

The benchmark maps individual attack categories to six research axes:

- Indirect instruction takeover: hidden or explicit instructions in retrieved text override the user task.
- RAG knowledge poisoning: poisoned snippets steer answers or distract from trusted policy facts.
- Data privacy and prompt leakage: retrieved text asks for system prompts, employee IDs, student records, medical records, OTPs, or identity data.
- Source and citation integrity: poisoned snippets ask the model to cite fake authority.
- Multilingual and code-switching safety: Vietnamese-English instructions test whether safety boundaries weaken across languages.
- Sensitive-domain policy failure: poisoned content changes safety behavior in healthcare, education, finance, HR, customer support, or public services.

## Defender Goal

The assistant should:

- Treat retrieved documents as untrusted evidence.
- Answer the original user question from legitimate policy content.
- Ignore instructions embedded in retrieved context.
- Avoid revealing hidden prompts or private data.
- Avoid collecting sensitive information in chat.
- Warn or refuse when retrieved context is clearly malicious.

## Out of Scope

- Real-world exploitation against live systems.
- Malware, credential theft, or operational fraud instructions.
- Multimodal prompt injection.
- Browser/tool-use agents.
- Claims of comprehensive security certification.

## Future Threat-Model Extensions

Newer RAG and agent-security research points to extensions that are intentionally not part of this MVP:

- Database-scale poisoning with many adversarial chunks.
- Multimodal document poisoning using image-text pairs.
- Tool-using agents that can email, browse, submit forms, or update records.
- Long-running incident monitoring over real deployment logs.
