from flask import Flask
from config import Config
from extensions import db, bcrypt

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
bcrypt.init_app(app)

# Import models so SQLAlchemy creates and tracks all tables
from models.user import User
from models.paper import Paper
from models.chat_message import ChatMessage

# Import blueprints
from routes.main import main
from routes.auth import auth
from routes.dashboard import dashboard
from routes.paper import paper

# Register blueprints
app.register_blueprint(main)
app.register_blueprint(auth)
app.register_blueprint(dashboard)
app.register_blueprint(paper)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)