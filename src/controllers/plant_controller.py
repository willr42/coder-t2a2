import json

from flask import Blueprint, Response, abort, request
from flask_jwt_extended import get_jwt, jwt_required
from marshmallow import ValidationError

from main import db
from models import Plant
from schemas import plant_schema, plants_schema

plant_blueprint = Blueprint("plants", __name__, url_prefix="/plants")


@plant_blueprint.get("/")
def get_plants():
    """Gets all plants in the database

    Returns:
        JSON
    """
    # This db call retrieves every Plant in the database
    plant_list = db.session.execute(db.select(Plant)).scalars().all()

    return plants_schema.dump(plant_list)


@plant_blueprint.get("/<int:plant_id>")
def get_plant(plant_id):
    """Gets a plant in the database by id

    Returns:
        JSON
    """
    # This db call uses the primary key of plant_id to retrieve a Plant object
    plant = db.session.get(Plant, plant_id)

    if not plant:
        abort(404, description="plant_id does not exist")

    return plant_schema.dump(plant), 200


@plant_blueprint.post("/")
@jwt_required()
def add_plant():
    """If a user is an expert, adds a new plant to the database

    Returns:
        JSON
    """
    jwt_claims = get_jwt()

    if not jwt_claims.get("expert", False):
        abort(401)

    try:
        new_plant_fields = plant_schema.load(request.json)
    except ValidationError as e:
        abort(400, description=e)

    # This db call retrieves an existing plant by name. Because name is unique, we'll only get back one or null
    existing_plant = db.session.execute(
        db.select(Plant).filter_by(name=new_plant_fields["name"])
    ).scalar()

    # We return this bespoke error response if the plant already exists, so we can send them back the ID
    if existing_plant:
        res = Response(
            status=409,
            mimetype="application/json",
            response=json.dumps(
                {"error": "Plant already exists", "resource": existing_plant.plant_id}
            ),
        )
        abort(res)

    new_plant = Plant()
    new_plant.name = new_plant_fields["name"].lower()
    name_list = []
    for item in new_plant_fields["common_name"]:
        name_list.append(item.lower())

    new_plant.common_name = name_list
    new_plant.watering = new_plant_fields["watering"]
    new_plant.cycle = new_plant_fields["cycle"]

    db.session.add(new_plant)
    db.session.commit()

    return plant_schema.dump(new_plant)


@plant_blueprint.delete("/<int:plant_id>")
@jwt_required()
def delete_plant(plant_id):
    """If a user is an expert, deletes a plant in the database"""
    jwt_claims = get_jwt()

    if not jwt_claims.get("expert", False):
        abort(401)

    # This db call uses the primary key of plant_id to retrieve a Plant object
    existing_plant = db.session.get(Plant, plant_id)

    if not existing_plant:
        abort(404, description="plant_id does not exist")

    db.session.delete(existing_plant)
    db.session.commit()

    return plant_schema.dump(existing_plant), 204


@plant_blueprint.put("/<int:plant_id>")
@jwt_required()
def update_plant(plant_id):
    """If a user is an expert, updates a plant by ID

    Returns:
        JSON
    """
    jwt_claims = get_jwt()

    if not jwt_claims.get("expert", False):
        abort(401)

    try:
        # request.json.update({"plant_id": plant_id})
        fields_to_update = plant_schema.load(
            request.json, partial=("name", "common_name", "cycle", "watering")
        )
    except ValidationError as e:
        abort(400, description=e)

    # This db call uses the primary key of plant_id to retrieve a Plant object
    existing_plant = db.session.get(Plant, plant_id)

    if not existing_plant:
        abort(404, description="plant_id does not exist")

    if fields_to_update["name"]:
        # If they're wanting to update the name, this db call retrieves any other plant by that name
        # If it exists, we don't allow them to add a clash
        clashing_name = db.session.execute(
            db.select(Plant).filter_by(name=fields_to_update["name"])
        ).scalar()

    if clashing_name:
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
        if field == "plant_id":
            continue
        setattr(existing_plant, field, fields_to_update[field])

        # existing_plant
    db.session.commit()

    return plant_schema.dump(existing_plant), 200
