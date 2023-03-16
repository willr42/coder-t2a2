import json

from flask import Blueprint, Response, abort, jsonify, request
from flask_jwt_extended import get_jwt, jwt_required
from marshmallow import ValidationError

from main import db
from models import Plant
from schemas import plant_schema, plants_schema

plant_blueprint = Blueprint("plants", __name__, url_prefix="/plants")


@plant_blueprint.get("/")
def get_plants():
    plant_list = db.session.execute(db.select(Plant)).scalars().all()

    return plants_schema.dump(plant_list)


@plant_blueprint.post("/")
@jwt_required()
def add_plant():
    jwt_claims = get_jwt()

    if not jwt_claims.get("expert", False):
        abort(401)

    try:
        new_plant_fields = plant_schema.load(request.json)
    except ValidationError as e:
        abort(400, description=e)

    existing_plant = db.session.execute(
        db.select(Plant).filter_by(name=new_plant_fields["name"])
    ).scalar()

    # TODO: can we make this into a handler rather than in-line here?
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
    jwt_claims = get_jwt()

    if not jwt_claims.get("expert", False):
        abort(401)

    existing_plant = db.session.get(Plant, plant_id)

    if not existing_plant:
        abort(404, description="plant_id does not exist")

    db.session.delete(existing_plant)
    db.session.commit()

    return plant_schema.dump(existing_plant), 204


@plant_blueprint.put("/<int:plant_id>")
@jwt_required()
def update_plant(plant_id):
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
