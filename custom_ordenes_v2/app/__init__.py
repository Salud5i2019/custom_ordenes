from flask import Flask
from flask_jwt_extended import JWTManager
from app.routes.vision import vision_bp
from app.routes.auth import auth_bp  # <-- nuevo blueprint
from app.models.log import db
from dotenv import load_dotenv
import os

load_dotenv()  # Carga variables del .env

jwt = JWTManager()  # Instancia global

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///logs.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY")

    db.init_app(app)
    jwt.init_app(app)

    app.register_blueprint(vision_bp)
    app.register_blueprint(auth_bp)

    with app.app_context():
        db.create_all()

    return app
