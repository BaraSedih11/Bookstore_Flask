from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .routes import inventory_manager_routes

app = Flask(__name__)

# Configure database connection (replace 'your_database.db' with desired filename)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bookstore.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)



# Register routes blueprint
app.register_blueprint(inventory_manager_routes)

if __name__ == '__main__':
    db.create_all()  # Create database tables if they don't exist
    app.run(debug=True)