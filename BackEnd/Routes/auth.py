from flask import Blueprint, request, jsonify
from BackEnd.model import User
from BackEnd.extensions import db, login_manager, jwt
from flask_login import login_user, logout_user
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from BackEnd.utilities.thread_management import store_thread, generate_new_thread_id
auth_bp = Blueprint('auth', __name__)

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
