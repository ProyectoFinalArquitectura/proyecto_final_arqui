from marshmallow import Schema, fields, validate

class EventSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True, validate=validate.Length(min=3, max=200))
    description = fields.Str()
    date = fields.DateTime(required=True)
    location = fields.Str(required=True, validate=validate.Length(min=2, max=255))
    max_capacity = fields.Int(required=True, validate=validate.Range(min=1))
    status = fields.Method("get_status")
    organizer_id = fields.Int(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    
    def get_status(self, obj):
        return obj.status.value if obj.status else None

class EventUpdateSchema(Schema):
    title = fields.Str(validate=validate.Length(min=3, max=200))
    description = fields.Str()
    date = fields.DateTime()
    location = fields.Str(validate=validate.Length(min=2, max=255))
    max_capacity = fields.Int(validate=validate.Range(min=1))
    status = fields.Str(validate=validate.OneOf(["ACTIVO", "SOLD_OUT", "FINALIZADO", "CANCELADO"]))