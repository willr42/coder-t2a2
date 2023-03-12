from main import db


class Garden(db.Model):
    __tablename__ = "gardens"

    garden_id = db.Column(db.Integer, nullable=False, primary_key=True)
    creation_date = db.Column(db.Date(), nullable=False)
    garden_type = db.Column(db.String(), nullable=False)

    user_id = db.Column(
        db.Integer, db.ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False
    )
    user = db.relationship("User", back_populates="garden")
