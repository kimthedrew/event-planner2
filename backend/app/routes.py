from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from . import db
from .models import User, Event, RSVP

bp = Blueprint('routes', __name__)

@bp.route('/signup', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if User.query.filter_by(username=username).first():
        return jsonify({"msg": "Username already exists"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"msg": "Email already exists"}), 400

    new_user = User(username, email, password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"msg": "User created successfully"}), 201

@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()

    if user and user.check_password(password):
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"msg": "Invalid credentials"}), 401

@bp.route('/events', methods=['POST'])
@jwt_required()
def create_event():
    user_id = get_jwt_identity()
    data = request.get_json()

    title = data.get('title')
    date = data.get('date')
    location = data.get('location')
    description = data.get('description')

    new_event = Event(title=title, date=date, location=location, description=description, user_id=user_id)
    db.session.add(new_event)
    db.session.commit()

    return jsonify({"msg": "Event created successfully"}), 201

@bp.route('/events', methods=['GET'])
def get_events():
    events = Event.query.all()
    events_list = [{"title": event.title, "date": event.date, "location": event.location, "description": event.description} for event in events]
    return jsonify(events_list)

@bp.route('/events/<int:event_id>', methods=['GET'])
def get_event(event_id):
    event = Event.query.get_or_404(event_id)
    return jsonify({"title": event.title, "date": event.date, "location": event.location, "description": event.description})

@bp.route('/rsvp/<int:event_id>', methods=['POST'])
@jwt_required()
def rsvp(event_id):
    user_id = get_jwt_identity()
    event = Event.query.get_or_404(event_id)

    existing_rsvp = RSVP.query.filter_by(user_id=user_id, event_id=event_id).first()
    if existing_rsvp:
        return jsonify({"msg": "You have already RSVP'd to this event."}), 400

    new_rsvp = RSVP(user_id=user_id, event_id=event_id)
    db.session.add(new_rsvp)
    db.session.commit()

    return jsonify({"msg": "RSVP successful!"}), 200
