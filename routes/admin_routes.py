from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import User, Event, Registration
from extensions import db

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/users', methods=['GET'])
@jwt_required()
def get_all_users():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if user.role != 'admin':
        return jsonify({"msg": "Unauthorized. Admin access required."}), 403

    users = User.query.all()
    result = []
    for u in users:
        result.append({
            "id": u.id,
            "name": u.name,
            "email": u.email,
            "role": u.role,
            "department": u.department,
            "created_at": u.created_at.isoformat()
        })
    return jsonify(result), 200

@admin_bp.route('/users/<int:user_id>/role', methods=['PUT'])
@jwt_required()
def update_user_role(user_id):
    current_user_id = get_jwt_identity()
    admin_user = User.query.get(current_user_id)
    
    if admin_user.role != 'admin':
        return jsonify({"msg": "Unauthorized. Admin access required."}), 403

    user_to_update = User.query.get_or_404(user_id)
    data = request.get_json()
    new_role = data.get('role')
    
    if new_role in ['student', 'organizer', 'admin']:
        user_to_update.role = new_role
        db.session.commit()
        return jsonify({"msg": f"User role updated to {new_role}"}), 200
        
    return jsonify({"msg": "Invalid role"}), 400

@admin_bp.route('/stats', methods=['GET'])
@jwt_required()
def get_system_stats():
    current_user_id = get_jwt_identity()
    admin_user = User.query.get(current_user_id)
    
    if admin_user.role != 'admin':
        return jsonify({"msg": "Unauthorized. Admin access required."}), 403

    total_users = User.query.count()
    total_events = Event.query.count()
    total_registrations = Registration.query.count()
    
    return jsonify({
        "total_users": total_users,
        "total_events": total_events,
        "total_registrations": total_registrations
    }), 200
