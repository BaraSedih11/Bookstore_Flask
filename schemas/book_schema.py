from flask_marshmallow import Marshmallow
from models import Book


ma = Marshmallow()


class BookSchema(ma.Schema):
    class Meta:
        model = Book
        fields = ('id', 'title', 'author', 'price', 'quantity', 'category', 'manager_id')
