from marshmallow import Schema, fields

class InventoryManagerSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    location = fields.Str()
    books = fields.Nested('BookSchema', exclude=('manager',), many=True)

inventory_manager_schema = InventoryManagerSchema()
