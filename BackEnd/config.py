import os
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_secret_key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///users.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'your_jwt_secret_key'
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY') or 'your_openai_api_key'
    IMAGE_FOLDER='BackEnd/static/images'