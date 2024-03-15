from datetime import datetime
from flask import Flask, jsonify, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from config import Config
import os
from marshmallow import Schema, fields
from werkzeug.security import generate_password_hash
# from flask_migrate import Migrate
from sqlalchemy.orm import sessionmaker
    

# configuration 
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)
# migrate = Migrate(app, db)
app.secret_key = '12345678'


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
    email = db.Column(db.String)
    password = db.Column(db.String)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id')) 
    books = db.relationship('Book', backref='inventory_manager')  # Define the relationship here

    def __init__(self, name, book_id, email, password):
        self.name = name
        self.book_id = book_id
        self.email = email
        self.password = password


    def __repr__(self):
        return f'<InventoryManager Book ID: {self.book_id}>'

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def __repr__(self):
        return f"<User {self.username}>"

payment_cart_books = db.Table('payment_cart_books',
    db.Column('payment_cart_id', db.Integer, db.ForeignKey('payment_cart.id'), primary_key=True),
    db.Column('book_id', db.Integer, db.ForeignKey('books.id'), primary_key=True),
    db.Column('quantity', db.Integer)  
)

class PaymentCart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'))
    _total_price = db.Column(db.Float, nullable=False)

    books = db.relationship('Book', secondary='payment_cart_books', backref='payment_carts')

    def __repr__(self):
        return f'<PaymentCart user_id: {self.user_id}, total_price: {self.total_price}>'
    
    def __init__(self, user_id, book_id, total_price=0):
        self.user_id = user_id
        self.book_id = book_id
        self._total_price = total_price

    @property
    def total_price(self):
        """
        Calculate the total price of the payment cart based on the books in it.
        """
        total_price = 0
        for item in self.books:
            total_price += item.price * item.quantity
        return total_price

    @total_price.setter
    def total_price(self, value):
        self._total_price = value

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    order_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self): 
        return f"<Order {self.id}>"

# schemas
class BookSchema(ma.Schema):
    class Meta:
        model = Book
        fields = ('id', 'title', 'author', 'price', 'quantity', 'category')

class InventoryManagerSchema(ma.Schema):
    class Meta:
        model = InventoryManager
        fields= ('id', 'name', 'email', 'password', 'book_id')

class UserSchema(Schema):
    model = User
    unknown = 'EXCLUDE'
    fields= ('id', 'username', 'email', 'password')
    
class PaymentCartSchema(Schema):
    model = PaymentCart
    fields = ("id", "user_id", "book_id", "total_price")

class OrderSchema(ma.Schema):
    model = Order
    fields = ('id', 'user_id', 'book_id', 'quantity', 'total_price', 'order_date')


# app.register_blueprint(book_blueprint)
# app.register_blueprint(inventory_blueprint)
# app.register_blueprint(users_blueprint)

book_schema = BookSchema()
books_schema = BookSchema(many=True)
user_schema = UserSchema()
users_schema = UserSchema(many=True)

inventory_schema = InventoryManagerSchema()
inventories_schema = InventoryManagerSchema(many=True)

shopping_cart = PaymentCartSchema()

with app.app_context():
    # db.drop_all()
    db.create_all()

    # manager1 = InventoryManager(name="inventory1", book_id=1, email="manager@gmail.com", password="123")
    # db.session.add(manager1)
    # db.session.commit()
    
    # book1 = Book(title="book1", author="bara", price=10.0, quantity=15, category="sceince")
    # db.session.add(book1)
    # db.session.commit()
    
    # user1 = User(username="user1", email="user1@example.com", password="123")
    # db.session.add(user1)
    # db.session.commit()

# routes

@app.route('/inventory', methods=['GET'])
def get_inventory_managers():
    if 'manager_id' not in session:
        return jsonify({'error': 'Unauthorized, You are not a manager'}), 401
    
    all_inventory_managers = InventoryManager.query.all()
    result = inventories_schema.dump(all_inventory_managers)
    return jsonify(result), 200


@app.route('/inventory/signup', methods=['POST'])
def manager_signup():
    name = request.json['name']
    book_id = request.json.get('book_id')  # Use .get() to get the value or None if not provided
    email = request.json['email']
    password = request.json.get('password')

    new_inventory_manager = InventoryManager(name=name, book_id=book_id, email=email, password=password)
    db.session.add(new_inventory_manager)
    db.session.commit()

    return inventory_schema.jsonify(new_inventory_manager)

