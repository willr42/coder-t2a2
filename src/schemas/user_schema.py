from main import ma


class UserSchema(ma.Schema):
    class Meta:
        fields = ("user_id", "full_name", "email", "password")

    email = ma.Email()
    password = ma.String(load_only=True)


user_schema = UserSchema()
