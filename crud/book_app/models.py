from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20), nullable=False)
    author = db.Column(db.String(20), nullable=False)
    isbn = db.Column(db.String(13), unique=True, nullable=False)
    published_date = db.Column(db.Date, nullable=False)