@app.route('/inventory/<int:id>', methods=['PUT'])
def update_inventory_manager(id):
    if 'manager_id' not in session:
        return jsonify({'error': 'Unauthorized, You are not a manager'}), 401
    
    inventory_manager = InventoryManager.query.get(id)
    name = request.json['name']
    book_id = request.json.get('book_id')  # Use .get() to get the value or None if not provided

    inventory_manager.name = name
    inventory_manager.book_id = book_id

    db.session.commit()

    return inventory_schema.jsonify(inventory_manager)

# Route to delete an existing inventory manager
@app.route('/inventory', methods=['DELETE'])
def delete_inventory_manager():
    if 'manager_id' not in session:
        return jsonify({'error': 'Unauthorized, You are not a manager'}), 401
    
    id = int(session['manager_id'])
    inventory_manager = InventoryManager.query.get(id)
    db.session.delete(inventory_manager)
    db.session.commit()

    return {"message": "Inventory deleted successfully"}, 200

@app.route('/inventory/login', methods=['POST'])
def manager_login():
    # Get data from the request
    data = request.json
    email = data.get('email')
    password = data.get('password')

    # Find the user by username or email
    manager = InventoryManager.query.filter(InventoryManager.email == email).first()

    # Check if the user exists and the password is correct
    if manager.password == password:
        session['manager_id'] = manager.id
        return jsonify({'message': 'Login successful', 'manager_id': manager.id}), 200
    else:
        return jsonify({'error': 'Invalid username/email or password'}), 401

@app.route('/inventory/logout', methods=['POST'])
def manager_logout():
    if 'manager_id' not in session:
        return jsonify({'error': 'Unauthorized, You are not a manager'}), 401
    
    session.pop('manager_id', None)
    return jsonify({'message': 'Logout successful'}), 200


@app.route('/inventory/books', methods=['GET'])
def get_books():
    if 'user_id' not in session and 'manager_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    all_books = Book.query.all()
    result = books_schema.dump(all_books)
    return jsonify(result), 200

@app.route('/inventory/books', methods=['POST'])
def add_book():
    if 'manager_id' not in session:
        return jsonify({'error': 'Unauthorized, You are not a manager'}), 401
      
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
    if 'user_id' not in session and 'manager_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    book = Book.query.get_or_404(book_id)
    # Serialize the book object into a dictionary
    serialized_book = book_schema.dump(book)
    return jsonify(serialized_book)


