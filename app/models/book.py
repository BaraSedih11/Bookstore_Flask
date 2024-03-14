from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from app import db, ma


Base = declarative_base()

class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    author = Column(String)
    price = Column(Float)
    quantity = Column(Integer)
    category = Column(String)
    manager_id = Column(Integer, ForeignKey('inventory_manager.id'))
    manager = relationship('InventoryManager', back_populates='books')


    def __repr__(self):
        return f"<Book(title='{self.title}', author='{self.author}', price={self.price}, quantity={self.quantity}, category='{self.category}', manager_id='{self.manager_id}')>"
