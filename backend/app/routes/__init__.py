# routes/__init__.py should only handle blueprint imports and registration
from flask import Blueprint

# Import blueprints from individual route files
from app.routes.user_routes import user_bp
from app.routes.auth_routes import auth_bp
from app.routes.event_routes import event_bp

def register_routes(app):
    # Register blueprints with the app
    app.register_blueprint(user_bp, url_prefix='/users')  # Register user blueprint
    app.register_blueprint(auth_bp, url_prefix='/auth')  # Register auth blueprint
    app.register_blueprint(event_bp, url_prefix='/events')  # Register event blueprint
