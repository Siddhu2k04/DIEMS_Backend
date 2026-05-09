from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Event, User, Registration
from extensions import db

organizer_bp = Blueprint('organizer', __name__)

@organizer_bp.route('/events', methods=['GET'])
@jwt_required()
def get_organizer_events():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if user.role not in ['organizer', 'admin']:
        return jsonify({"msg": "Unauthorized."}), 403

    events = Event.query.filter_by(organizer_id=current_user_id).all()
    result = []
    for event in events:
        result.append({
            "id": event.id,
            "title": event.title,
            "status": event.status,
            "date_time": event.date_time.isoformat(),
            "registration_count": Registration.query.filter_by(event_id=event.id).count()
        })
    return jsonify(result), 200

@organizer_bp.route('/events/<int:event_id>/registrations', methods=['GET'])
@jwt_required()
def get_event_registrations(event_id):
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    event = Event.query.get_or_404(event_id)

    if user.role != 'admin' and event.organizer_id != int(current_user_id):
        return jsonify({"msg": "Unauthorized."}), 403

    registrations = Registration.query.filter_by(event_id=event_id).all()
    result = []
    for reg in registrations:
        result.append({
            "id": reg.id,
            "user_name": reg.user.name,
            "user_email": reg.user.email,
            "status": reg.status,
            "attendance_status": reg.attendance_status,
            "registered_at": reg.registered_at.isoformat()
        })
    return jsonify(result), 200

@organizer_bp.route('/registrations/<int:reg_id>/status', methods=['PUT'])
@jwt_required()
def update_registration_status(reg_id):
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    registration = Registration.query.get_or_404(reg_id)
    event = registration.event

    if user.role != 'admin' and event.organizer_id != int(current_user_id):
        return jsonify({"msg": "Unauthorized."}), 403

    data = request.get_json()
    new_status = data.get('status')
    if new_status in ['pending', 'approved', 'rejected']:
        registration.status = new_status
        db.session.commit()
        return jsonify({"msg": f"Registration marked as {new_status}"}), 200
    
    return jsonify({"msg": "Invalid status"}), 400
