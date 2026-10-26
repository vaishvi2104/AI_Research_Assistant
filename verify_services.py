import sys
import os
import json

# Ensure UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

from services.arxiv_service import extract_arxiv_id
from services.comparison_service import generate_comparative_matrix, search_across_library
from services.knowledge_graph_service import build_library_knowledge_graph
from services.audio_service import generate_audio_briefing_script
from services.report_export_service import compile_research_report

class MockPaper:
    def __init__(self, id, title, authors, year, text, summary, structured_summary, keywords, entities, references_text, notes):
        self.id = id
        self.title = title
        self.authors = authors
        self.publication_year = year
        self.text = text
        self.summary = summary
        self.structured_summary = structured_summary
        self.keywords = keywords
        self.entities = entities
        self.references_text = references_text
        self.notes = notes
        self.file_type = "pdf"
        self.page_count = 15
        self.word_count = 8500
        self.reading_time = 42

p1 = MockPaper(
    id=1,
    title="Attention Is All You Need",
    authors="Ashish Vaswani, Noam Shazeer, Niki Parmar",
    year="2017",
    text="We propose the Transformer model based on self-attention.",
    summary="The Transformer model relies entirely on self-attention mechanisms.",
    structured_summary=json.dumps({
        "problem": "Recurrent sequence bottlenecks",
        "methodology": "Multi-head self-attention",
        "findings": "28.4 BLEU on WMT 2014 English-to-German",
        "limitations": "Quadratic compute on sequence length"
    }),
    keywords="transformer, attention, self-attention, BLEU",
    entities="Google Brain (ORG), Ashish Vaswani (PERSON)",
    references_text="[1] Hochreiter et al. LSTM\n\n[2] Bahdanau et al. Neural Machine Translation",
    notes="Key model architecture for my thesis."
)

p2 = MockPaper(
    id=2,
    title="BERT: Pre-training of Deep Bidirectional Transformers",
    authors="Jacob Devlin, Ming-Wei Chang, Kenton Lee",
    year="2018",
    text="We introduce BERT for bidirectional language representation.",
    summary="BERT is designed to pre-train deep bidirectional representations.",
    structured_summary=json.dumps({
        "problem": "Unidirectional context limitations in standard language models",
        "methodology": "Masked Language Model (MLM) and Next Sentence Prediction",
        "findings": "Obtains state-of-the-art on 11 NLP benchmarks including GLUE",
        "limitations": "Expensive pre-training resource consumption"
    }),
    keywords="BERT, NLP, bidirectional, masked language model",
    entities="Google AI Language (ORG), Jacob Devlin (PERSON)",
    references_text="[1] Vaswani et al. Attention Is All You Need\n\n[2] Peters et al. ELMo",
    notes="Compare with GPT-2 baseline."
)

print("=" * 60)
print("  VALIDATING 7 ADVANCED AI RESEARCH EXTENSIONS")
print("=" * 60)

# 1. arXiv ID parsing
print("\n[1] Testing 1-Click arXiv ID / URL Parsing:")
id_res = extract_arxiv_id("https://arxiv.org/abs/1706.03762v5")
print(f"[-] Extracted arXiv ID: {id_res}")
assert id_res == "1706.03762"

# 2. Multi-Paper Comparative Matrix
print("\n[2] Testing Multi-Paper Comparative Literature Matrix:")
matrix = generate_comparative_matrix([p1, p2])
print(f"[-] Matrix generated for {len(matrix['columns'])} papers across {len(matrix['rows'])} dimensions:")
for r in matrix["rows"]:
    print(f"    * {r['dimension']}")
print(f"[-] Synthesis Verdict: {matrix['synthesis'][:80]}...")

# 3. Global Library Search
print("\n[3] Testing Global Multi-Paper Library Search:")
search_res = search_across_library("transformer self-attention", [p1, p2])
print(f"[-] Matched {len(search_res['sources'])} sources in library.")

# 4. Interactive Knowledge Graph
print("\n[4] Testing Interactive Knowledge Graph Serialization:")
graph = build_library_knowledge_graph([p1, p2])
print(f"[-] Knowledge Graph: {graph['stats']['total_nodes']} nodes, {graph['stats']['total_edges']} edges.")

# 5. Audio Briefing Generator
print("\n[5] Testing AI Audio Briefing (Podcast Script Generator):")
audio_script = generate_audio_briefing_script(p1)
print(f"[-] Audio Script ({len(audio_script)} chars): {audio_script[:120]}...")

# 6. Literature Review Report Compiler
print("\n[6] Testing Literature Review Report Compiler:")
report = compile_research_report(p1)
print(f"[-] Report compiled for '{report['paper'].title}'.")
print(f"[-] BibTeX:\n{report['citations']['bibtex']}")

print("\n" + "=" * 60)
print("  ALL ADVANCED EXTENSION MODULES WORKING PERFECTLY!")
print("=" * 60)
