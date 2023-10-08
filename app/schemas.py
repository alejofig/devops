from marshmallow import fields, Schema

class ClienteSchema(Schema):
    id = fields.Integer()
    app_uuid = fields.String()
    email = fields.String()
    blocked_reason = fields.String()
    datetime_request = fields.DateTime()
    ip_request = fields.String()