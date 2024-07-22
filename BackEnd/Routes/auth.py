from flask import Blueprint, request, jsonify, session, redirect, url_for
from BackEnd.model import User
from BackEnd.extensions import db, login_manager, jwt, oauth
from flask_login import login_user, logout_user
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from BackEnd.utilities.thread_management import store_thread, generate_new_thread_id
from authlib.integrations.flask_client import OAuth
from BackEnd.config import Config
from google.oauth2 import id_token
from google.auth.transport import requests
import os
from BackEnd.utilities.send_mail import send_welcome_email  # Import the utility function
auth_bp = Blueprint('auth', __name__)

oauth = OAuth()


google = oauth.register(
    name='google',
    client_id=Config.GOOGLE_CLIENT_ID,
    client_secret=Config.GOOGLE_CLIENT_SECRET,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    refresh_token_url=None,
    redirect_uri=Config.GOOGLE_REDIRECT_URI,
    client_kwargs={'scope': 'openid profile email'},
)


@auth_bp.route('/signup', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password1 = data.get('password1')
    password2 = data.get('password2')

    first_name = data.get('first_name')
    user = User.query.filter_by(email=email).first()
    if user:
        return jsonify({'message': 'User already exists'}), 400
    elif password1 != password2:
        return jsonify({'message': 'Passwords do not match'}), 400
    elif len(password1) < 8:
        return jsonify({'message': 'Password must be at least 8 characters long'}), 400
    elif len(email) < 4:
        return jsonify({'message': 'Email must be at least 4 characters long'}), 400
    else:
    
        new_user = User(email=email, first_name=first_name)
        new_user.set_password(password1)
        db.session.add(new_user)
        db.session.commit()
        send_welcome_email(email, first_name)  # Send welcome email
    return jsonify({'message': 'User created successfully'}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    print(email)
    password = data.get('password')
    print(password)
    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return jsonify({'message': 'Invalid credentials'}), 401
    login_user(user)
    thread_id=generate_new_thread_id()
    store_thread(email, thread_id)
    access_token = create_access_token(identity={'password':user.password,'email': user.email})
    return jsonify({'success': True,'access_token': access_token}), 200
    
@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    logout_user()
    return jsonify({'message': 'User logged out'}), 200

@auth_bp.route('/google-login', methods=['POST'])
def google_login():
    token = request.json.get('token')
    try:
        idinfo = id_token.verify_oauth2_token(token, requests.Request(), os.getenv('GOOGLE_CLIENT_ID'))
        if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            raise ValueError('Wrong issuer.')
        
        email = idinfo['email']
        print(email)
        first_name = idinfo.get('given_name', '')
        print(first_name)
        user = User.query.filter_by(email=email).first()

        if not user:
            # Create a new user if not exists
            user = User(email=email, first_name=first_name)
            db.session.add(user)
            db.session.commit()
            send_welcome_email(email, first_name)  # Send welcome email on first login
    

        login_user(user)
        thread_id=generate_new_thread_id()
        print(f' this is from google log in threadID: {thread_id}')
        store_thread(email, thread_id)
        """user = User.query.filter_by(email=email).first()
        if not user:
            user = User(email=email, first_name=first_name)
            db.session.add(user)
            db.session.commit()"""

        access_token = create_access_token(identity={'email':user.email})
        print(f' this is from google log in access_token: {access_token}')
        return jsonify({'success': True, 'access_token': access_token}), 200
    except ValueError:
        return jsonify({'message': 'Invalid token'}), 401
    except Exception as e:
        return jsonify({'error': 'An error occurred', 'details': str(e)}), 500
    
@auth_bp.route('/admin-login', methods=['POST'])
def admin_login():
    ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD')
    data = request.get_json()
    password = data.get('password')
    if password == ADMIN_PASSWORD:
        users = User.query.all()
        user_info = [{"email": user.email, "first_name": user.first_name} for user in users]
        return jsonify({"success": True, "users": user_info}), 200
    else:
        return jsonify({"success": False, "message": "Invalid password"}), 401