from main import ma


class GardenPlantSchema(ma.Schema):
    class Meta:
        fields = (
            "garden_plant_id",
            "last_watered",
            "placement",
            "healthiness",
            "garden_id",
            "plant",
        )

    last_watered = ma.Date()
    plant = ma.Nested("PlantSchema", only=("plant_id", "name"))


garden_plant_schema = GardenPlantSchema()
garden_plants_schema = GardenPlantSchema(many=True)
