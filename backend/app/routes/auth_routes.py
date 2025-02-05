from flask import Blueprint, request, jsonify
from app import db, bcrypt
from app.models import User
from flask_jwt_extended import create_access_token

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    if User.query.filter_by(email=data['email']).first():
        return jsonify(message="Email already in use"), 400

    # Pass the plain text password to User constructor (it will be hashed there)
    new_user = User(name=data['name'], email=data['email'], password=data['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify(message="User created successfully"), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        print("Received data:", data)  # Debugging output

        if not data:
            return jsonify({"error": "Missing JSON data"}), 400

        email = data.get('email')
        password = data.get('password')

        user = User.query.filter_by(email=email).first()

        if user and bcrypt.check_password_hash(user.password, password):
            access_token = create_access_token(identity=str(user.id))
            return jsonify({"access_token": access_token}), 200

        return jsonify({"error": "Invalid email or password"}), 401

    except Exception as e:
        print("Error:", str(e))  # Print error in the console
        return jsonify({"error": "Internal Server Error"}), 500
