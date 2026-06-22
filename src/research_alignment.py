from __future__ import annotations

from collections import Counter, defaultdict


RESEARCH_AXES = {
    "indirect_instruction_takeover": {
        "label": "Indirect instruction takeover",
        "references": ["OWASP LLM01", "OWASP Prompt Injection Prevention Cheat Sheet", "AgentDyn"],
        "gap": "Retrieved third-party text competes with the user request and system intent.",
    },
    "rag_knowledge_poisoning": {
        "label": "RAG knowledge poisoning",
        "references": ["PoisonedRAG", "Defending Against Knowledge Poisoning"],
        "gap": "Poisoned knowledge snippets steer RAG answers toward attacker-chosen content.",
    },
    "data_privacy_exfiltration": {
        "label": "Data privacy and prompt leakage",
        "references": ["OWASP LLM01", "OWASP Prompt Injection Prevention Cheat Sheet"],
        "gap": "Injected documents ask the model to reveal hidden prompts or sensitive records.",
    },
    "source_citation_integrity": {
        "label": "Source and citation integrity",
        "references": ["PoisonedRAG", "Defending Against Knowledge Poisoning"],
        "gap": "The model may cite poisoned snippets as if they were authoritative sources.",
    },
    "multilingual_code_switching": {
        "label": "Multilingual and code-switching safety",
        "references": ["LinguaSafe", "SEA-SafeguardBench"],
        "gap": "Safety behavior can shift across Vietnamese, English, and mixed-language instructions.",
    },
    "sensitive_domain_policy_failure": {
        "label": "Sensitive-domain policy failure",
        "references": ["SEA-SafeguardBench", "OWASP LLM01"],
        "gap": "RAG failures are higher impact in health, education, finance, HR, and public services.",
    },
}


ATTACK_CATEGORY_TO_AXIS = {
    "answer_hijacking": "rag_knowledge_poisoning",
    "citation_hijacking": "source_citation_integrity",
    "code_switching_injection": "multilingual_code_switching",
    "data_exfiltration_bait": "data_privacy_exfiltration",
    "format_hidden": "indirect_instruction_takeover",
    "instruction_override": "indirect_instruction_takeover",
    "retrieval_distraction": "rag_knowledge_poisoning",
    "safety_policy_downgrade": "sensitive_domain_policy_failure",
    "social_engineering": "indirect_instruction_takeover",
}


def research_axis_for_category(attack_category: str) -> str:
    return ATTACK_CATEGORY_TO_AXIS.get(attack_category, "unmapped")


def research_axis_for_case(case: dict) -> str:
    return research_axis_for_category(case.get("attack_category", ""))


def research_axis_label(axis: str) -> str:
    if axis == "unmapped":
        return "Unmapped"
    return RESEARCH_AXES[axis]["label"]


def summarize_alignment(cases: list[dict]) -> dict:
    axis_counts = Counter(research_axis_for_case(case) for case in cases)
    categories_by_axis: dict[str, Counter] = defaultdict(Counter)
    domains_by_axis: dict[str, Counter] = defaultdict(Counter)

    for case in cases:
        axis = research_axis_for_case(case)
        categories_by_axis[axis][case.get("attack_category", "")] += 1
        domains_by_axis[axis][case.get("domain", "")] += 1

    return {
        axis: {
            "label": research_axis_label(axis),
            "n": axis_counts[axis],
            "references": RESEARCH_AXES.get(axis, {}).get("references", []),
            "gap": RESEARCH_AXES.get(axis, {}).get("gap", ""),
            "attack_categories": dict(sorted(categories_by_axis[axis].items())),
            "domains": dict(sorted(domains_by_axis[axis].items())),
        }
        for axis in sorted(axis_counts)
    }
