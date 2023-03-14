from main import db
from sqlalchemy.dialects.postgresql import ARRAY
import enum

# https://stackoverflow.com/a/61689730


# Growth cycle
class Cycle(enum.Enum):
    perennial = "perennial"
    annual = "annual"
    biennial = "biennial"
    biannual = "biannual"


# Watering amount required
class Watering(enum.Enum):
    frequent = "frequent"
    average = "average"
    minimal = "minimal"
    none = "none"


class Plant(db.Model):
    __tablename__ = "plants"

    plant_id = db.Column(db.Integer, nullable=False, primary_key=True)
    name = db.Column(db.String(), nullable=False, unique=True)
    common_name = db.Column(ARRAY(db.String()), nullable=False)
    cycle = db.Column(db.Enum(Cycle), nullable=False)
    watering = db.Column(db.Enum(Watering), nullable=False)

    garden_plant = db.relationship("GardenPlant", back_populates="plant")
