from flask import Blueprint, request, jsonify
from app.models.inventory_manager import InventoryManager
from app import db
from app.schemas.inventory_manager_schema import InventoryManagerSchema

inventory_blueprint = Blueprint('inventory', __name__)
inventory_schema = InventoryManagerSchema()
inventories_schema = InventoryManagerSchema(many=True)

# Route to get all inventory managers
@inventory_blueprint.route('/inventory', methods=['GET'])
def get_inventory_managers():
    all_inventory_managers = InventoryManager.query.all()
    result = inventories_schema.dump(all_inventory_managers)
    return jsonify(result)

# Route to add a new inventory manager
@inventory_blueprint.route('/inventory', methods=['POST'])
def add_inventory_manager():
    name = request.json['name']
    book_id = request.json['book_id']

    new_inventory_manager = InventoryManager(name=name, book_id=book_id)
    db.session.add(new_inventory_manager)
    db.session.commit()

    return inventory_schema.jsonify(new_inventory_manager)

# Route to update an existing inventory manager
@inventory_blueprint.route('/inventory/<int:id>', methods=['PUT'])
def update_inventory_manager(id):
    inventory_manager = InventoryManager.query.get(id)
    name = request.json['name']
    book_id = request.json['book_id']

    inventory_manager.name = name
    inventory_manager.book_id = book_id

    db.session.commit()

    return inventory_schema.jsonify(inventory_manager)

# Route to delete an existing inventory manager
@inventory_blueprint.route('/inventory/<int:id>', methods=['DELETE'])
def delete_inventory_manager(id):
    inventory_manager = InventoryManager.query.get(id)
    db.session.delete(inventory_manager)
    db.session.commit()

    return inventory_schema.jsonify(inventory_manager)
