from flask import Blueprint, request, jsonify
from app import db
from app.models import Event
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

    new_event = Event(
        name=data['name'],
        event_type=data['event_type'],
        age_limit=data['age_limit'],
        drinks_available=data['drinks_available'],
        location=data['location'],
        time=data['time'],
        max_attendees=data['max_attendees'],
        created_by=user_id
    )
    db.session.add(new_event)
    db.session.commit()
    return jsonify(new_event.to_dict()), 201


@event_bp.route('/<int:event_id>', methods=['DELETE'])
@jwt_required()
def delete_event(event_id):
    event = Event.query.get(event_id)
    if not event:
        return jsonify({"error": "Event not found"}), 404

    db.session.delete(event)
    db.session.commit()
    return jsonify({"message": "Event deleted"}), 200
