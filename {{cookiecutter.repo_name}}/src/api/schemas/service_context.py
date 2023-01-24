from marshmallow import Schema, fields


class ServiceContextSchema(Schema):
    maintenance = fields.Boolean()
