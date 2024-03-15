from flask_marshmallow import Marshmallow
from ..models.book import Book


ma = Marshmallow()


class BookSchema(ma.Schema):
    class Meta:
        model = Book
        fields = ('id', 'title', 'author', 'price', 'quantity', 'category', 'manager_id')
