from marshmallow import Schema, fields, validate

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=2, max=100))
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True, validate=validate.Length(min=6))
    role = fields.Method("get_role")
    created_at = fields.DateTime(dump_only=True)



    def get_role(self, obj):
        return obj.role.value if obj.role else None

class UserUpdateSchema(Schema):
    name = fields.Str(validate=validate.Length(min=2, max=100))
    email = fields.Email()
    role = fields.Str(validate=validate.OneOf(["ADMIN", "ORGANIZADOR"]))