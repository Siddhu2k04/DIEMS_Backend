from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from models import Event, User, Registration
from extensions import db
from utils.qr_generator import generate_qr_code

event_bp = Blueprint('event', __name__)

def build_ticket_qr_data(registration):
    user = registration.user
    event = registration.event
    return "\n".join([
        "DIEMS Event Ticket",
        f"Student Name: {user.name}",
        f"Student Email: {user.email}",
        f"Event Name: {event.title}",
    ])

@event_bp.route('/', methods=['GET'])
def get_events():
    events = Event.query.all()
    result = []
    for event in events:
        result.append({
            "id": event.id,
            "title": event.title,
            "description": event.description,
            "date_time": event.date_time.isoformat(),
            "venue": event.venue,
            "status": event.status,
            "category": event.category,
            "banner_image": event.banner_image,
            "organizer_name": event.organizer.name
        })
    return jsonify(result), 200

@event_bp.route('/<int:event_id>', methods=['GET'])
def get_event(event_id):
    event = Event.query.get_or_404(event_id)
    return jsonify({
        "id": event.id,
        "title": event.title,
        "description": event.description,
        "date_time": event.date_time.isoformat(),
        "venue": event.venue,
        "status": event.status,
        "category": event.category,
        "banner_image": event.banner_image,
        "organizer_name": event.organizer.name,
        "registration_limit": event.registration_limit
    }), 200

@event_bp.route('/', methods=['POST'])
@jwt_required()
def create_event():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if user.role not in ['organizer', 'admin']:
        return jsonify({"msg": "Unauthorized. Only organizers can create events."}), 403
        
    data = request.get_json()
    
    try:
        date_time = datetime.fromisoformat(data['date_time'].replace('Z', '+00:00'))
    except ValueError:
        return jsonify({"msg": "Invalid date format. Use ISO format."}), 400

    new_event = Event(
        title=data['title'],
        description=data['description'],
        venue=data['venue'],
        date_time=date_time,
        category=data.get('category'),
        registration_limit=data.get('registration_limit'),
        banner_image=data.get('banner_image'),
        organizer_id=current_user_id
    )
    
    db.session.add(new_event)
    db.session.commit()
    
    return jsonify({"msg": "Event created successfully", "event_id": new_event.id}), 201

@event_bp.route('/<int:event_id>/register', methods=['POST'])
@jwt_required()
def register_for_event(event_id):
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    event = Event.query.get_or_404(event_id)
    
    # Check if already registered
    existing_reg = Registration.query.filter_by(user_id=current_user_id, event_id=event_id).first()
    if existing_reg:
        return jsonify({"msg": "Already registered for this event"}), 400
        
    # Check capacity
    if event.registration_limit:
        current_count = Registration.query.filter_by(event_id=event_id).count()
        if current_count >= event.registration_limit:
            return jsonify({"msg": "Event capacity reached"}), 400
            
    registration = Registration(
        user_id=current_user_id,
        event_id=event_id,
        status='approved', # Automatically approve for now
    )
    
    db.session.add(registration)
    db.session.flush()

    try:
        qr_code_path = generate_qr_code(build_ticket_qr_data(registration))
    except Exception as e:
        print(f"Warning: Failed to generate QR code image: {e}")
        qr_code_path = None

    registration.qr_code = qr_code_path
    db.session.commit()
    
    return jsonify({"msg": "Successfully registered", "qr_code": qr_code_path}), 201

@event_bp.route('/registrations/<int:registration_id>/verify', methods=['GET'])
def verify_registration(registration_id):
    registration = Registration.query.get_or_404(registration_id)
    user = registration.user
    event = registration.event

    return jsonify({
        "id": registration.id,
        "status": registration.status,
        "attendance_status": registration.attendance_status,
        "registered_at": registration.registered_at.isoformat(),
        "student": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "department": user.department
        },
        "event": {
            "id": event.id,
            "title": event.title,
            "description": event.description,
            "date_time": event.date_time.isoformat(),
            "venue": event.venue,
            "status": event.status,
            "category": event.category,
            "organizer_name": event.organizer.name
        }
    }), 200

@event_bp.route('/<int:event_id>', methods=['PUT'])
@jwt_required()
def update_event(event_id):
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    event = Event.query.get_or_404(event_id)

    if user.role != 'admin' and event.organizer_id != int(current_user_id):
        return jsonify({"msg": "Unauthorized."}), 403

    data = request.get_json()
    
    if 'title' in data: event.title = data['title']
    if 'description' in data: event.description = data['description']
    if 'venue' in data: event.venue = data['venue']
    if 'date_time' in data: 
        try:
            event.date_time = datetime.fromisoformat(data['date_time'].replace('Z', '+00:00'))
        except ValueError:
            return jsonify({"msg": "Invalid date format. Use ISO format."}), 400
    if 'category' in data: event.category = data['category']
    if 'registration_limit' in data: event.registration_limit = data['registration_limit']
    if 'banner_image' in data: event.banner_image = data['banner_image']
    if 'status' in data: event.status = data['status']

    db.session.commit()
    
    # Broadcast event update via sockets
    from ..sockets import broadcast_event_update
    broadcast_event_update(event_id, {"msg": "Event updated", "event_id": event_id})
    
    return jsonify({"msg": "Event updated successfully"}), 200

@event_bp.route('/<int:event_id>', methods=['DELETE'])
@jwt_required()
def delete_event(event_id):
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    event = Event.query.get_or_404(event_id)

    if user.role != 'admin' and event.organizer_id != int(current_user_id):
        return jsonify({"msg": "Unauthorized."}), 403

    db.session.delete(event)
    db.session.commit()
    
    return jsonify({"msg": "Event deleted successfully"}), 200

@event_bp.route('/recommendations', methods=['GET'])
@jwt_required()
def get_recommendations():
    """
    Mock AI Event Recommendation System.
    In a real-world app, this would use a machine learning model to recommend events based on 
    past registrations, user department, and browsing history.
    Here we recommend upcoming events in the user's department or popular categories.
    """
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    # Simple logic: Recommend upcoming events
    recommended_events = Event.query.filter_by(status='upcoming').order_by(Event.date_time.asc()).limit(4).all()
    
    result = []
    for event in recommended_events:
        result.append({
            "id": event.id,
            "title": event.title,
            "category": event.category,
            "date_time": event.date_time.isoformat(),
            "banner_image": event.banner_image,
            "match_score": "95%" # Mocked match score
        })
        
    return jsonify(result), 200
