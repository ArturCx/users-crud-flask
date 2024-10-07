from flask import Blueprint, jsonify, make_response, request, abort
from app import db
from bson.objectid import ObjectId
from app.models import User, UserPreferences
from datetime import datetime

main = Blueprint('main', __name__)

# Criar novo usuário
@main.route('/users', methods=['POST'])
def create_user():
    data = request.json
    now = datetime.now()
    user = User(
        username=data['username'],
        password=data['password'],
        roles=data['roles'],
        preferences=UserPreferences(data['timezone']).__dict__,
        active=data.get('is_user_active', True),
        created_ts=now.timestamp(),
    )
    inserted_id = db.users.insert_one(user.__dict__).inserted_id
    return jsonify({'id': str(inserted_id)}), 201

# Pegar um usuário específico
@main.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    user = db.users.find_one({'_id': ObjectId(user_id)})
    if not user:
        abort(404, description="User not found")
    return jsonify(user_serializer(user))

# Pegar todos os usuários
@main.route('/users', methods=['GET'])
def get_users():
    users = list(db.users.find())
    return jsonify([user_serializer(user) for user in users])

# Atualizar um usuário
@main.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.json
    user = db.users.find_one({'_id': ObjectId(user_id)})
    if not user:
        abort(404, description="User not found")
    
    updated_data = {
        'username': data['username'],
        'password': data['password'],
        'roles': data['roles'],
        'preferences': {
            'timezone': data['timezone']
        },
        'active': data['active'],
        'updated_ts': datetime.now().timestamp()
    }
    
    db.users.update_one({'_id': ObjectId(user_id)}, {'$set': updated_data})
    return jsonify({'msg': 'User updated successfully'})

# Deletar usuário
@main.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = db.users.find_one({'_id': ObjectId(user_id)})
    if not user:
        abort(404, description="User not found")
    
    db.users.delete_one({'_id': ObjectId(user_id)})
    return jsonify({'msg': 'User deleted successfully'})

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
