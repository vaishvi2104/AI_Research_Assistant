import json
from services.citation_generator import generate_citations


def compile_research_report(paper):
    """
    Compiles all research artifacts for a paper into a comprehensive,
    print-ready Literature Review Report structure.
    """
    struct = {}
    if paper.structured_summary:
        try:
            struct = json.loads(paper.structured_summary)
        except Exception:
            struct = {}

    citations = generate_citations(
        title=paper.title,
        authors=paper.authors,
        year=paper.publication_year
    )

    refs = [r.strip() for r in (paper.references_text or "").split("\n\n") if r.strip()]

    return {
        "paper": paper,
        "structured": struct,
        "citations": citations,
        "references": refs,
        "notes": paper.notes or "No personal research notes recorded."
    }
