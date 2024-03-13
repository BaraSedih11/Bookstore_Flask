from flask import Blueprint, request, jsonify
from models import InventoryManager, Book
from . import db
from schemas import inventory_manager_schema



inventory_manager_bp = Blueprint('inventory_manager_bp', __name__, url_prefix='/inventory_managers')

@inventory_manager_bp.route('/', methods=['POST'])
def create_inventory_manager():
    data = request.json
    name = data.get('name')
    location = data.get('location')

    if not name:
        return jsonify({'message': 'Name is required'}), 400

    new_inventory_manager = InventoryManager(name=name, location=location)
    db.session.add(new_inventory_manager)
    db.session.commit()

    return inventory_manager_schema.jsonify(new_inventory_manager), 201

@inventory_manager_bp.route('/', methods=['GET'])
def list_inventory_managers():
    inventory_managers = InventoryManager.query.all()
    result = inventory_manager_schema.dump(inventory_managers)
    return jsonify(result)

@inventory_manager_bp.route('/<int:inventory_manager_id>', methods=['GET'])
def get_inventory_manager(inventory_manager_id):
    inventory_manager = InventoryManager.query.get_or_404(inventory_manager_id)
    return inventory_manager_schema.jsonify(inventory_manager)

@inventory_manager_bp.route('/<int:inventory_manager_id>/books', methods=['GET'])
def get_inventory_manager_books(inventory_manager_id):
    inventory_manager = InventoryManager.query.get_or_404(inventory_manager_id)
    books = inventory_manager.books
    return jsonify({'books': [book.serialize() for book in books]})

@inventory_manager_bp.route('/<int:inventory_manager_id>', methods=['PUT'])
def update_inventory_manager(inventory_manager_id):
    inventory_manager = InventoryManager.query.get_or_404(inventory_manager_id)
    data = request.json
    for key, value in data.items():
        setattr(inventory_manager, key, value)
    db.session.commit()
    return jsonify({'message': 'Inventory manager updated successfully'})

@inventory_manager_bp.route('/<int:inventory_manager_id>', methods=['DELETE'])
def delete_inventory_manager(inventory_manager_id):
    inventory_manager = InventoryManager.query.get_or_404(inventory_manager_id)
    db.session.delete(inventory_manager)
    db.session.commit()
    return jsonify({'message': 'Inventory manager deleted successfully'})
