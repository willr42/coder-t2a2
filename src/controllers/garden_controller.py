import datetime

from flask import Blueprint, abort, request
from flask_jwt_extended import current_user, jwt_required
from marshmallow import ValidationError

from main import db
from models import Garden
from schemas import garden_schema, gardens_schema

garden_blueprint = Blueprint("gardens", __name__, url_prefix="/gardens")


@garden_blueprint.get("/")
@jwt_required()
def get_gardens():
    """Gets all gardens of the current user's id

    Returns:
        JSON
    """
    gardens = (
        db.session.execute(db.select(Garden).filter_by(user_id=current_user.user_id))
        .scalars()
        .all()
    )

    if not gardens:
        abort(404, description="user has no gardens")

    return gardens_schema.dump(gardens), 200


@garden_blueprint.post("/")
@jwt_required()
def create_garden():
    """Creates a new garden for the given user's id

    Returns:
        JSON
    """
    try:
        garden_fields = garden_schema.load(request.json)
    except ValidationError as e:
        abort(400, description=e)

    new_garden = Garden()
    new_garden.creation_date = datetime.date.today().isoformat()
    new_garden.garden_type = garden_fields["garden_type"]
    new_garden.user_id = current_user.user_id

    db.session.add(new_garden)
    db.session.commit()

    return garden_schema.dump(new_garden)


@garden_blueprint.delete("/<int:garden_id>")
@jwt_required()
def delete_garden(garden_id):
    """Deletes a garden for the given user's id"""
    existing_garden = db.session.get(Garden, garden_id)

    if not existing_garden:
        abort(404, description="garden_id does not exist")

    if current_user.user_id != existing_garden.user_id:
        abort(401)

    db.session.delete(existing_garden)
    db.session.commit()

    return garden_schema.dump(existing_garden), 204
