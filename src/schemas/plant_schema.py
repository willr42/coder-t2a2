from main import ma
from models import Plant
from models.plants import Cycle, Watering


class PlantSchema(ma.Schema):
    class Meta:
        fields = ("plant_id", "name", "common_name", "cycle", "watering")

    cycle = ma.Enum(Cycle)
    watering = ma.Enum(Watering)


plant_schema = PlantSchema()
plants_schema = PlantSchema(many=True)
