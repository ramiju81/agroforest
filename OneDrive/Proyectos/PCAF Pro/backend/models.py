# backend/models.py
from datetime import datetime
from backend import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(20))  # 'user' o 'trainer'
    measurements = db.relationship('Measurement', backref='user', lazy='dynamic')
    workouts = db.relationship('Workout', backref='user', lazy='dynamic')

class Measurement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    weight = db.Column(db.Float)
    height = db.Column(db.Float)
    muscle_mass = db.Column(db.Float)
    body_fat = db.Column(db.Float)

class Workout(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    trainer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    completed = db.Column(db.Boolean, default=False)
    exercises = db.relationship('Exercise', backref='workout', lazy='dynamic')

class Exercise(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey('workout.id'))
    name = db.Column(db.String(140))
    sets = db.Column(db.Integer)
    reps = db.Column(db.Integer)
    weight = db.Column(db.Float)
    notes = db.Column(db.Text)