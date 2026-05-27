import os
import sys
# pyrefly: ignore [missing-import]
from werkzeug.security import generate_password_hash


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from app import create_app
from extensions import db
from models import User

app = create_app()

def seed_database():
    with app.app_context():

      
        db.create_all()

        print("Checking database...")

       
        existing_admin = User.query.filter_by(email="admin@diems.edu").first()

        if not existing_admin:
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

            print("Default users added successfully!")

        else:
            print("Users already exist. No duplicate data added.")

        print("Database ready and data stored permanently in app.db")

if __name__ == "__main__":
    seed_database()