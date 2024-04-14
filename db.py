from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

db = SQLAlchemy()

class Lecture(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text)
    length = db.Column(db.Integer)
    datetime = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    summary = db.Column(db.Text)