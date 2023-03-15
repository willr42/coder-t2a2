from main import ma


class GardenSchema(ma.Schema):
    class Meta:
        fields = ("garden_id", "creation_date", "garden_type", "user_id")

    creation_date = ma.Date()


garden_schema = GardenSchema()
gardens_schema = GardenSchema(many=True)
