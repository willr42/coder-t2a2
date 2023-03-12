from main import db
from sqlalchemy.dialects.postgresql import ARRAY

# Growth cycle
CYCLE = ("perennial", "annual", "biennial", "biannual")
# Watering amount required
WATERING = ("frequent", "average", "minimal", "none")


class Plant(db.Model):
    __tablename__ = "plants"

    plant_id = db.Column(db.Integer, nullable=False, primary_key=True)
    name = db.Column(db.String(), nullable=False, unique=True)
    common_name = db.Column(ARRAY(db.String()), nullable=False)
    cycle = db.Column(db.Enum(*CYCLE, name="cycle"), nullable=False)
    watering = db.Column(db.Enum(*WATERING, name="watering"), nullable=False)

    garden_plant = db.relationship("GardenPlant", back_populates="plant")
