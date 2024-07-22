import os
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file
from datetime import timedelta
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_secret_key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///users.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'your_jwt_secret_key'
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY') or 'your_openai_api_key'
    IMAGE_FOLDER='BackEnd/static/images'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    SESSION_TYPE='filesystem'
    SESSION_PERMANENT = False
    SESSION_USE_SIGNER = True
    SESSION_KEY_PREFIX = 'session:'
    GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID')
    GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET')
    GOOGLE_REDIRECT_URI = os.environ.get('GOOGLE_REDIRECT_URI') or 'http://localhost:5000/auth/google/callback'

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')  # Your email address
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')  # Your email password or app password
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_USERNAME')
