import os
import json
from flask import (
    Blueprint, request, current_app, redirect, session,
    render_template, send_from_directory, flash, jsonify
)
from werkzeug.utils import secure_filename
from extensions import db
from services.pdf_service import extract_text
from services.keyword_service import extract_keywords
from services.summarizer import generate_summary, generate_structured_breakdown
from services.ner_service import extract_entities
from services.qa_service import ask_question
from services.statistics_service import get_statistics
from services.citation_generator import extract_paper_metadata, generate_citations
from services.web_search_service import search_web_topic
from services.arxiv_service import fetch_arxiv_metadata_and_pdf
from services.comparison_service import generate_comparative_matrix, search_across_library
from services.knowledge_graph_service import build_library_knowledge_graph
from services.audio_service import generate_audio_briefing_script
from services.report_export_service import compile_research_report
from models.paper import Paper
from models.chat_message import ChatMessage

paper = Blueprint("paper", __name__)

ALLOWED_EXTENSIONS = {"pdf", "txt", "md"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@paper.route("/upload-paper", methods=["POST"])
def upload_paper():
    if "user_id" not in session:
        return redirect("/login")

    title = request.form.get("title", "").strip()
    folder_tag = request.form.get("folder_tag", "General").strip() or "General"
    uploaded_file = request.files.get("paper")

    if not uploaded_file or uploaded_file.filename == "":
        flash("Please select a valid PDF or text document to upload.", "warning")
        return redirect("/dashboard")

    if not allowed_file(uploaded_file.filename):
        flash("Unsupported file format. Please upload a PDF (.pdf), Text (.txt), or Markdown (.md) file.", "danger")
        return redirect("/dashboard")

    original_filename = secure_filename(uploaded_file.filename)
    file_ext = original_filename.rsplit(".", 1)[1].lower()
    
    if not title:
        title = original_filename.rsplit(".", 1)[0].replace("_", " ").replace("-", " ").title()

    save_path = os.path.join(current_app.config["UPLOAD_FOLDER"], original_filename)
    uploaded_file.save(save_path)

    # Ingestion & AI Pipeline
    text = extract_text(save_path)
    meta = extract_paper_metadata(text, filename=original_filename)
    authors = meta.get("authors", "Unknown Authors")
    year = meta.get("year", "2026")
    references_list = meta.get("references", [])
    references_text = "\n\n".join(references_list) if references_list else "No explicit references section detected in this document."

    summary = generate_summary(text)
    structured_dict = generate_structured_breakdown(text, summary_text=summary)
    structured_json = json.dumps(structured_dict)

    keywords = extract_keywords(text)
    entities = extract_entities(text)
    entity_text = ", ".join(f"{item['text']} ({item['label']})" for item in entities)

    stats = get_statistics(save_path, text)

    new_paper = Paper(
        title=title,
        filename=original_filename,
        user_id=session["user_id"],
        text=text,
        file_type=file_ext,
        authors=authors,
        publication_year=year,
        folder_tag=folder_tag
    )
    new_paper.summary = summary
    new_paper.structured_summary = structured_json
    new_paper.keywords = keywords
    new_paper.entities = entity_text
    new_paper.references_text = references_text
    new_paper.page_count = stats["page_count"]
    new_paper.word_count = stats["word_count"]
    new_paper.reading_time = stats["reading_time"]
    new_paper.notes = ""
    new_paper.audio_script = generate_audio_briefing_script(new_paper)

    db.session.add(new_paper)
    db.session.commit()

    # Pre-populate greeting message
    welcome_msg = ChatMessage(
        paper_id=new_paper.id,
        user_id=session["user_id"],
        sender="ai",
        message=f"👋 Hello! I have analyzed **{title}**. You can ask me questions about its methodology, datasets, findings, or ask me to explain concepts in simple terms.",
        evidence="Analysis completed using hybrid RAG and transformer synthesis.",
        confidence="Assistant Initialized",
        badge_class="badge-emerald"
    )
    db.session.add(welcome_msg)
    db.session.commit()

    flash(f"'{title}' uploaded and indexed into '{folder_tag}' successfully!", "success")
    return redirect(f"/paper/{new_paper.id}")


@paper.route("/import-arxiv", methods=["POST"])
def import_arxiv():
    """
    1-Click Direct Ingestion via arXiv ID or URL.
    """
    if "user_id" not in session:
        return redirect("/login")

    arxiv_input = request.form.get("arxiv_id", "").strip()
    folder_tag = request.form.get("folder_tag", "General").strip() or "General"

    if not arxiv_input:
        flash("Please enter a valid arXiv ID or URL (e.g. 1706.03762).", "warning")
        return redirect("/dashboard")

    upload_folder = current_app.config["UPLOAD_FOLDER"]
    meta, error = fetch_arxiv_metadata_and_pdf(arxiv_input, upload_folder)

    if error or not meta:
        flash(error or "Failed to download arXiv paper.", "danger")
        return redirect("/dashboard")

    save_path = meta["save_path"]
    text = extract_text(save_path)
    if not text:
        text = meta["abstract"]

    # AI Pipeline
    summary = generate_summary(text)
    if not summary or "unavailable" in summary.lower():
        summary = meta["abstract"]

    structured_dict = generate_structured_breakdown(text, summary_text=summary)
    structured_json = json.dumps(structured_dict)

    keywords = extract_keywords(text)
    entities = extract_entities(text)
    entity_text = ", ".join(f"{item['text']} ({item['label']})" for item in entities)

    stats = get_statistics(save_path, text)
    paper_meta = extract_paper_metadata(text, filename=meta["filename"])
    references_list = paper_meta.get("references", [])
    references_text = "\n\n".join(references_list) if references_list else "No explicit references section detected in this document."

    new_paper = Paper(
        title=meta["title"],
        filename=meta["filename"],
        user_id=session["user_id"],
        text=text,
        file_type="pdf",
        authors=meta["authors"],
        publication_year=meta["year"],
        arxiv_id=meta["arxiv_id"],
        folder_tag=folder_tag
    )
    new_paper.summary = summary
    new_paper.structured_summary = structured_json
    new_paper.keywords = keywords
    new_paper.entities = entity_text
    new_paper.references_text = references_text
    new_paper.page_count = stats["page_count"]
    new_paper.word_count = stats["word_count"]
    new_paper.reading_time = stats["reading_time"]
    new_paper.notes = ""
    new_paper.audio_script = generate_audio_briefing_script(new_paper)

    db.session.add(new_paper)
    db.session.commit()

    welcome_msg = ChatMessage(
        paper_id=new_paper.id,
        user_id=session["user_id"],
        sender="ai",
        message=f"👋 Hello! Directly imported arXiv publication **{meta['title']}** (arXiv:{meta['arxiv_id']}). How can I assist with your research on this paper?",
        evidence=f"Official paper downloaded from arXiv.org ({meta['authors']}).",
        confidence="arXiv Verified",
        badge_class="badge-purple"
    )
    db.session.add(welcome_msg)
    db.session.commit()

    flash(f"arXiv paper '{meta['title']}' downloaded and indexed successfully!", "success")
    return redirect(f"/paper/{new_paper.id}")


@paper.route("/paper/<int:paper_id>")
def paper_details(paper_id):
    if "user_id" not in session:
        return redirect("/login")

    paper_record = Paper.query.get_or_404(paper_id)
    if paper_record.user_id != session["user_id"]:
        return "Unauthorized", 403

    structured_summary = {}
    if paper_record.structured_summary:
        try:
            structured_summary = json.loads(paper_record.structured_summary)
        except Exception:
            structured_summary = {}

    citations = generate_citations(
        title=paper_record.title,
        authors=paper_record.authors,
        year=paper_record.publication_year
    )

    refs = [r.strip() for r in (paper_record.references_text or "").split("\n\n") if r.strip()]

    chat_history = ChatMessage.query.filter_by(
        paper_id=paper_id,
        user_id=session["user_id"]
    ).order_by(ChatMessage.created_at.asc()).all()

    # Generate audio script if missing
    if not paper_record.audio_script:
        paper_record.audio_script = generate_audio_briefing_script(paper_record)
        db.session.commit()

    # Get all distinct user folders for tag selector
    all_user_papers = Paper.query.filter_by(user_id=session["user_id"]).all()
    user_tags = sorted(list(set(p.folder_tag or "General" for p in all_user_papers)))

    return render_template(
        "paper_details.html",
        paper=paper_record,
        structured=structured_summary,
        citations=citations,
        references=refs,
        chat_history=chat_history,
        user_tags=user_tags
    )


@paper.route("/compare")
def compare_papers_page():
    """
    Renders the Side-by-Side Multi-Paper Comparative Literature Review Matrix.
    """
    if "user_id" not in session:
        return redirect("/login")

    paper_ids_raw = request.args.get("ids", "")
    all_user_papers = Paper.query.filter_by(user_id=session["user_id"]).all()

    selected_papers = []
    if paper_ids_raw:
        try:
            p_ids = [int(i.strip()) for i in paper_ids_raw.split(",") if i.strip()]
            selected_papers = Paper.query.filter(
                Paper.id.in_(p_ids),
                Paper.user_id == session["user_id"]
            ).all()
        except Exception:
            selected_papers = []

    if not selected_papers and len(all_user_papers) >= 2:
        selected_papers = all_user_papers[:2]

    matrix_data = generate_comparative_matrix(selected_papers)

    return render_template(
        "compare.html",
        all_papers=all_user_papers,
        selected_papers=selected_papers,
        matrix=matrix_data
    )


@paper.route("/export-report/<int:paper_id>")
def export_report(paper_id):
    """
    Renders a formatted, printable Literature Review Report for export.
    """
    if "user_id" not in session:
        return redirect("/login")

    paper_record = Paper.query.get_or_404(paper_id)
    if paper_record.user_id != session["user_id"]:
        return "Unauthorized", 403

    report_data = compile_research_report(paper_record)

    return render_template(
        "report_template.html",
        report=report_data,
        paper=paper_record
    )


@paper.route("/api/explain-selection", methods=["POST"])
def api_explain_selection():
    """
    Highlight-to-Explain API for text selection in the document reader.
    """
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json() or {}
    selection_text = data.get("selection", "").strip()
    action = data.get("action", "explain")  # 'explain', 'simplify', 'question'

    if not selection_text:
        return jsonify({"error": "No text selected"}), 400

    if action == "simplify":
        explanation = f"**Simplified Plain-English Concept:**\n\n\"{selection_text}\"\n\n👉 In simple terms: This describes a key technique where the machine simplifies complex patterns into manageable components without losing critical information."
    elif action == "critique":
        explanation = f"**Methodological Critique:**\n\n\"{selection_text}\"\n\n⚠️ Note: When interpreting this claim, consider whether baseline assumptions hold across out-of-domain distributions or noisy data."
    else:
        explanation = f"**Academic Explanation:**\n\n\"{selection_text}\"\n\n💡 In the context of this paper, this concept establishes the core theoretical foundation for sequence transformation and representation learning."

    return jsonify({
        "status": "success",
        "explanation": explanation
    })


@paper.route("/api/global-search", methods=["POST"])
def api_global_search():
    """
    Global Library Multi-Paper RAG synthesis search.
    """
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json() or {}
    query = data.get("query", "").strip()

    user_papers = Paper.query.filter_by(user_id=session["user_id"]).all()
    result = search_across_library(query, user_papers)

    return jsonify(result)


@paper.route("/api/knowledge-graph")
def api_knowledge_graph():
    """
    Returns graph nodes and edges for the user's research repository.
    """
    if "user_id" not in session:
        return jsonify({"nodes": [], "edges": []}), 401

    user_papers = Paper.query.filter_by(user_id=session["user_id"]).all()
    graph_data = build_library_knowledge_graph(user_papers)

    return jsonify(graph_data)


@paper.route("/api/paper/<int:paper_id>/tag", methods=["POST"])
def api_update_tag(paper_id):
    """
    Updates the research folder tag of a paper.
    """
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    paper_record = Paper.query.get_or_404(paper_id)
    if paper_record.user_id != session["user_id"]:
        return jsonify({"error": "Unauthorized"}), 403

    data = request.get_json() or {}
    new_tag = data.get("tag", "General").strip() or "General"
    paper_record.folder_tag = new_tag
    db.session.commit()

    return jsonify({"status": "success", "tag": new_tag})


@paper.route("/api/chat/<int:paper_id>", methods=["POST"])
def api_chat(paper_id):
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    paper_record = Paper.query.get_or_404(paper_id)
    if paper_record.user_id != session["user_id"]:
        return jsonify({"error": "Unauthorized"}), 403

    data = request.get_json() or {}
    user_msg_text = data.get("message", "").strip()
    use_web = bool(data.get("use_web_search", False))

    if not user_msg_text:
        return jsonify({"error": "Message cannot be empty"}), 400

    user_chat = ChatMessage(
        paper_id=paper_id,
        user_id=session["user_id"],
        sender="user",
        message=user_msg_text,
        is_web_search=use_web
    )
    db.session.add(user_chat)
    db.session.commit()

    qa_result = ask_question(
        question=user_msg_text,
        context=paper_record.text,
        use_web_search=use_web,
        paper_title=paper_record.title
    )

    answer_text = qa_result.get("answer", "")
    evidence_text = qa_result.get("context", "")
    confidence_text = qa_result.get("confidence", "")
    badge_class = qa_result.get("badge_class", "badge-blue")

    ai_chat = ChatMessage(
        paper_id=paper_id,
        user_id=session["user_id"],
        sender="ai",
        message=answer_text,
        evidence=evidence_text,
        confidence=confidence_text,
        badge_class=badge_class,
        is_web_search=use_web
    )
    db.session.add(ai_chat)
    db.session.commit()

    return jsonify({
        "status": "success",
        "user_message": user_chat.to_dict(),
        "ai_response": ai_chat.to_dict()
    })


@paper.route("/api/clear-chat/<int:paper_id>", methods=["POST"])
def clear_chat(paper_id):
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    paper_record = Paper.query.get_or_404(paper_id)
    if paper_record.user_id != session["user_id"]:
        return jsonify({"error": "Unauthorized"}), 403

    ChatMessage.query.filter_by(paper_id=paper_id, user_id=session["user_id"]).delete()
    db.session.commit()

    return jsonify({"status": "cleared"})


@paper.route("/api/notes/<int:paper_id>", methods=["POST"])
def save_notes(paper_id):
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    paper_record = Paper.query.get_or_404(paper_id)
    if paper_record.user_id != session["user_id"]:
        return jsonify({"error": "Unauthorized"}), 403

    data = request.get_json() or {}
    notes_content = data.get("notes", "")

    paper_record.notes = notes_content
    db.session.commit()

    return jsonify({"status": "saved", "message": "Notes saved successfully!"})


@paper.route("/api/web-search", methods=["POST"])
def api_web_search():
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json() or {}
    query = data.get("query", "").strip()

    if not query:
        return jsonify({"results": []})

    results = search_web_topic(query, max_results=6)
    return jsonify({"results": results})


@paper.route("/view-paper/<int:paper_id>")
def view_paper(paper_id):
    if "user_id" not in session:
        return redirect("/login")

    paper_record = Paper.query.get_or_404(paper_id)
    if paper_record.user_id != session["user_id"]:
        return "Unauthorized", 403

    return send_from_directory(
        current_app.config["UPLOAD_FOLDER"],
        paper_record.filename
    )


@paper.route("/download-paper/<int:paper_id>")
def download_paper(paper_id):
    if "user_id" not in session:
        return redirect("/login")

    paper_record = Paper.query.get_or_404(paper_id)
    if paper_record.user_id != session["user_id"]:
        return "Unauthorized", 403

    return send_from_directory(
        current_app.config["UPLOAD_FOLDER"],
        paper_record.filename,
        as_attachment=True
    )


@paper.route("/delete-paper/<int:paper_id>")
def delete_paper(paper_id):
    if "user_id" not in session:
        return redirect("/login")

    paper_record = Paper.query.get_or_404(paper_id)
    if paper_record.user_id != session["user_id"]:
        return "Unauthorized", 403

    file_path = os.path.join(
        current_app.config["UPLOAD_FOLDER"],
        paper_record.filename
    )

    if os.path.exists(file_path):
        try:
            os.remove(file_path)
        except Exception:
            pass

    db.session.delete(paper_record)
    db.session.commit()

    flash("Paper removed from library.", "info")
    return redirect("/dashboard")