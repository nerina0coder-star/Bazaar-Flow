# init_db.py
from app import create_app
from app.extensions import db
from app.models import User, Chamber, Message, Item, participants

app = create_app()
with app.app_context():
    db.create_all()
    print("✅ Tables created successfully!")