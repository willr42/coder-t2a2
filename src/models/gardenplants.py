from main import db


class GardenPlant(db.Model):
    __tablename__ = "garden_plants"

    garden_plant_id = db.Column(db.Integer, nullable=False, primary_key=True)

    last_watered = db.Column(db.Date, nullable=False)
    placement = db.Column(db.String(), nullable=False)
    healthiness = db.Column(db.Integer, nullable=False, default=5)

    garden_id = db.Column(
        db.Integer,
        db.ForeignKey("gardens.garden_id"),
    )
    garden = db.relationship(
        "Garden",
        back_populates="garden_plants",
    )

    plant_id = db.Column(
        db.Integer, db.ForeignKey("plants.plant_id", ondelete="CASCADE"), nullable=False
    )
    plant = db.relationship(
        "Plant",
        back_populates="garden_plant",
    )
