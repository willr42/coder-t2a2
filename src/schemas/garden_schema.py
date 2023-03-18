from marshmallow import validate

from main import ma


class GardenSchema(ma.Schema):
    class Meta:
        fields = (
            "garden_id",
            "creation_date",
            "garden_type",
            "user_id",
            "garden_plants",
        )

    creation_date = ma.Date(dump_only=True)
    garden_type = ma.String(required=True, validate=validate.Length(min=1))
    garden_plants = ma.List(ma.Nested("GardenPlantSchema", only=("garden_plant_id",)))


garden_schema = GardenSchema()
gardens_schema = GardenSchema(many=True)
