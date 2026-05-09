from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models import User
from extensions import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    if not data or not data.get('email') or not data.get('password') or not data.get('name'):
        return jsonify({"msg": "Missing required fields"}), 400
        
    if User.query.filter_by(email=data['email']).first():
        return jsonify({"msg": "Email already exists"}), 400
        
    password_hash = generate_password_hash(data['password'])
    
    new_user = User(
        name=data['name'],
        email=data['email'],
        password_hash=password_hash,
        role=data.get('role', 'student')
    )
    
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({"msg": "User created successfully"}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({"msg": "Missing required fields"}), 400
        
    user = User.query.filter_by(email=data['email']).first()
    
    if not user or not check_password_hash(user.password_hash, data['password']):
        return jsonify({"msg": "Invalid credentials"}), 401
        
    access_token = create_access_token(identity=str(user.id))
    
    return jsonify({
        "access_token": access_token,
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role
        }
    }), 200

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({"msg": "User not found"}), 404
        
    return jsonify({
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "role": user.role,
        "department": user.department,
        "profile_picture": user.profile_picture,
        "points": getattr(user, 'points', 0),
        "badges": getattr(user, 'badges', [])
    }), 200

@auth_bp.route('/me', methods=['PUT'])
@jwt_required()
def update_profile():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({"msg": "User not found"}), 404
        
    data = request.get_json()
    if 'name' in data:
        user.name = data['name']
    if 'department' in data:
        user.department = data['department']
    if 'profile_picture' in data:
        user.profile_picture = data['profile_picture']
        
    db.session.commit()
    return jsonify({"msg": "Profile updated successfully"}), 200

@auth_bp.route('/me/registrations', methods=['GET'])
@jwt_required()
def get_my_registrations():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({"msg": "User not found"}), 404
        
    registrations = user.registrations
    result = []
    for reg in registrations:
        result.append({
            "id": reg.id,
            "status": reg.status,
            "qr_code": reg.qr_code,
            "registered_at": reg.registered_at.isoformat(),
            "student": {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "department": user.department
            },
            "event": {
                "id": reg.event.id,
                "title": reg.event.title,
                "date_time": reg.event.date_time.isoformat(),
                "venue": reg.event.venue,
                "banner_image": reg.event.banner_image,
                "status": reg.event.status,
                "category": reg.event.category,
                "organizer_name": reg.event.organizer.name
            }
        })
        
    return jsonify(result), 200
