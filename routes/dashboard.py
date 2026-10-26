from flask import Blueprint, render_template, session, redirect, request
from models.paper import Paper
from sqlalchemy import or_

dashboard = Blueprint("dashboard", __name__)


@dashboard.route("/dashboard")
def dashboard_page():
    if "user_id" not in session:
        return redirect("/login")

    search = request.args.get("search", "").strip()
    sort = request.args.get("sort", "latest")

    query = Paper.query.filter(Paper.user_id == session["user_id"])

    if search:
        search_filter = f"%{search}%"
        query = query.filter(
            or_(
                Paper.title.ilike(search_filter),
                Paper.authors.ilike(search_filter),
                Paper.keywords.ilike(search_filter)
            )
        )

    if sort == "latest":
        query = query.order_by(Paper.upload_date.desc())
    elif sort == "oldest":
        query = query.order_by(Paper.upload_date.asc())
    elif sort == "az":
        query = query.order_by(Paper.title.asc())
    elif sort == "za":
        query = query.order_by(Paper.title.desc())

    papers = query.all()
    total_papers = len(papers)

    total_pages = sum(paper.page_count or 0 for paper in papers)
    total_reading_time = sum(paper.reading_time or 0 for paper in papers)

    return render_template(
        "dashboard.html",
        name=session.get("user_name", "Researcher"),
        papers=papers,
        total_papers=total_papers,
        total_pages=total_pages,
        total_reading_time=total_reading_time,
        search=search,
        sort=sort
    )