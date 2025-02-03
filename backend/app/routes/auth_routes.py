# app/routes/auth_routes.py
from flask import Blueprint, request, jsonify

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    # Import db and bcrypt locally inside the function to avoid circular import
    from app import db, bcrypt
    from app.models import User
    data = request.json
    user = User.query.filter_by(email=data['email']).first()
    
    if user and bcrypt.check_password_hash(user.password, data['password']):
        return jsonify(message="Login successful"), 200
    else:
        return jsonify(message="Invalid credentials"), 401

@auth_bp.route('/signup', methods=['POST'])
def signup():
    # Import db and bcrypt locally inside the function to avoid circular import
    from app import db, bcrypt
    from app.models import User
    data = request.json
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify(message="Email already in use"), 400
    
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    new_user = User(name=data['name'], email=data['email'], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify(message="User created successfully"), 201
