from extensions import db
from datetime import datetime


class ChatMessage(db.Model):
    __tablename__ = "chat_messages"

    id = db.Column(db.Integer, primary_key=True)
    paper_id = db.Column(db.Integer, db.ForeignKey("papers.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    
    sender = db.Column(db.String(10), nullable=False)  # 'user' or 'ai'
    message = db.Column(db.Text, nullable=False)
    evidence = db.Column(db.Text, nullable=True)  # Supporting sentence or web citation
    confidence = db.Column(db.String(50), nullable=True)
    badge_class = db.Column(db.String(50), nullable=True)
    is_web_search = db.Column(db.Boolean, default=False)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "sender": self.sender,
            "message": self.message,
            "evidence": self.evidence,
            "confidence": self.confidence,
            "badge_class": self.badge_class,
            "is_web_search": self.is_web_search,
            "created_at": self.created_at.strftime("%H:%M") if self.created_at else ""
        }
