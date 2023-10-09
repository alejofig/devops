from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os 
app = Flask(__name__)
app.config['DEBUG'] = True

DB_USER=os.getenv("DB_USER","example")
DB_PASSWORD= os.getenv("DB_PASSWORD","example")
DB_HOST=os.getenv("DB_HOST","localhost")
DB_PORT=os.getenv("DB_PORT",5434)
DB_NAME=os.getenv("DB_NAME","example")

# DATABASE_URL = os.getenv("DATABASE_URL")
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL

db = SQLAlchemy(app)
ma = Marshmallow(app)

from .routes import cliente_bp
app.register_blueprint(cliente_bp, url_prefix='/blacklists')
with app.app_context():
    db.create_all()