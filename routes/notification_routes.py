from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Notification, User
from extensions import db

notification_bp = Blueprint('notification', __name__)

@notification_bp.route('/', methods=['GET'])
@jwt_required()
def get_notifications():
    current_user_id = get_jwt_identity()
    notifications = (
        Notification.query
        .filter_by(user_id=current_user_id)
        .order_by(Notification.created_at.desc())
        .limit(50)
        .all()
    )

    return jsonify([
        {
            "id": notification.id,
            "message": notification.message,
            "type": notification.type,
            "is_read": notification.is_read,
            "created_at": notification.created_at.isoformat()
        }
        for notification in notifications
    ]), 200

@notification_bp.route('/<int:notification_id>/read', methods=['PUT'])
@jwt_required()
def mark_notification_read(notification_id):
    current_user_id = get_jwt_identity()
    notification = Notification.query.get_or_404(notification_id)

    if notification.user_id != int(current_user_id):
        return jsonify({"msg": "Unauthorized."}), 403

    notification.is_read = True
    db.session.commit()
    return jsonify({"msg": "Notification marked as read"}), 200

@notification_bp.route('/read-all', methods=['PUT'])
@jwt_required()
def mark_all_notifications_read():
    current_user_id = get_jwt_identity()
    Notification.query.filter_by(user_id=current_user_id, is_read=False).update({"is_read": True})
    db.session.commit()
    return jsonify({"msg": "All notifications marked as read"}), 200