@app.route('/inventory/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    if 'manager_id' not in session:
        return jsonify({'error': 'Unauthorized, You are not a manager'}), 401

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
    if 'manager_id' not in session:
        return jsonify({'error': 'Unauthorized, You are not a manager'}), 401

    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    return jsonify({'message': 'Book deleted successfully'})


# Users routes
@app.route('/users/signup', methods=['POST'])
def user_signup():
    # Get data from the request
    data = request.json

    # Check if username or email already exists
    existing_user = User.query.filter_by(username=data['username']).first()
    if existing_user:
        return jsonify({'error': 'Username already exists'}), 400

    existing_email = User.query.filter_by(email=data['email']).first()
    if existing_email:
        return jsonify({'error': 'Email already exists'}), 400

    # Hash the password
    # hashed_password = generate_password_hash(data['password'], method='sha256')

    # Create a new user instance
    new_user = User(username=data['username'], email=data['email'], password=data['password'])  

    # Add the user to the database
    db.session.add(new_user)
    db.session.commit()

    # Serialize the user data
    serialized_user = user_schema.dump(new_user)

    # Return a success response
    return jsonify({'message': 'User created successfully'}), 201

@app.route('/users/login', methods=['POST'])
def user_login():
    # Get data from the request
    data = request.json
    email = data.get('email')
    password = data.get('password')

    # Find the user by username or email
    user = User.query.filter(User.email == email).first()

    # Check if the user exists and the password is correct
    if user.password == password:
        session['user_id'] = user.id
        return jsonify({'message': 'Login successful', 'user_id': user.id}), 200
    else:
        return jsonify({'error': 'Invalid username/email or password'}), 401

@app.route('/users/logout', methods=['POST'])
def user_logout():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    session.pop('user_id', None)
    return jsonify({'message': 'Logout successful'}), 200


# payment cart routes
@app.route('/payment_carts', methods=['POST'])
def create_payment_cart():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = request.json

    book = Book.query.get_or_404(data['book_id'])
    # Serialize the book object into a dictionary
    serialized_book = book_schema.dump(book)    

    total_price = 0
    price = 0
    quantity = 0
    for key, val in serialized_book.items():
        if key == "price":
            price = val
        if key == "quantity":
            quantity = val
        
    total_price += price * quantity


    # Create the payment cart instance
    payment_cart = PaymentCart(user_id=data['user_id'], book_id=data['book_id'], total_price=total_price)

    # Save the payment cart to the database
    db.session.add(payment_cart)
    db.session.commit()

    return jsonify({'message': 'Payment cart created successfully', 'payment_cart_id': payment_cart.id}), 201

@app.route('/payment_carts/<int:payment_cart_id>/add_book', methods=['POST'])
def add_book_to_payment_cart(payment_cart_id):
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
   
    data = request.json
    book_id = data.get('book_id')
    quantity = data.get('quantity')

    if not book_id or not quantity:
        return jsonify({'error': 'Book ID and quantity are required'}), 400

    payment_cart = PaymentCart.query.get_or_404(payment_cart_id)    
    book = Book.query.get_or_404(book_id)

    # Check if the book is available
    if book.quantity < quantity:
        return jsonify({'error': 'Not enough stock for this book'}), 400

    # Add the book to the payment cart with the specified quantity
    payment_cart.books.append(book)
    db.session.commit()

    return jsonify({'message': 'Book added to payment cart successfully'}), 200


@app.route('/payment_carts/<int:payment_cart_id>/remove_book', methods=['POST'])
def remove_book_from_payment_cart(payment_cart_id):
    data = request.json
    book_id = data.get('book_id')

    if not book_id:
        return jsonify({'error': 'Book ID is required'}), 400

    payment_cart = PaymentCart.query.get_or_404(payment_cart_id)
    book = Book.query.get_or_404(book_id)

    # Check if the book is in the payment cart
    if book not in payment_cart.books:
        return jsonify({'error': 'Book not found in the payment cart'}), 400

    # Remove the book from the payment cart
    payment_cart.books.remove(book)
    db.session.commit()

    return jsonify({'message': 'Book removed from payment cart successfully'}), 200


# order routes
@app.route('/orders/place', methods=['POST'])
def place_order():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    # Get data from the request
    data = request.json
    user_id = session['user_id']
    book_id = data.get('book_id')
    quantity = data.get('quantity')

    if not book_id or not quantity:
        return jsonify({'error': 'Book ID and quantity are required'}), 400

    # Check if the book is available in inventory
    book = Book.query.get_or_404(book_id)
    if book.quantity < quantity:
        return jsonify({'error': 'Not enough stock for this book'}), 400

    # Calculate total price
    total_price = book.price * quantity

    # Create a new order
    new_order = Order(user_id=user_id, book_id=book_id, quantity=quantity, total_price=total_price)

    # Add the order to the database
    db.session.add(new_order)
    db.session.commit()

    # Update inventory
    book.quantity -= quantity
    db.session.commit()

    return jsonify({'message': 'Order placed successfully'}), 201

@app.route('/orders', methods=['GET'])
def view_orders():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    user_id = session['user_id']
    orders = Order.query.filter_by(user_id=user_id).all()

    order_list = []
    for order in orders:
        order_list.append({
            'id': order.id,
            'book_id': order.book_id,
            'quantity': order.quantity,
            'total_price': order.total_price,
            'order_date': order.order_date.strftime('%Y-%m-%d %H:%M:%S')
        })

    return jsonify(order_list), 200

# Generate Report Route
@app.route('/orders/report', methods=['GET'])
def generate_report():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    user_id = session['user_id']
    total_orders = Order.query.filter_by(user_id=user_id).count()
    total_sales = db.session.query(db.func.sum(Order.total_price)).filter_by(user_id=user_id).scalar()

    return jsonify({'total_orders': total_orders, 'total_sales': total_sales}), 200


if __name__ == '__main__':
    
    app.run(debug=True)

    
