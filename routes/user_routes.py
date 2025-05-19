from flask import Blueprint, request, jsonify
from db import users_collection

user_routes = Blueprint('users', __name__)

@user_routes.route('/users', methods=['POST'])
def create_user():
    data = request.json
    user_id = users_collection.insert_one(data).inserted_id
    return jsonify({'message': 'User created', 'user_id': str(user_id)}), 201

@user_routes.route('/users', methods=['GET'])
def get_users():
    users = list(users_collection.find({}, {'_id': 0}))  # Exclude MongoDB's _id field
    return jsonify(users), 200

@user_routes.route('/users/<string:email>', methods=['PUT'])
def update_user(email):
    data = request.json
    result = users_collection.update_one({'email': email}, {'$set': data})
    if result.matched_count == 0:
        return jsonify({'message': 'User not found'}), 404
    return jsonify({'message': 'User updated'}), 200

@user_routes.route('/users/<string:email>', methods=['DELETE'])
def delete_user(email):
    result = users_collection.delete_one({'email': email})
    if result.deleted_count == 0:
        return jsonify({'message': 'User not found'}), 404
    return jsonify({'message': 'User deleted'}), 200