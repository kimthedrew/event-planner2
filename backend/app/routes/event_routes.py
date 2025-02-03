# app/routes/event_routes.py
from flask import Blueprint, request, jsonify

event_bp = Blueprint('event_bp', __name__)

@event_bp.route('/', methods=['GET'])
def get_events():
    # Import db locally inside the function to avoid circular import
    from app import db
    from app.models import Event
    events = Event.query.all()
    return jsonify([event.to_dict() for event in events])

@event_bp.route('/', methods=['POST'])
def create_event():
    # Import db locally inside the function to avoid circular import
    from app import db
    from app.models import Event
    data = request.json
    new_event = Event(name=data['name'], date=data['date'], location=data['location'])
    db.session.add(new_event)
    db.session.commit()
    return jsonify(new_event.to_dict()), 201
