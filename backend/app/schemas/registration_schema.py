from marshmallow import Schema, fields

class RegistrationSchema(Schema):
    id = fields.Int(dump_only=True)
    event_id = fields.Int(required=True)
    attendee_id = fields.Int(dump_only=True)
    registration_date = fields.DateTime(dump_only=True)
    status = fields.Str(dump_only=True)