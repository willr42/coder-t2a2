from main import db


class User(db.Model):
    __tablename__ = "users"

    user_id = db.Column(db.Integer, nullable=False, primary_key=True)
    full_name = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(), nullable=False, unique=True)
    expert = db.Column(db.Boolean, nullable=False, default=False)
