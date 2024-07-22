from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_caching import Cache
from authlib.integrations.flask_client import OAuth
from flask_mail import Mail
db = SQLAlchemy()
login_manager = LoginManager()
jwt = JWTManager()
migrate = Migrate()
cache=Cache()
oauth = OAuth()
mail=Mail()