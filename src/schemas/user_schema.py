from main import ma
from models import User


class UserSchema(ma.Schema):
    class Meta:
        fields = ("user_id", "full_name", "email", "password")

    email = ma.Email()


user_schema = UserSchema()
