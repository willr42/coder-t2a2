from main import ma
from models import User


class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User

    user_id = ma.auto_field()
    full_name = ma.auto_field()
    email = ma.auto_field(required=True)
    # NOTE: May need to remove these requireds later
    password = ma.auto_field(required=True)


user_schema = UserSchema()
