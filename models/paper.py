from extensions import db


class Paper(db.Model):
    __tablename__ = "papers"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=False)
    filename = db.Column(db.String(300), nullable=False)
    file_type = db.Column(db.String(20), default="pdf")
    
    # Academic Identifiers & Collections
    arxiv_id = db.Column(db.String(100), nullable=True)
    doi = db.Column(db.String(100), nullable=True)
    folder_tag = db.Column(db.String(100), default="General")

    # Metadata
    authors = db.Column(db.String(500), default="Unknown Authors")
    publication_year = db.Column(db.String(50), default="2026")
    
    # Full Extracted Document Text
    text = db.Column(db.Text)

    # AI-generated content
    summary = db.Column(db.Text)
    structured_summary = db.Column(db.Text)  # JSON formatted sections
    keywords = db.Column(db.Text)
    entities = db.Column(db.Text)
    references_text = db.Column(db.Text)
    audio_script = db.Column(db.Text, nullable=True)  # Spoken briefing script
    
    # Document Metrics
    page_count = db.Column(db.Integer, default=1)
    word_count = db.Column(db.Integer, default=0)
    reading_time = db.Column(db.Integer, default=1)

    # Research User Notes
    notes = db.Column(db.Text, default="")

    upload_date = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id")
    )

    # Relationship to ChatMessages
    chat_messages = db.relationship(
        "ChatMessage",
        backref="paper",
        cascade="all, delete-orphan",
        lazy=True,
        order_by="ChatMessage.created_at.asc()"
    )

    def __init__(self, title, filename, user_id, text=None, file_type="pdf", authors="Unknown Authors", publication_year="2026", arxiv_id=None, doi=None, folder_tag="General"):
        self.title = title
        self.filename = filename
        self.user_id = user_id
        self.text = text
        self.file_type = file_type
        self.authors = authors
        self.publication_year = publication_year
        self.arxiv_id = arxiv_id
        self.doi = doi
        self.folder_tag = folder_tag