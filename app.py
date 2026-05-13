import os
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from extensions import db, jwt, socketio
from flasgger import Swagger

load_dotenv()

def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": "*"}})

    # Configuration
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev_secret_key')
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'jwt_dev_secret_key')
    
    # Use MySQL if provided in DATABASE_URL, else fallback to SQLite
    base_dir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', f'sqlite:///{os.path.join(base_dir, "app.db")}')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    socketio.init_app(app, cors_allowed_origins="*")
    
    # Initialize Swagger
    swagger_config = {
        "headers": [],
        "specs": [
            {
                "endpoint": 'apispec_1',
                "route": '/apispec_1.json',
                "rule_filter": lambda rule: True,
                "model_filter": lambda tag: True,
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/apidocs/"
    }
    Swagger(app, config=swagger_config)

    # Import and register blueprints
    from routes.auth_routes import auth_bp
    from routes.event_routes import event_bp
    from routes.organizer_routes import organizer_bp
    from routes.admin_routes import admin_bp
    from routes.notification_routes import notification_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(event_bp, url_prefix='/api/events')
    app.register_blueprint(organizer_bp, url_prefix='/api/organizer')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')
    app.register_blueprint(notification_bp, url_prefix='/api/notifications')

    # Import socket events
    import sockets

    # Create tables
    with app.app_context():
        import models
        db.create_all()

    return app

if __name__ == '__main__':
    app = create_app()
    socketio.run(app, debug=True, port=5000, allow_unsafe_werkzeug=True)
