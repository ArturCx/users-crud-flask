from flask import Blueprint, jsonify, request, abort
from app import db
from bson.objectid import ObjectId
from app.models import User, UserPreferences
from datetime import datetime

main = Blueprint('main', __name__)

# Helper function to parse roles
def parse_roles(data):
    roles = []
    if data.get('is_user_admin'):
        roles.append('admin')
    if data.get('is_user_manager'):
        roles.append('manager')
    if data.get('is_user_tester'):
        roles.append('tester')
    return roles

# Route to get all users
@main.route('/users', methods=['GET'])
def get_users():
    users = list(db.users.find())
    return jsonify([user_serializer(user) for user in users])

# Route to create a new user
@main.route('/users', methods=['POST'])
def create_user():
    data = request.json
    user = User(
        username=data['user'],
        password=data['password'],
        roles=parse_roles(data),
        preferences=UserPreferences(data['user_timezone']),
        active=data.get('is_user_active', True),
        created_ts=datetime.strptime(data['created_at'], '%Y-%m-%dT%H:%M:%SZ').timestamp()
    )
    inserted_id = db.users.insert_one(user.__dict__).inserted_id
    return jsonify({'id': str(inserted_id)}), 201

# Route to update a user
@main.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.json
    user = db.users.find_one({'_id': ObjectId(user_id)})
    if not user:
        abort(404, description="User not found")
    
    updated_data = {
        'username': data.get('user', user['username']),
        'password': data.get('password', user['password']),
        'roles': parse_roles(data),
        'preferences': {
            'timezone': data['user_timezone']
        },
        'active': data.get('is_user_active', user['active']),
        'updated_ts': datetime.now().timestamp()
    }
    
    db.users.update_one({'_id': ObjectId(user_id)}, {'$set': updated_data})
    return jsonify({'msg': 'User updated successfully'})

# Route to delete a user
@main.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = db.users.find_one({'_id': ObjectId(user_id)})
    if not user:
        abort(404, description="User not found")
    
    db.users.delete_one({'_id': ObjectId(user_id)})
    return jsonify({'msg': 'User deleted successfully'})

# Helper function to serialize user
def user_serializer(user):
    return {
        'id': str(user['_id']),
        'username': user['username'],
        'roles': user['roles'],
        'timezone': user['preferences']['timezone'],
        'active': user['active'],
        'created_ts': user['created_ts'],
        'updated_ts': user.get('updated_ts', user['created_ts'])
    }
