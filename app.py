from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from config import Config
import os
from marshmallow import Schema, fields


app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)


# Models
class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    author = db.Column(db.String)
    price = db.Column(db.Float)
    quantity = db.Column(db.Integer)
    category = db.Column(db.String)
    # manager_id = db.Column(db.Integer, db.ForeignKey('inventory_manager.id'))
    # manager = db.relationship('InventoryManager', back_populates='books')

    def __init__(self, title, author, price, quantity, category):
        self.title = title
        self.author = author
        self.price = price
        self.quantity = quantity
        self.category = category
        # self.manager_id = manager_id

    def __repr__(self):
        return f"<Book(title='{self.title}', author='{self.author}', price={self.price}, quantity={self.quantity}, category='{self.category}')>"

class InventoryManager(db.Model):
    __tablename__ = 'inventory_manager'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)   
    book_id = db.Column(db.Integer, db.ForeignKey('books.id')) 
    books = db.relationship('Book', backref='inventory_manager')  # Define the relationship here

    def __init__(self, name, book_id):
        self.name = name
        self.book_id = book_id


    def __repr__(self):
        return f'<InventoryManager Book ID: {self.book_id}>'


# schemas
class BookSchema(ma.Schema):
    class Meta:
        model = Book
        fields = ('id', 'title', 'author', 'price', 'quantity', 'category', 'manager_id')

class InventoryManagerSchema(ma.Schema):
    class Meta:
        model = InventoryManager
        fields= ('id', 'name', 'book_id')


# app.register_blueprint(book_blueprint)
# app.register_blueprint(inventory_blueprint)


book_schema = BookSchema()
books_schema = BookSchema(many=True)

inventory_schema = InventoryManagerSchema()
inventories_schema = InventoryManagerSchema(many=True)


# with app.app_context():
    # db.drop_all()
    # db.create_all()
#     manager1 = InventoryManager(name="inventory1", book_id=1)
#     db.session.add(manager1)
#     db.session.commit()
    
#     book1 = Book(title="book1", author="bara", price=10.0, quantity=15, category="sceince", manager_id=1)
#     db.session.add(book1)
#     db.session.commit()
    
    # Create an instance of your Book model without specifying the 'id' argument
    # book = Book(title='Example Book', author='John Doe', price=29.99, quantity=10, category='Fiction')
    # manager = InventoryManager(name='Manager Name', book_id=1)

    # Add instances to the session
    # db.session.add(book)
    # db.session.add(manager)

    # Commit the changes
    # db.session.commit()

    # book_schema = book
    # books_schema.add()
    # inventories_schema

# routes

@app.route('/inventory', methods=['GET'])
def get_inventory_managers():
    all_inventory_managers = InventoryManager.query.all()
    result = inventories_schema.dump(all_inventory_managers)
    return jsonify(result), 200


@app.route('/inventory', methods=['POST'])
def add_inventory_manager():
    name = request.json['name']
    book_id = request.json.get('book_id')  # Use .get() to get the value or None if not provided

    new_inventory_manager = InventoryManager(name=name, book_id=book_id)
    db.session.add(new_inventory_manager)
    db.session.commit()

    return inventory_schema.jsonify(new_inventory_manager)

@app.route('/inventory/<int:id>', methods=['PUT'])
def update_inventory_manager(id):
    inventory_manager = InventoryManager.query.get(id)
    name = request.json['name']
    book_id = request.json.get('book_id')  # Use .get() to get the value or None if not provided

    inventory_manager.name = name
    inventory_manager.book_id = book_id

    db.session.commit()

    return inventory_schema.jsonify(inventory_manager)

# Route to delete an existing inventory manager
@app.route('/inventory/<int:id>', methods=['DELETE'])
def delete_inventory_manager(id):
    inventory_manager = InventoryManager.query.get(id)
    db.session.delete(inventory_manager)
    db.session.commit()

    return {"message": "Inventory deleted successfully"}, 200

@app.route('/inventory/books', methods=['GET'])
def get_books():
    all_books = Book.query.all()
    result = books_schema.dump(all_books)
    return jsonify(result), 200

@app.route('/inventory/books', methods=['POST'])
def add_book():
    data = request.json
    title = data.get('title')
    author = data.get('author')
    price = data.get('price')
    quantity = data.get('quantity')
    category = data.get('category')

    if not all([title, author, price, quantity]):
        return jsonify({'message': 'Missing required fields'}), 400

    new_book = Book(title=title, author=author, price=price, quantity=quantity, category=category)
    db.session.add(new_book)
    db.session.commit()

    return jsonify({'message': 'Book added successfully'}), 201

@app.route('/inventory/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = Book.query.get_or_404(book_id)
    # Serialize the book object into a dictionary
    serialized_book = book_schema.dump(book)
    return jsonify(serialized_book)


@app.route('/inventory/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    book = Book.query.get_or_404(book_id)
    data = request.json
    # Ensure that only valid fields are updated
    allowed_fields = ['title', 'author', 'price', 'quantity', 'category', 'manager_id']
    for key, value in data.items():
        if key in allowed_fields:
            setattr(book, key, value)
    db.session.commit()
    return jsonify({'message': 'Book updated successfully'})

@app.route('/inventory/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    return jsonify({'message': 'Book deleted successfully'})


if __name__ == '__main__':
    app.run(debug=True)

    
