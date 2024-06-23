from flask import Flask
from .extensions import db, login_manager, jwt, migrate
from .config import Config

DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)   

    from BackEnd.Routes.auth import auth_bp
    from BackEnd.Routes.vanai import vanai_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(vanai_bp)
    return app