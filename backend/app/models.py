from app import db, bcrypt
from flask_sqlalchemy import SQLAlchemy

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    def to_dict(self):
        return {"id": self.id, "name": self.name, "email": self.email}


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    event_type = db.Column(db.String(50), nullable=False)
    age_limit = db.Column(db.Integer, nullable=False)
    drinks_available = db.Column(db.Boolean, default=False)
    location = db.Column(db.String(200), nullable=False)
    time = db.Column(db.String(50), nullable=False)
    max_attendees = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(50), default="Active")  # Active, Postponed, Canceled
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "event_type": self.event_type,
            "age_limit": self.age_limit,
            "drinks_available": self.drinks_available,
            "location": self.location,
            "time": self.time,
            "max_attendees": self.max_attendees,
            "status": self.status,
            "created_by": self.created_by
        }
class RSVP(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)

    user = db.relationship('User', backref=db.backref('rsvps', lazy=True))
    event = db.relationship('Event', backref=db.backref('rsvps', lazy=True))