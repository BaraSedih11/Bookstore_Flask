from flask import Flask
from app.routes.routes import routes
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from config import Config
from app.schemas.schemas import BookSchema
from app.models.book import Book
from app.models.inventory_manager import InventoryManager
from app.routes.book_routes import book_blueprint
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

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    author = db.Column(db.String)
    price = db.Column(db.Float)
    quantity = db.Column(db.Integer)
    category = db.Column(db.String)
    manager_id = db.Column(db.Integer, db.ForeignKey('inventory_manager.id'))
    manager = db.relationship('InventoryManager', back_populates='books')

    def __init__(self, id, title, author, price, quantity, category, manager_id):
        self.id = id
        self.title = title
        self.author = author
        self.price = price
        self.quantity = quantity
        self.category = category
        self.manager_id = manager_id

    def __repr__(self):
        return f"<Book(title='{self.title}', author='{self.author}', price={self.price}, quantity={self.quantity}, category='{self.category}', manager_id='{self.manager_id}')>"


class InventoryManager(db.Model):
    __tablename__ = 'inventory_manager'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)   
    book_id = db.Column(db.Integer, db.ForeignKey('books.id')) 
    book = db.relationship('Book', backref=db.backref('inventory', lazy=True))

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
        id = fields.Int(dump_only=True)
        name = fields.Str(required=True)
        book_id = fields.Int(required=False)


app.register_blueprint(book_blueprint)


book_schema = BookSchema()
books_schema = BookSchema(many=True)

invetory_schema = InventoryManagerSchema()
invetories_schema = InventoryManagerSchema(many=True)


# with app.app_context():
#     db.create_all()


if __name__ == '__main__':
    app.run(debug=True)
