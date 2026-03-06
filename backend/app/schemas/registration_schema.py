from marshmallow import Schema, fields

class RegistrationSchema(Schema):
    id = fields.Int(dump_only=True)
    event_id = fields.Int(dump_only=True)
    attendee_id = fields.Int(dump_only=True)
    registration_date = fields.DateTime(dump_only=True)
    status = fields.Method("get_status")

    def get_status(self, obj):
        return obj.status.value if obj.status else None