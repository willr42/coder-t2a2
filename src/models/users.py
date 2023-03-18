from main import db, jwt


class User(db.Model):
    __tablename__ = "users"

    user_id = db.Column(db.Integer, nullable=False, primary_key=True)
    full_name = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(), nullable=False, unique=True)
    password = db.Column(db.String(), nullable=False)
    expert = db.Column(db.Boolean, nullable=False, default=False)

    garden = db.relationship("Garden", back_populates="user")


# This middleware allows us to access the current_user object inside routes
@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.filter_by(user_id=identity).one_or_none()
