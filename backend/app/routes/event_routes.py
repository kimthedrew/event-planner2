from flask import Blueprint, request, jsonify
from app import db
from app.models import Event, RSVP
from flask_jwt_extended import jwt_required, get_jwt_identity

event_bp = Blueprint('event_bp', __name__)

@event_bp.route('/', methods=['GET'])
def get_events():
    events = Event.query.all()
    return jsonify([event.to_dict() for event in events])

@event_bp.route('/create', methods=['POST'])
@jwt_required()
def create_event():
    data = request.get_json()
    user_id = get_jwt_identity()

    try:
        new_event = Event(
            name=data['name'],
            event_type=data['event_type'],
            age_limit=data['age_limit'],
            location=data['location'],
            time=data['time'],
            max_attendees=data['max_attendees'],
            drinks_available=data['drinks_available'],
            created_by=user_id  # Store the creator's ID
        )
        db.session.add(new_event)
        db.session.commit()

        return jsonify({"msg": "Event created successfully!"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
@event_bp.route('/<int:event_id>/rsvp', methods=['POST'])
@jwt_required()
def rsvp_for_event(event_id):
    user_id = get_jwt_identity()
    
    event = Event.query.get(event_id)
    if not event:
        return jsonify({"error": "Event not found"}), 404
    
    # Check if user has already RSVP'd
    existing_rsvp = RSVP.query.filter_by(user_id=user_id, event_id=event_id).first()
    if existing_rsvp:
        return jsonify({"error": "You have already RSVP’d for this event"}), 400
    
    # Check if max attendees reached
    if RSVP.query.filter_by(event_id=event_id).count() >= event.max_attendees:
        return jsonify({"error": "Event is full"}), 400

    new_rsvp = RSVP(user_id=user_id, event_id=event_id)
    db.session.add(new_rsvp)
    db.session.commit()

    return jsonify({"msg": "RSVP successful!"}), 201
