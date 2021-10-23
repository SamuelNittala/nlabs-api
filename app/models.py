from enum import unique

from sqlalchemy.orm import backref
from . import db

bookings = db.Table('bookings',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('advisor_id', db.Integer,db.ForeignKey('advisor.id'))
)

class Advisor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    photo_url = db.Column(db.String(120), nullable=False,)

    def __init__(self,username,photo_url):
        self.username = username
        self.photo_url = photo_url

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False, unique=True)
    role = db.Column(db.String(10), nullable=False)
    bookings = db.relationship("Advisor",secondary=bookings,backref=db.backref('clients', lazy='dynamic'))

    def __init__(self,username, password, email, role):
        self.username = username
        self.password = password
        self.email = email
        self.role = role

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    advisor_id = db.Column(db.Integer, db.ForeignKey("advisor.id"))
    timing = db.Column(db.DateTime)

    def __init__(self,user_id,advisor_id,timing):
        self.user_id = user_id
        self.advisor_id = advisor_id
        self.timing = timing




