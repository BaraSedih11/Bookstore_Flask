from marshmallow import Schema, fields
from models.inventory_manager import  InventoryManager

class InventoryManagerSchema(Schema):
    class Meta:
        model = InventoryManager
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    location = fields.Str()
    # books = fields.Nested('BookSchema', exclude=('manager',), many=True)

inventory_manager_schema = InventoryManagerSchema()
    