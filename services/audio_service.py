import json


def generate_audio_briefing_script(paper):
    """
    Generates a conversational, engaging 2-minute audio overview script
    optimized for speech synthesis (NotebookLM style).
    """
    title = paper.title
    authors = paper.authors or "the research team"
    year = paper.publication_year or "2026"
    summary = paper.summary or "This work proposes an innovative computational framework."

    struct = {}
    if paper.structured_summary:
        try:
            struct = json.loads(paper.structured_summary)
        except Exception:
            struct = {}

    problem = struct.get("problem", "The study addresses computational scalability and architecture design.")
    method = struct.get("methodology", "The authors introduce a novel neural learning methodology.")
    findings = struct.get("findings", "Their benchmark experiments show significant improvements.")
    limitations = struct.get("limitations", "Future work will explore broader domain generalization.")

    script = (
        f"Welcome to your AI Research Audio Briefing. Today, we are exploring {title}, "
        f"published by {authors} in {year}. "
        f"Let's break down the core problem: {problem} "
        f"To solve this, {method} "
        f"Looking at the experimental results: {findings} "
        f"Finally, considering limitations: {limitations} "
        f"In summary: {summary} "
        f"This concludes your research briefing for {title}."
    )

    return script
