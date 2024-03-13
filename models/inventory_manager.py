from flask_sqlalchemy import Model, Column, String, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class InventoryManager(Model):
    __tablename__ = 'inventory_manager'

    id = Column(Integer, primary_key=True)
    name = Column(String)   
    location = Column(String)
    # books = relationship('Book', back_populates='manager')

    def __init__(self, name, location):
        self.name = name
        self.location = location

