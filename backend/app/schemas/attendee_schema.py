from marshmallow import Schema, fields, validate

class AttendeeSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=2, max=100))
    email = fields.Email(required=True)
    phone = fields.Str(validate=validate.Length(max=20))
    created_at = fields.DateTime(dump_only=True)