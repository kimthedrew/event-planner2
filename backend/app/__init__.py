# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from app.routes.user_routes import user_bp  # Import user_bp from user_routes
from app.routes.auth_routes import auth_bp  # Import auth_bp for authentication routes
from app.routes.event_routes import event_bp  # Import event_bp for event routes

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)

    # Enable CORS for the frontend (React) running on localhost:3000
    CORS(app, origins="http://localhost:3000")

    # Configure the app with necessary settings
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///event_planner.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'supersecret'  # This should be moved to environment variables

    # Initialize extensions with the app
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # Register blueprints
    app.register_blueprint(user_bp, url_prefix='/users')  # Register the user routes
    app.register_blueprint(auth_bp, url_prefix='/auth')  # Register the auth routes
    app.register_blueprint(event_bp, url_prefix='/events')  # Register the event routes

    return app
