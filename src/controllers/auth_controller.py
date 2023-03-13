from datetime import timedelta

from flask import Blueprint, abort, request
from flask_jwt_extended import create_access_token
from marshmallow.exceptions import ValidationError

from main import bcrypt, db
from models.users import User
from schemas.user_schema import user_schema

auth = Blueprint("auth", __name__, url_prefix="/auth")


def validate_user_req(request):
    """Validate a user request is appropriate format and contains required fields."""
    try:
        user_fields = user_schema.load(request.json)
    except ValidationError:
        return abort(400, description="Your request is missing a required field")

    error = user_schema.validate(user_fields)

    if error:
        return error

    return user_fields


@auth.route("/register", methods=["POST"])
def register_user():
    user_fields = validate_user_req(request)

    existing_user = db.session.execute(
        db.select(User).filter_by(email=user_fields["email"])
    ).scalar_one()

    if existing_user:
        # Don't want to allow malicious actors to enumerate emails here
        return abort(400, description="Incorrect request. Please contact support")

    new_user = User()
    new_user.full_name = user_fields["full_name"]
    new_user.email = user_fields["email"]
    new_user.password = bcrypt.generate_password_hash(user_fields["password"]).decode(
        "utf-8"
    )
    db.session.add(new_user)
    db.session.commit()

    expiry = timedelta(days=1)
    access_token = create_access_token(
        identity=str(new_user.user_id), expires_delta=expiry
    )

    return {"token": access_token}
