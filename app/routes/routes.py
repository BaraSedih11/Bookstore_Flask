from flask import Blueprint, request, jsonify
from app import db, ma
from ..models.models import Book

routes = Blueprint('routes', __name__)

@routes.route('/')
def index():
    return "Hi it works!"


@routes.route('/', methods=['POST'])
def add_book():
    data = request.json
    title = data.get('title')
    author = data.get('author')
    price = data.get('price')
    quantity = data.get('quantity')
    category = data.get('category')
    manager_id = data.get('manager_id')  # Get manager_id from request data

    if not all([title, author, price, quantity, manager_id]):
        return jsonify({'message': 'Missing required fields'}), 400

    new_book = Book(title=title, author=author, price=price, quantity=quantity, category=category, manager_id=manager_id)
    db.session.add(new_book)
    db.session.commit()

    return jsonify({'message': 'Book added successfully'}), 201
