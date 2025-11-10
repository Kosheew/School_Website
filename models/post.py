from app import db
from datetime import datetime

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    content = db.Column(db.Text, nullable=False)
    file_path = db.Column(db.String(200))
    date_posted = db.Column(db.Date, default=datetime.utcnow)
    scheduled_date = db.Column(db.Date, nullable=True)
    category = db.Column(db.String(50), nullable=False, default='index')  # Додайте це поле
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}', '{self.category}')"