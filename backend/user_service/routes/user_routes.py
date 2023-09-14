from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from ..models import User
from ..database import db
from ..utils import hash_password

users = Blueprint('users', __name__)


@users.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    # check if username or email already exists
    exisiting_username = User.query.filter_by(
        username=data['username']).first()
    if exisiting_username:
        return jsonify({'message': 'Username already exists'}), 400
    exisiting_email = User.query.filter_by(email=data['email']).first()
    if exisiting_email:
        return jsonify({'message': 'Email already exists'}), 400

    hashed = hash_password(data['password'])
    new_user = User(
        username=data['username'],
        full_name=data['full_name'],
        email=data['email'],
        hashed_password=hashed
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User created successfully'}), 201


@users.route('/', methods=['GET'])
def get_all_users():
    users = User.query.all()
    return jsonify([user.serialize() for user in users]), 200


@users.route('/<string:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404

    user_data = user.serialize()
    return jsonify(user_data), 200


@users.route('/<string:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404

    data = request.get_json()
    if 'username' in data:
        user.username = data['username']
    if 'full_name' in data:
        user.full_name = data['full_name']
    if 'email' in data:
        user.email = data['email']

    db.session.commit()

    return jsonify({'message': 'User updated successfully'}), 200


@users.route('/<string:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404

    db.session.delete(user)
    db.session.commit()

    return jsonify({'message': 'User deleted successfully'}), 200
