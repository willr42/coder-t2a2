import json

from flask import Blueprint, Response, abort, jsonify, request
from flask_jwt_extended import current_user, get_jwt, jwt_required
from marshmallow import ValidationError

from main import db
from models import Garden, GardenPlant, Plant
from schemas import garden_plant_schema, garden_plant_schema_no_id, garden_plants_schema

garden_plant_blueprint = Blueprint(
    "garden_plants", __name__, url_prefix="/gardenplants"
)


@garden_plant_blueprint.get("/<int:garden_id>")
@jwt_required()
def get_garden_plants(garden_id):
    """Gets all plants for a particular garden

    Returns:
        JSON
    """
    garden = db.session.get(Garden, garden_id)

    if not garden:
        abort(404, description="garden_id does not exist")

    if garden.user_id != current_user.user_id:
        abort(401)

    garden_plant_list = (
        db.session.execute(db.select(GardenPlant).filter_by(garden_id=garden_id))
        .scalars()
        .all()
    )

    return garden_plants_schema.dump(garden_plant_list)


@garden_plant_blueprint.get("/<int:garden_id>/<int:garden_plant_id>")
@jwt_required()
def get_garden_plant(garden_id, garden_plant_id):
    """Gets a particular plant from a particular garden

    Returns:
        JSON
    """
    # Check they're getting their own Garden
    garden = db.session.get(Garden, garden_id)

    if not garden:
        abort(404, description="garden_id does not exist")

    if garden.user_id != current_user.user_id:
        abort(401)

    # Find the plant

    garden_plant = db.session.execute(
        db.select(GardenPlant).filter_by(garden_plant_id=garden_plant_id)
    ).scalar()

    if not garden_plant:
        abort(404, description="garden_plant_id does not exist")

    return garden_plant_schema_no_id.dump(garden_plant)


@garden_plant_blueprint.put("/<int:garden_id>/<int:garden_plant_id>")
@jwt_required()
def update_garden_plant(garden_id, garden_plant_id):
    """Updates a user's specific plant in their garden

    Returns:
        JSON
    """
    # Check they're getting their own Garden
    garden = db.session.get(Garden, garden_id)

    if not garden:
        abort(404, description="garden_id does not exist")

    if garden.user_id != current_user.user_id:
        abort(401)

    try:
        # request.json.update({"plant_id": plant_id})
        fields_to_update = garden_plant_schema.load(
            request.json,
            partial=(
                "garden_id",
                "last_watered",
                "placement",
                "healthiness",
            ),
        )
    except ValidationError as e:
        abort(400, description=e)

    existing_plant = db.session.get(Plant, plant_id)

    if not existing_plant:
        abort(404, description="plant_id does not exist")

    if fields_to_update["name"]:
        clashing_name = db.session.execute(
            db.select(Plant).filter_by(name=fields_to_update["name"])
        ).scalar()

    # TODO: can we make this into a handler rather than in-line here?
    if existing_plant:
        res = Response(
            status=409,
            mimetype="application/json",
            response=json.dumps(
                {
                    "error": "Plant by that name already exists",
                    "resource": existing_plant.plant_id,
                }
            ),
        )
        abort(res)

    for field in fields_to_update:
        setattr(existing_plant, field, fields_to_update[field])

        # existing_plant
    db.session.commit()

    return plant_schema.dump(existing_plant), 200
