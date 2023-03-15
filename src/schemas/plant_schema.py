from main import ma
from models.plants import Cycle, Watering


class PlantSchema(ma.Schema):
    class Meta:
        fields = ("plant_id", "name", "common_name", "cycle", "watering")

    plant_id = ma.Integer(required=False)
    name = ma.String(required=True)
    common_name = ma.List(ma.String(), required=False)
    cycle = ma.Enum(Cycle, required=True)
    watering = ma.Enum(Watering, required=True)


plant_schema = PlantSchema()
plants_schema = PlantSchema(many=True)
