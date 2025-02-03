# app/routes/user_routes.py
from flask import Blueprint, request, jsonify
from app import db
from app.models import User

user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/')
def home():
    return "Welcome to the Event Planner API!"

@user_bp.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])

@user_bp.route('/users', methods=['POST'])
def create_user():
    data = request.json
    new_user = User(name=data['name'], email=data['email'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user.to_dict()), 201
