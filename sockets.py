from flask_socketio import emit, join_room, leave_room
from extensions import socketio

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@socketio.on('join')
def on_join(data):
  
    room = data.get('room')
    if room:
        join_room(room)
        print(f'Client joined room {room}')

@socketio.on('leave')
def on_leave(data):
    room = data.get('room')
    if room:
        leave_room(room)
        print(f'Client left room {room}')

def send_notification(user_id, message, notification_type):
    """
    Utility function to send a notification to a specific user's room.
    """
    socketio.emit('notification', {
        'message': message,
        'type': notification_type
    }, room=f'user_{user_id}')
    
def broadcast_event_update(event_id, data):
    """
    Utility function to broadcast an event update to all clients watching an event.
    """
    socketio.emit('event_update', data, room=f'event_{event_id}')
