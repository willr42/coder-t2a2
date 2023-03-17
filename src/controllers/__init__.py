from .auth_controller import auth_blueprint
from .garden_controller import garden_blueprint
from .garden_plant_controller import garden_plant_blueprint
from .plant_controller import plant_blueprint

registerable_controllers = [
    auth_blueprint,
    plant_blueprint,
    garden_blueprint,
    garden_plant_blueprint,
]
