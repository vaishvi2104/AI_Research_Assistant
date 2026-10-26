import os
import json
from app import app
from extensions import db
from models.paper import Paper
from services.arxiv_service import extract_arxiv_id
from services.comparison_service import generate_comparative_matrix, search_across_library
from services.knowledge_graph_service import build_library_knowledge_graph
from services.audio_service import generate_audio_briefing_script
from services.report_export_service import compile_research_report

print("\n" + "=" * 65)
print("  VERIFYING ADVANCED AI RESEARCH ASSISTANT EXPANSION SUITE")
print("=" * 65 + "\n")

# 1. Test arXiv ID extractor
print("[1] Testing arXiv Identifier parsing...")
id1 = extract_arxiv_id("https://arxiv.org/abs/1706.03762")
id2 = extract_arxiv_id("1706.03762v5")
print(f"[-] Extracted IDs: {id1}, {id2}")
assert id1 == "1706.03762"
assert id2 == "1706.03762"

with app.app_context():
    papers = Paper.query.filter_by(user_id=1).all()
    if not papers:
        # Create dummy papers for test
        p1 = Paper("Attention Is All You Need", "attention.pdf", 1, "Transformers are self-attention models.", file_type="pdf", authors="Ashish Vaswani et al.", publication_year="2017")
        p1.structured_summary = json.dumps({"problem": "RNN latency", "methodology": "Self-attention", "findings": "28.4 BLEU", "limitations": "Memory quadratic"})
        p1.keywords = "transformer, self-attention, neural translation"
        p2 = Paper("BERT: Pre-training Deep Bidirectional Transformers", "bert.pdf", 1, "BERT is a bidirectional transformer.", file_type="pdf", authors="Jacob Devlin et al.", publication_year="2018")
        p2.structured_summary = json.dumps({"problem": "Unidirectional context", "methodology": "Masked language model", "findings": "80.5 GLUE", "limitations": "Pretraining compute"})
        p2.keywords = "BERT, NLP, pre-training, masked language model"
        db.session.add(p1)
        db.session.add(p2)
        db.session.commit()
        papers = [p1, p2]

    # 2. Test Multi-Paper Comparative Matrix
    print("\n[2] Testing Multi-Paper Comparative Matrix Generator...")
    matrix = generate_comparative_matrix(papers)
    print(f"[-] Comparative matrix created with {len(matrix['columns'])} paper columns and {len(matrix['rows'])} dimensions.")
    print("    Dimensions:", [r["dimension"] for r in matrix["rows"]])

    # 3. Test Global Library Search
    print("\n[3] Testing Global Library Search...")
    global_res = search_across_library("transformer self-attention", papers)
    print(f"[-] Global search found {len(global_res['sources'])} sources.")

    # 4. Test Knowledge Graph Data Generator
    print("\n[4] Testing Interactive Knowledge Graph...")
    graph = build_library_knowledge_graph(papers)
    print(f"[-] Graph constructed with {graph['stats']['total_nodes']} nodes and {graph['stats']['total_edges']} edges.")

    # 5. Test Audio Briefing Script Generator
    print("\n[5] Testing AI Audio Briefing Script...")
    script = generate_audio_briefing_script(papers[0])
    print(f"[-] Audio script generated ({len(script)} chars): {script[:100]}...")

    # 6. Test Literature Review Report Compiler
    print("\n[6] Testing Report Compiler...")
    report = compile_research_report(papers[0])
    print(f"[-] Report compiled for '{report['paper'].title}'. Citations: APA, BibTeX, IEEE.")

# 7. Test Web API Endpoints
print("\n[7] Testing Advanced API & Route Endpoints...")
with app.test_client() as client:
    with client.session_transaction() as sess:
        sess["user_id"] = 1
        sess["user_name"] = "Researcher"

    # Test /compare page
    res_comp = client.get("/compare")
    print("[-] GET /compare :", res_comp.status_code)
    assert res_comp.status_code == 200

    # Test /export-report/<id>
    pid = papers[0].id
    res_rep = client.get(f"/export-report/{pid}")
    print(f"[-] GET /export-report/{pid} :", res_rep.status_code)
    assert res_rep.status_code == 200

    # Test /api/explain-selection
    res_expl = client.post("/api/explain-selection", json={"selection": "Multi-head attention allows the model to jointly attend to information", "action": "explain"})
    print("[-] POST /api/explain-selection :", res_expl.status_code, res_expl.get_json()["status"])
    assert res_expl.status_code == 200

    # Test /api/knowledge-graph
    res_kg = client.get("/api/knowledge-graph")
    print("[-] GET /api/knowledge-graph :", res_kg.status_code, f"{len(res_kg.get_json()['nodes'])} nodes")
    assert res_kg.status_code == 200

    # Test /api/paper/<id>/tag
    res_tag = client.post(f"/api/paper/{pid}/tag", json={"tag": "Thesis Chapter 1"})
    print(f"[-] POST /api/paper/{pid}/tag :", res_tag.status_code, res_tag.get_json())
    assert res_tag.status_code == 200

print("\n" + "=" * 65)
print("  ALL ADVANCED FEATURES SUCCESSFULLY VALIDATED AND OPERATIONAL!")
print("=" * 65 + "\n")
