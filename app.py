from flask import Flask
from app.routes.routes import routes
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from config import Config
from app.schemas.schemas import BookSchema

# Initialize the Flask application
app = Flask(__name__)

# Register the blueprint
app.register_blueprint(routes)

# Load the configuration from the Config class
app.config.from_object(Config)

# Initialize the database object
db = SQLAlchemy(app)

# Initialize the Marshmallow object
ma = Marshmallow(app)

# Create the book schema instance
book_schema = BookSchema()

if __name__ == '__main__':
    with app.app_context():
        # Create the database tables
        db.create_all()

    # Run the Flask application
    app.run(debug=True)
