from marshmallow import validate

from main import ma


class UserSchema(ma.Schema):
    class Meta:
        fields = ("user_id", "full_name", "email", "password")

    email = ma.Email()
    full_name = ma.String(validate=validate.Length(min=1))
    password = ma.String(
        required=True,
        load_only=True,
        validate=validate.Length(
            min=6, error="Your password must be longer than 6 characters."
        ),
    )


user_schema = UserSchema()
