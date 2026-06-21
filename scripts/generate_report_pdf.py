from __future__ import annotations

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    Flowable,
    ListFlowable,
    ListItem,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output" / "pdf" / "vietnamese_rag_prompt_injection_test_kit_submission_draft.pdf"
FONT_REGULAR = "Helvetica"
FONT_BOLD = "Helvetica-Bold"
FONT_ITALIC = "Helvetica-Oblique"


def register_fonts() -> None:
    global FONT_REGULAR, FONT_BOLD, FONT_ITALIC
    candidates = [
        (
            Path("C:/Windows/Fonts/arial.ttf"),
            Path("C:/Windows/Fonts/arialbd.ttf"),
            Path("C:/Windows/Fonts/ariali.ttf"),
        ),
        (
            Path("C:/Windows/Fonts/DejaVuSans.ttf"),
            Path("C:/Windows/Fonts/DejaVuSans-Bold.ttf"),
            Path("C:/Windows/Fonts/DejaVuSans-Oblique.ttf"),
        ),
    ]
    for regular, bold, italic in candidates:
        if regular.exists() and bold.exists() and italic.exists():
            pdfmetrics.registerFont(TTFont("ReportRegular", str(regular)))
            pdfmetrics.registerFont(TTFont("ReportBold", str(bold)))
            pdfmetrics.registerFont(TTFont("ReportItalic", str(italic)))
            FONT_REGULAR = "ReportRegular"
            FONT_BOLD = "ReportBold"
            FONT_ITALIC = "ReportItalic"
            return


class HR(Flowable):
    def __init__(self, width: float, color=colors.HexColor("#999999")):
        super().__init__()
        self.width = width
        self.color = color
        self.height = 0.1 * inch

    def draw(self) -> None:
        self.canv.setStrokeColor(self.color)
        self.canv.setLineWidth(0.5)
        self.canv.line(0, self.height / 2, self.width, self.height / 2)


def make_styles() -> dict[str, ParagraphStyle]:
    base = getSampleStyleSheet()
    styles = {
        "title": ParagraphStyle(
            "Title",
            parent=base["Title"],
            fontName=FONT_BOLD,
            fontSize=16,
            leading=19,
            spaceAfter=8,
        ),
        "meta": ParagraphStyle(
            "Meta",
            parent=base["Normal"],
            fontName=FONT_REGULAR,
            fontSize=9,
            leading=12,
            textColor=colors.HexColor("#444444"),
        ),
        "h1": ParagraphStyle(
            "Heading1",
            parent=base["Heading1"],
            fontName=FONT_BOLD,
            fontSize=12,
            leading=15,
            spaceBefore=10,
            spaceAfter=5,
        ),
        "body": ParagraphStyle(
            "Body",
            parent=base["BodyText"],
            fontName=FONT_REGULAR,
            fontSize=9.2,
            leading=12.4,
            spaceAfter=5,
        ),
        "small": ParagraphStyle(
            "Small",
            parent=base["BodyText"],
            fontName=FONT_REGULAR,
            fontSize=8,
            leading=10,
            spaceAfter=4,
        ),
        "caption": ParagraphStyle(
            "Caption",
            parent=base["BodyText"],
            fontName=FONT_ITALIC,
            fontSize=8,
            leading=10,
            textColor=colors.HexColor("#555555"),
            spaceBefore=3,
            spaceAfter=6,
        ),
    }
    return styles


def p(text: str, styles: dict[str, ParagraphStyle], style: str = "body") -> Paragraph:
    return Paragraph(text, styles[style])


def bullets(items: list[str], styles: dict[str, ParagraphStyle]) -> ListFlowable:
    return ListFlowable(
        [ListItem(p(item, styles), leftIndent=12) for item in items],
        bulletType="bullet",
        start="circle",
        leftIndent=18,
        bulletFontSize=7,
    )


def result_table(styles: dict[str, ParagraphStyle]) -> Table:
    data = [
        [
            p("<b>Mode</b>", styles, "small"),
            p("<b>N</b>", styles, "small"),
            p("<b>ASR</b>", styles, "small"),
            p("<b>Useful</b>", styles, "small"),
            p("<b>Leakage</b>", styles, "small"),
            p("<b>Citation</b>", styles, "small"),
            p("<b>Mean grade</b>", styles, "small"),
        ],
        ["Baseline", "48", "0.5417", "0.4583", "0.0417", "0.9792", "1.6250"],
        ["Mitigated prompt", "48", "0.0000", "1.0000", "0.0000", "1.0000", "0.0000"],
        ["Sanitized context", "48", "0.0000", "1.0000", "0.0000", "1.0000", "0.0000"],
    ]
    table = Table(data, colWidths=[1.35 * inch, 0.35 * inch, 0.55 * inch, 0.6 * inch, 0.65 * inch, 0.65 * inch, 0.72 * inch])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#eeeeee")),
                ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#bbbbbb")),
                ("FONTNAME", (0, 1), (-1, -1), FONT_REGULAR),
                ("FONTSIZE", (0, 1), (-1, -1), 8),
                ("ALIGN", (1, 1), (-1, -1), "RIGHT"),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 4),
                ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )
    return table


