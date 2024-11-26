from flask import Blueprint, request, jsonify
from models import db, User
from flask_bcrypt import generate_password_hash, check_password_hash

bp = Blueprint('admin', __name__)

# List all users
@bp.route('/users', methods=['GET'])
def list_users():
    users = User.query.all()
    return jsonify([
        {"id": user.id, "name": user.name, "email": user.email, "role": user.role}
        for user in users
    ]), 200

# Add a new user
@bp.route('/users', methods=['POST'])
def add_user():
    data = request.json

    # Check if user with the same email already exists
    if User.query.filter_by(email=data['email']).first():
        return jsonify({"error": "User with this email already exists"}), 400

    # Hash password before saving it
    hashed_password = generate_password_hash(data['password']).decode('utf-8')
    
    new_user = User(
        name=data['name'],
        email=data['email'],
        password=hashed_password,
        role=data['role']
    )
    
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User added successfully"}), 201

# Delete a user by ID
@bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted successfully"}), 200

# Update user details (username, email, password, role)
@bp.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    data = request.json
    
    # Update user details
    if 'name' in data:
        user.name = data['name']
    if 'email' in data:
        # Check if email already exists
        if User.query.filter_by(email=data['email']).first() and data['email'] != user.email:
            return jsonify({"error": "User with this email already exists"}), 400
        user.email = data['email']
    if 'role' in data:
        user.role = data['role']
    if 'password' in data:
        user.password = generate_password_hash(data['password']).decode('utf-8')
    
    db.session.commit()
    return jsonify({"message": "User updated successfully"}), 200
