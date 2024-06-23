from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity


vanai_bp = Blueprint('vanai', __name__)

@vanai_bp.route('/vanai', methods=['GET', 'POST'])
@jwt_required()
def vanai():
    auth_header = request.headers.get('Authorization')
    print(f"Authorization Header: {auth_header}") # Add this line to check the Authorization header
    user_identity = get_jwt_identity()
    return jsonify({'message': 'Vanai', 'user': user_identity}), 200