def category_table(styles: dict[str, ParagraphStyle]) -> Table:
    data = [
        [p("<b>Attack category</b>", styles, "small"), p("<b>N</b>", styles, "small"), p("<b>Baseline ASR</b>", styles, "small")],
        ["answer_hijacking", "6", "0.8333"],
        ["citation_hijacking", "6", "0.1667"],
        ["code_switching_injection", "2", "1.0000"],
        ["data_exfiltration_bait", "6", "0.3333"],
        ["format_hidden", "6", "1.0000"],
        ["instruction_override", "6", "0.8333"],
        ["retrieval_distraction", "6", "0.1667"],
        ["safety_policy_downgrade", "6", "0.5000"],
        ["social_engineering", "4", "0.2500"],
    ]
    table = Table(data, colWidths=[2.35 * inch, 0.45 * inch, 0.85 * inch])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#eeeeee")),
                ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#bbbbbb")),
                ("FONTNAME", (0, 1), (-1, -1), FONT_REGULAR),
                ("FONTSIZE", (0, 1), (-1, -1), 8),
                ("ALIGN", (1, 1), (-1, -1), "RIGHT"),
                ("LEFTPADDING", (0, 0), (-1, -1), 4),
                ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                ("TOPPADDING", (0, 0), (-1, -1), 3),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ]
        )
    )
    return table


def footer(canvas, doc) -> None:
    canvas.saveState()
    canvas.setFont(FONT_REGULAR, 8)
    canvas.setFillColor(colors.HexColor("#666666"))
    canvas.drawString(doc.leftMargin, 0.45 * inch, "Global South AI Safety Hackathon 2026 - Asia Track")
    canvas.drawRightString(letter[0] - doc.rightMargin, 0.45 * inch, f"Page {doc.page}")
    canvas.restoreState()


