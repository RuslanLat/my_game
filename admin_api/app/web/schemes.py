# admin_api/app/web/schemes.py

from marshmallow import Schema, fields


class OkResponseSchema(Schema):
    status = fields.Str()
    data = fields.Dict()