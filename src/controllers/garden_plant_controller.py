from flask import Blueprint, Response, abort, request
from flask_jwt_extended import current_user, jwt_required
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
    # This db call uses the primary key of garden_id to retrieve a Garden object
    garden = db.session.get(Garden, garden_id)

    if not garden:
        abort(404, description="garden_id does not exist")

    if garden.user_id != current_user.user_id:
        abort(401)

    # This db call selects all the GardenPlants that belong to this particular garden_id
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
    # This db call uses the primary key of garden_id to retrieve a Garden object
    garden = db.session.get(Garden, garden_id)

    if not garden:
        abort(404, description="garden_id does not exist")

    if garden.user_id != current_user.user_id:
        abort(401)

    # This db call selects one GardenPlant by filtering on garden_plant_id, but we check
    # the garden_id so that if this doesn't match our route, we can throw an error
    garden_plant = db.session.execute(
        db.select(GardenPlant).filter_by(
            garden_plant_id=garden_plant_id, garden_id=garden_id
        )
    ).scalar()

    if not garden_plant:
        abort(404, description="garden_plant does not exist in this garden")

    return garden_plant_schema_no_id.dump(garden_plant)


@garden_plant_blueprint.post("/<int:garden_id>/")
@jwt_required()
def post_garden_plant(garden_id):
    """Adds a particular plant to a particular garden

    Returns:
        JSON
    """
    # This db call uses the primary key of garden_id to retrieve a Garden object
    garden = db.session.get(Garden, garden_id)

    if not garden:
        abort(404, description="garden_id does not exist")

    if garden.user_id != current_user.user_id:
        abort(401)

    try:
        new_plant_fields = garden_plant_schema_no_id.load(request.json)
    except ValidationError as e:
        abort(400, description=e)

    # This db call uses the primary key of plant_id to retrieve a Plant object
    plant_type = db.session.get(Plant, new_plant_fields["plant_id"])

    if not plant_type:
        abort(404, description="plant id not found")

    new_garden_plant = GardenPlant()
    new_garden_plant.garden_id = garden.garden_id
    new_garden_plant.plant_id = plant_type.plant_id
    new_garden_plant.last_watered = new_plant_fields["last_watered"]
    new_garden_plant.placement = new_plant_fields["placement"]
    new_garden_plant.healthiness = new_plant_fields["healthiness"]

    db.session.add(new_garden_plant)
    db.session.commit()

    return garden_plant_schema.dump(new_garden_plant)


@garden_plant_blueprint.put("/<int:garden_id>/<int:garden_plant_id>")
@jwt_required()
def update_garden_plant(garden_id, garden_plant_id):
    """Updates a user's specific plant in their garden

    Returns:
        JSON
    """
    # This db call uses the primary key of garden_id to retrieve a Garden object
    garden = db.session.get(Garden, garden_id)

    if not garden:
        abort(404, description="garden_id does not exist")

    if garden.user_id != current_user.user_id:
        abort(401)

    try:
        fields_to_update = garden_plant_schema.load(
            request.json,
            partial=(
                "garden_plant_id",
                "garden_id",
                "last_watered",
                "placement",
                "healthiness",
                "plant",
            ),
        )
    except ValidationError as e:
        abort(400, description=e)

    # This db call returns the GardenPlant in this current Garden, or null if they don't exist
    existing_garden_plant = db.session.execute(
        db.select(GardenPlant)
        .filter_by(garden_plant_id=garden_plant_id)
        .filter_by(garden_id=garden_id)
    ).scalar()

    if not existing_garden_plant:
        abort(404, description="garden_plant does not exist in this garden")

    for field in fields_to_update:
        # Users can't change these fields
        if field == "plant" or field == "garden_plant_id":
            continue
        elif field == "garden_id":
            # This db call uses a primary key lookup to get a garden. If that garden doesn't match the garden they're trying to
            # change, we error, as they are unauthorized.
            new_garden = db.session.get(Garden, fields_to_update[field])
            if new_garden.user_id != current_user.user_id:
                abort(401)

        setattr(existing_garden_plant, field, fields_to_update[field])

    db.session.commit()

    return garden_plant_schema_no_id.dump(existing_garden_plant), 200


@garden_plant_blueprint.delete("/<int:garden_id>/<int:garden_plant_id>")
@jwt_required()
def delete_garden_plant(garden_id, garden_plant_id):
    """Deletes a particular plant from a particular garden

    Returns:
        JSON
    """
    # This db call uses the primary key of garden_id to retrieve a Garden object
    garden = db.session.get(Garden, garden_id)

    if not garden:
        abort(404, description="garden_id does not exist")

    if garden.user_id != current_user.user_id:
        abort(401)

    # This db call returns the GardenPlant in this current Garden, or null if they don't exist
    garden_plant = db.session.execute(
        db.select(GardenPlant)
        .filter_by(garden_plant_id=garden_plant_id)
        .filter_by(garden_id=garden_id)
    ).scalar()

    if not garden_plant:
        abort(404, description="garden_plant does not exist in this garden")

    db.session.delete(garden_plant)
    db.session.commit()

    return Response(status=204)
