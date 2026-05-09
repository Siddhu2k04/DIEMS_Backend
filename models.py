from datetime import datetime, timezone
from extensions import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='student') # student, organizer, admin
    profile_picture = db.Column(db.String(255), nullable=True)
    department = db.Column(db.String(100), nullable=True)
    points = db.Column(db.Integer, default=0)
    badges = db.Column(db.JSON, nullable=True) # JSON array of badges
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    registrations = db.relationship('Registration', backref='user', lazy=True)
    events_organized = db.relationship('Event', backref='organizer', lazy=True)
    notifications = db.relationship('Notification', backref='user', lazy=True)
    feedbacks = db.relationship('Feedback', backref='user', lazy=True)
    certificates = db.relationship('Certificate', backref='user', lazy=True)
    messages = db.relationship('ChatMessage', backref='sender', lazy=True)

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    banner_image = db.Column(db.String(255), nullable=True)
    venue = db.Column(db.String(200), nullable=False)
    date_time = db.Column(db.DateTime, nullable=False)
    registration_limit = db.Column(db.Integer, nullable=True)
    category = db.Column(db.String(100), nullable=True)
    status = db.Column(db.String(20), default='upcoming') # upcoming, ongoing, completed, cancelled
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    
    organizer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    registrations = db.relationship('Registration', backref='event', lazy=True)
    announcements = db.relationship('Announcement', backref='event', lazy=True)
    feedbacks = db.relationship('Feedback', backref='event', lazy=True)
    certificates = db.relationship('Certificate', backref='event', lazy=True)
    chat_messages = db.relationship('ChatMessage', backref='event', lazy=True)

class Registration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    qr_code = db.Column(db.String(255), nullable=True)
    status = db.Column(db.String(20), default='pending') # pending, approved, rejected
    attendance_status = db.Column(db.Boolean, default=False)
    registered_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.Text, nullable=False)
    type = db.Column(db.String(50), nullable=False) # e.g., 'event_update', 'registration_approved'
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Announcement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False) # 1 to 5
    comment = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)

class Certificate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    certificate_url = db.Column(db.String(255), nullable=False)
    issued_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)

class ChatMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class AttendanceLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    scanned_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    
    registration_id = db.Column(db.Integer, db.ForeignKey('registration.id'), nullable=False)
    registration = db.relationship('Registration', backref=db.backref('attendance_logs', lazy=True))
