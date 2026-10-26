from database.db import db
from extensions import db

class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)

    email = db.Column(db.String(120), unique=True, nullable=False)

    password = db.Column(db.String(255), nullable=False)

    created_at = db.Column(db.DateTime, server_default=db.func.now())

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

    
    def __repr__(self):
        return f"<User {self.name}>"