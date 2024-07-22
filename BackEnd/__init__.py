from flask import Flask
from .extensions import db, login_manager, jwt, migrate,cache,oauth,mail
from .config import Config
from .model import User
from flask_session import Session

DB_NAME = "database.db"

def create_app():
    app = Flask(__name__,static_url_path='/static/images')
    app.config.from_object(Config)
   
    db.init_app(app)
    login_manager.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    oauth.init_app(app) 
    mail.init_app(app)   
    Session(app)
   
    
    from BackEnd.Routes.auth import auth_bp
    from BackEnd.Routes.vanai import vanai_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(vanai_bp)
    return app


# User loader callback for JWT
@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.filter_by(email=identity["email"]).one_or_none()