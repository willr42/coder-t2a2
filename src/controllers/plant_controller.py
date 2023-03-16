import json

from flask import Blueprint, Response, abort, jsonify, request
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
def add_plant():
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
    for field in new_plant_fields:
        setattr(new_plant, field, new_plant_fields[field])

    db.session.add(new_plant)
    db.session.commit()

    return plant_schema.dump(new_plant)
