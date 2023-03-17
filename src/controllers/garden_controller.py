import json

from flask import Blueprint, Response, abort, request
from flask_jwt_extended import current_user, get_jwt, jwt_required
from marshmallow import ValidationError

from main import db
from models import Garden
from schemas import garden_schema, gardens_schema

garden_blueprint = Blueprint("gardens", __name__, url_prefix="/gardens")


@garden_blueprint.get("/")
@jwt_required()
def get_gardens():
    gardens = (
        db.session.execute(db.select(Garden).filter_by(user_id=current_user.user_id))
        .scalars()
        .all()
    )

    if not gardens:
        abort(404, description="user has no gardens")

    return gardens_schema.dump(gardens), 200
