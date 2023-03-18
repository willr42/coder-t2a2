from main import ma


class GardenPlantSchema(ma.Schema):
    class Meta:
        fields = (
            "garden_plant_id",
            "last_watered",
            "placement",
            "healthiness",
            "garden_id",
            "plant_id",
        )

    last_watered = ma.Date()
    plant_id = ma.Integer()


garden_plant_schema = GardenPlantSchema()
garden_plant_schema_no_id = GardenPlantSchema(exclude=("garden_plant_id",))
garden_plants_schema = GardenPlantSchema(many=True)
