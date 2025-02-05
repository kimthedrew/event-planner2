from flask import Blueprint, request, jsonify
from app import db
from app.models import User

# Define the user blueprint
user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/', methods=['GET'], strict_slashes=False)
@user_bp.route('', methods=['GET'], strict_slashes=False)
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])

@user_bp.route('/', methods=['POST'], strict_slashes=False)
@user_bp.route('', methods=['POST'], strict_slashes=False)
def create_user():
    data = request.get_json()

    if not data.get('password') or not data.get('name'):
        return jsonify({"error": "Password and Name are required"}), 400

    new_user = User(name=data['name'], email=data['email'], password=data['password'])
    db.session.add(new_user)
    db.session.commit()

    return jsonify(new_user.to_dict()), 201
