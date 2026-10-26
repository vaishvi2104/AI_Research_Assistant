import re


def build_library_knowledge_graph(papers):
    """
    Builds nodes and edges representing the interconnected research graph
    (Papers, Authors, Topics, and Technologies) across the user's library.
    """
    nodes = []
    edges = []
    
    seen_nodes = set()
    edge_id = 1

    for paper in papers:
        paper_node_id = f"paper_{paper.id}"
        if paper_node_id not in seen_nodes:
            seen_nodes.add(paper_node_id)
            nodes.append({
                "id": paper_node_id,
                "label": paper.title[:30] + ("..." if len(paper.title) > 30 else ""),
                "full_title": paper.title,
                "group": "paper",
                "color": "#2563eb",
                "shape": "dot",
                "size": 26,
                "paper_id": paper.id,
                "title": f"<b>Paper:</b> {paper.title}<br><b>Year:</b> {paper.publication_year or '2026'}"
            })

        # 1. Author Nodes & Edges
        if paper.authors and paper.authors != "Unknown Authors":
            author_names = [a.strip() for a in re.split(r'[,;&]| and ', paper.authors) if len(a.strip()) > 2]
            for auth in author_names[:3]:
                auth_id = f"author_{auth.lower().replace(' ', '_')}"
                if auth_id not in seen_nodes:
                    seen_nodes.add(auth_id)
                    nodes.append({
                        "id": auth_id,
                        "label": auth,
                        "group": "author",
                        "color": "#059669",
                        "shape": "circle",
                        "size": 18,
                        "title": f"<b>Author:</b> {auth}"
                    })
                
                edges.append({
                    "id": f"edge_{edge_id}",
                    "from": paper_node_id,
                    "to": auth_id,
                    "color": {"color": "#a7f3d0", "highlight": "#059669"},
                    "label": "authored"
                })
                edge_id += 1

        # 2. Keyword & Concept Nodes & Edges
        if paper.keywords:
            keywords = [k.strip() for k in paper.keywords.split(",") if len(k.strip()) > 2]
            for kw in keywords[:5]:
                kw_id = f"kw_{kw.lower().replace(' ', '_')}"
                if kw_id not in seen_nodes:
                    seen_nodes.add(kw_id)
                    nodes.append({
                        "id": kw_id,
                        "label": kw,
                        "group": "concept",
                        "color": "#7c3aed",
                        "shape": "diamond",
                        "size": 16,
                        "title": f"<b>Key Concept:</b> {kw}"
                    })
                
                edges.append({
                    "id": f"edge_{edge_id}",
                    "from": paper_node_id,
                    "to": kw_id,
                    "color": {"color": "#ddd6fe", "highlight": "#7c3aed"},
                    "label": "topic"
                })
                edge_id += 1

    return {
        "nodes": nodes,
        "edges": edges,
        "stats": {
            "total_nodes": len(nodes),
            "total_edges": len(edges)
        }
    }
