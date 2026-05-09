import os
import sys
from datetime import datetime, timedelta, timezone
from werkzeug.security import generate_password_hash

# Ensure the workspace root is on sys.path so package imports work
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from app import create_app
from extensions import db
from models import User

app = create_app()

def seed_database():
    with app.app_context():
        # Drop all tables and recreate them
        db.drop_all()
        db.create_all()
        
        print("Seeding database...")
        
        # 1. Create Users (Admin, Organizer, Student)
        admin = User(
            name="Admin User",
            email="admin@diems.edu",
            password_hash=generate_password_hash("admin123"),
            role="admin"
        )
        
        organizer = User(
            name="Tech Club",
            email="techclub@diems.edu",
            password_hash=generate_password_hash("org123"),
            role="organizer"
        )
        
        student = User(
            name="John Student",
            email="john@diems.edu",
            password_hash=generate_password_hash("student123"),
            role="student",
            department="Computer Science",
            points=150
        )
        
        db.session.add_all([admin, organizer, student])
        db.session.commit()
        
        print("Database seeding completed successfully!")

if __name__ == "__main__":
    seed_database()
