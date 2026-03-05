from marshmallow import Schema, fields, validate

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=2, max=100))
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True, validate=validate.Length(min=6))
    role = fields.Str(dump_only=True)
    created_at = fields.DateTime(dump_only=True)

class UserUpdateSchema(Schema):
    name = fields.Str(validate=validate.Length(min=2, max=100))
    email = fields.Email()
    role = fields.Str(validate=validate.OneOf(["ADMIN", "ORGANIZADOR"]))