from flask import Blueprint, request, jsonify
from models.book import Book
from . import db



book_bp = Blueprint('book_bp', __name__, url_prefix='/books')

@book_bp.route('/', methods=['POST'])
def add_book():
    data = request.json
    title = data.get('title')
    author = data.get('author')
    price = data.get('price')
    quantity = data.get('quantity')
    category = data.get('category')
    manager_id = data.get('manager_id')  # Get m    anager_id from request data

    if not all([title, author, price, quantity, manager_id]):
        return jsonify({'message': 'Missing required fields'}), 400

    new_book = Book(title=title, author=author, price=price, quantity=quantity, category=category, manager_id=manager_id)
    db.session.add(new_book)
    db.session.commit()

    return jsonify({'message': 'Book added successfully'}), 201

@book_bp.route('/', methods=['GET'])
def list_books():
    books = Book.query.all()
    return jsonify([book.to_dict() for book in books])

@book_bp.route('/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = Book.query.get_or_404(book_id)
    return jsonify(book.to_dict())

@book_bp.route('/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    book = Book.query.get_or_404(book_id)
    data = request.json
    for key, value in data.items():
        setattr(book, key, value)
    db.session.commit()
    return jsonify({'message': 'Book updated successfully'})

@book_bp.route('/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    return jsonify({'message': 'Book deleted successfully'})
