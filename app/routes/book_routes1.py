# from flask import Blueprint, request, jsonify
# from models.book import Book
# from app import db, ma



# book_bp = Blueprint('book_bp', __name__, url_prefix='/books')


# @book_bp.route('/', methods=['GET'])
# def list_books():
#     books = Book.query.all()
#     return jsonify([book.to_dict() for book in books])

# @book_bp.route('/<int:book_id>', methods=['GET'])
# def get_book(book_id):
#     book = Book.query.get_or_404(book_id)
#     return jsonify(book.to_dict())

# @book_bp.route('/<int:book_id>', methods=['PUT'])
# def update_book(book_id):
#     book = Book.query.get_or_404(book_id)
#     data = request.json
#     for key, value in data.items():
#         setattr(book, key, value)
#     db.session.commit()
#     return jsonify({'message': 'Book updated successfully'})

# @book_bp.route('/<int:book_id>', methods=['DELETE'])
# def delete_book(book_id):
#     book = Book.query.get_or_404(book_id)
#     db.session.delete(book)
#     db.session.commit()
#     return jsonify({'message': 'Book deleted successfully'})
