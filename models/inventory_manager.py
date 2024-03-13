from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class InventoryManager(Base):
    __tablename__ = 'inventory_manager'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    location = Column(String)
    books = relationship('Book', back_populates='manager')
