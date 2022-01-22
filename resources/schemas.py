from marshmallow import Schema, fields


class DiscountCodeSchema(Schema):
    id = fields.Integer()
    brand_id = fields.Integer()
    count = fields.Integer(load_only=True)


class DiscountCodeUserSchema(Schema):
    id = fields.Integer(dump_only=True)
    brand_id = fields.Integer()
    code = fields.String(dump_only=True)
    usable = fields.Boolean(dump_only=True)
