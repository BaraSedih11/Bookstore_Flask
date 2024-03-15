from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from app import db, ma



class InventoryManager(db.Model):
    __tablename__ = 'inventory_manager'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)   
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    book = db.relationship('Book', backref=db.backref('inventory', lazy=True))

    def __repr__(self):
        return f'<InventoryManager Book ID: {self.book_id}, Quantity: {self.quantity}>'

