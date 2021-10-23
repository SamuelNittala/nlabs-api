from enum import unique

from sqlalchemy.orm import relation, relationship
from . import db

class Advisor(db.Model):
    __tablename__ = "advisors"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    photo_url = db.Column(db.String(120), nullable=False,)

    booking = db.relationship("Booking")

    def __init__(self,username,photo_url):
        self.username = username
        self.photo_url = photo_url

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False, unique=True)
    role = db.Column(db.String(10), nullable=False)

    booking = db.relationship("Booking")

    def __init__(self,username, password, email, role):
        self.username = username
        self.password = password
        self.email = email
        self.role = role

class Booking(db.Model):
    __tablename__ = "bookings"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    advisor_id = db.Column(db.Integer, db.ForeignKey('advisors.id'))
    timing = db.Column(db.DateTime)

    def __init__(self, user_id, advisor_id,timing):
        self.user_id = user_id
        self.advisor_id = advisor_id
        self.timing = timing


