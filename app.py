from flask import Flask, request, jsonify
import os
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from middleware import SimpleMiddleWare



app = Flask(__name__)
app.wsgi_app = SimpleMiddleWare(app.wsgi_app)
basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Initialize db
db = SQLAlchemy(app)
# Initialize ma
ma = Marshmallow(app)
