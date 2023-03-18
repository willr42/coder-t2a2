from datetime import timedelta

from flask import Blueprint, abort, request
from flask_jwt_extended import create_access_token
from marshmallow.exceptions import ValidationError

from main import bcrypt, db
from models import User
from schemas import user_schema

auth_blueprint = Blueprint("auth", __name__, url_prefix="/auth")


@auth_blueprint.route("/register", methods=["POST"])
def register_user():
    """Registers a new user.

    Returns:
        _token_: _JWT_
    """
    try:
        user_fields = user_schema.load(request.json)
    except ValidationError as e:
        abort(400, description=e)

    # This db query selects all the users, filtered by their email, and returns a list that matches. 
    # Because emails are enforced uniqueness, this will be only ever return the one email, or null.
    existing_user = db.session.execute(
        db.select(User).filter_by(email=user_fields["email"])
    ).scalar()

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
        identity=str(new_user.user_id),
        expires_delta=expiry,
        additional_claims={"expert": new_user.expert},
    )

    return {"token": access_token}


@auth_blueprint.route("/login", methods=["POST"])
def login_user():
    """Logs an existing user in.

    Returns:
        token: JWT
    """
    try:
        user_fields = user_schema.load(request.json)
    except ValidationError as e:
        abort(401, description=e)

    # This db query selects all the users, filtered by their email, and returns one that matches.
    # This is the equivalent of a SELECT FROM WHERE in SQL.
    user = db.session.execute(
        db.select(User).filter_by(email=user_fields["email"])
    ).scalar()

    if not user or not bcrypt.check_password_hash(
        pw_hash=user.password, password=user_fields["password"]
    ):
        return abort(401, description="Username or password incorrect")

    expiry = timedelta(days=1)
    access_token = create_access_token(
        identity=str(user.user_id),
        expires_delta=expiry,
        additional_claims={"expert": user.expert},
    )

    return {"token": access_token}
