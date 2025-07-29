from flask import Flask
from .models import db
from .routes import main
from .admin_routes import admin
import os

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.secret_key = 'gizli-anahtar'

    os.makedirs("app/static/uploads", exist_ok=True)

    db.init_app(app)
    app.register_blueprint(main)
    app.register_blueprint(admin)

    return app
