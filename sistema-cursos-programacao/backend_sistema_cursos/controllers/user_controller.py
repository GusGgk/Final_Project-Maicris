from flask import Blueprint, request, jsonify
from services.user_service import get_all_users, create_user

user_controller = Blueprint('user_controller', __name__)

@user_controller.route('/users', methods=['GET'])
def list_users():
    users = get_all_users()
    return jsonify(users)

@user_controller.route('/users', methods=['POST'])
def add_user():
    data = request.json
    result = create_user(data)
    return jsonify(result), 201