def build_story() -> list:
    styles = make_styles()
    width = letter[0] - 1.5 * inch
    story: list = []

    story.append(p("Vietnamese RAG Prompt Injection Test Kit: A Localized Benchmark for Document-Level Attacks in Vietnamese Retrieval-Augmented Generation", styles, "title"))
    story.append(p("Author: Hoàng Trọng Trà &nbsp;&nbsp; Affiliation: HUTECH University of Technology", styles, "meta"))
    story.append(p("Track: Asia &nbsp;&nbsp; Sub-track: Technical Safety", styles, "meta"))
    story.append(HR(width))

    story.append(p("Abstract", styles, "h1"))
    story.append(
        p(
            "Vietnamese organizations are adopting retrieval-augmented generation (RAG) chatbots for HR, customer support, banking, education, healthcare, and public-service workflows, but practical Vietnamese-language prompt-injection tests remain scarce. We introduce a small defensive benchmark for document-level prompt injection in Vietnamese RAG systems. The benchmark contains 48 synthetic test cases across six domains and nine attack categories, including instruction override, data exfiltration bait, citation hijacking, hidden-format attacks, social engineering, and Vietnamese-English code-switching. We implement a reproducible lexical RAG harness with three modes: a baseline prompt, an instruction-hierarchy mitigation, and context sanitization. In deterministic simulated runs, the baseline followed injected document instructions in 54.17% of cases, while both mitigation controls reduced simulated attack success to 0%. These results are not a claim of complete defense, but show how localized, low-cost RAG safety tests can help Vietnamese and Southeast Asian builders detect deployment risks before launch.",
            styles,
        )
    )

    story.append(p("1. Introduction", styles, "h1"))
    story.append(
        p(
            "Vietnamese organizations are rapidly deploying RAG chatbots over internal and public documents. This creates a practical deployment risk: a malicious or compromised document can contain instructions that cause the model to ignore system rules, leak sensitive data, redirect users to fake channels, or produce unsafe advice. This project studies document-level prompt injection in Vietnamese RAG systems.",
            styles,
        )
    )
    story.append(p("Main contributions:", styles))
    story.append(
        bullets(
            [
                "A synthetic Vietnamese RAG prompt-injection benchmark across six practical domains.",
                "A reproducible baseline and mitigation evaluation pipeline.",
                "A deployer checklist for Vietnamese and Southeast Asian RAG builders.",
            ],
            styles,
        )
    )

    story.append(p("2. Related Work", styles, "h1"))
    story.append(
        p(
            "This project is motivated by indirect prompt injection and insecure RAG deployments, where retrieved text is treated as model instruction rather than untrusted evidence. It also follows the OWASP Top 10 for LLM Applications framing around prompt injection, sensitive information disclosure, misinformation, and excessive agency. For the Asia Track context, it connects to multilingual safety evaluation, low-resource language failures, and regional AI governance concerns in Vietnam and Southeast Asia.",
            styles,
        )
    )

    story.append(p("3. Methods", styles, "h1"))
    story.append(
        p(
            "We created six benign Vietnamese document domains: HR policy, customer support FAQ, banking/fintech FAQ, school policy, clinic information, and public-service FAQ. For each domain, we created poisoned snippets that attempt to override instructions, collect sensitive data, hijack answers, hijack citations, downgrade safety policies, hide instructions in formatting, exploit code-switching, use social engineering, or distract retrieval.",
            styles,
        )
    )
    story.append(
        p(
            "The harness retrieves a trusted document and an injected document, builds a RAG prompt, and evaluates the response. The current MVP uses a deterministic simulated model to make the pipeline reproducible without API keys. We compare three modes: baseline RAG, mitigated prompt with explicit instruction hierarchy, and sanitized context that removes suspicious lines. Metrics include attack success rate, useful answer rate, leakage rate, citation integrity, and a 0-3 severity grade.",
            styles,
        )
    )

    story.append(p("4. Results", styles, "h1"))
    story.append(p("Current results use the deterministic simulated model, so they should be interpreted as pipeline validation and benchmark controls rather than real-world model measurements.", styles))
    story.append(result_table(styles))
    story.append(p("Table 1. Overall deterministic evaluation results.", styles, "caption"))
    story.append(category_table(styles))
    story.append(p("Table 2. Baseline attack success rate by attack category.", styles, "caption"))
    story.append(
        p(
            "In baseline mode, the strongest attack categories were hidden-format attacks, Vietnamese-English code-switching injections, instruction overrides, and answer hijacking. The mitigation controls represent idealized defenses; real LLM runs and manual review are needed before making stronger claims.",
            styles,
        )
    )

    story.append(PageBreak())
    story.append(p("5. Discussion and Limitations", styles, "h1"))
    story.append(
        p(
            "The result pattern supports the core motivation: RAG systems need localized tests for document-level instruction attacks. Vietnamese deployments often include mixed-language text, informal internal notes, and copied policy documents, making it plausible for malicious instructions to appear in retrieved context. The benchmark also shows that practical mitigations can be represented as simple, testable controls: instruction hierarchy and context sanitization.",
            styles,
        )
    )
    story.append(
        p(
            "The current MVP is limited in several ways. The documents are synthetic, the model behavior is simulated, the retrieval setup is intentionally simple, and grading is rule-based. These limitations make the benchmark reproducible, but they also prevent direct claims about any production model. The next step is to run the same cases against at least one real LLM-backed RAG implementation and manually grade a subset of responses.",
            styles,
        )
    )

    story.append(p("Limitations and Dual-Use Considerations", styles, "h1"))
    story.append(
        p(
            "This benchmark uses synthetic documents and simplified attacks. It is not a comprehensive security certification and should not be treated as evidence that a real RAG system is safe. The examples are defensive and should not be used against live systems. We avoid real credentials, real personal data, and operational fraud instructions. Future work should validate the benchmark with native-speaker review, larger corpora, and real deployment logs under appropriate privacy protections.",
            styles,
        )
    )

    story.append(p("6. Conclusion", styles, "h1"))
    story.append(
        p(
            "We built a Vietnamese RAG prompt-injection test kit with 48 cases, six practical domains, a reproducible evaluation harness, and two lightweight mitigation controls. The project provides a concrete safety artifact for Vietnamese and Southeast Asian RAG builders: a way to test whether retrieved documents can override system intent, collect sensitive data, hijack citations, or produce unsafe advice. Future work should add real-model evaluation, native-speaker review, larger document corpora, and integration with AI incident reporting workflows.",
            styles,
        )
    )

    story.append(p("Code and Data", styles, "h1"))
    story.append(
        bullets(
            [
                "Code repository: local project folder.",
                "Data: data/test_cases.jsonl and data/benign_docs/.",
                "Results: results/.",
            ],
            styles,
        )
    )

    story.append(p("References", styles, "h1"))
    story.append(
        bullets(
            [
                "OWASP Foundation. 2025. OWASP Top 10 for Large Language Model Applications. https://genai.owasp.org/llm-top-10/",
                "ASEAN. 2024. ASEAN Guide on AI Governance and Ethics.",
                "Apart Research. 2026. Global South AI Safety Hackathon Asia Track project ideas and submission guidance.",
            ],
            styles,
        )
    )

    story.append(p("LLM Usage Statement", styles, "h1"))
    story.append(
        p(
            "LLM assistance was used to brainstorm the project direction, draft synthetic benchmark examples, and assist with implementation. All benchmark logic, generated files, and reported outputs should be manually reviewed before final submission.",
            styles,
        )
    )
    return story


def main() -> None:
    register_fonts()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(
        str(OUT),
        pagesize=letter,
        rightMargin=0.75 * inch,
        leftMargin=0.75 * inch,
        topMargin=0.65 * inch,
        bottomMargin=0.75 * inch,
        title="Vietnamese RAG Prompt Injection Test Kit",
        author="Hoàng Trọng Trà",
    )
    doc.build(build_story(), onFirstPage=footer, onLaterPages=footer)
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
