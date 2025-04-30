from marshmallow import Schema, fields


class TodoSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str()
    description = fields.Str()
    status = fields.Str()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
    completed = fields.Bool()
