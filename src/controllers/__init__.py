from .auth_controller import auth_blueprint
from .plant_controller import plant_blueprint

registerable_controllers = [auth_blueprint, plant_blueprint]
