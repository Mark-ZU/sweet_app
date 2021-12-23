from flask_login import UserMixin
from . import db

class User(UserMixin, db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(100))
    password=db.Column(db.String(100))
    def __repr__(self):
        return '<User {}>'.format(self.id)

class Table(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    pos_x=db.Column(db.Float)
    pos_y=db.Column(db.Float)
    radius=db.Column(db.Float)
    capacity=db.Column(db.Integer)
    def __repr__(self):
        return '<Table {}>'.format(self.id)
    def to_dict(self):
        return {
            "id":self.id,
            "x":self.pos_x,
            "y":self.pos_y,
            "r":self.radius,
            "capa":self.capacity
        }

class Guest(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(100))
    phone=db.Column(db.String(100))
    arranged=db.Column(db.Boolean)
    table=db.Column(db.Integer)
    seat_id=db.Column(db.Integer)
    def __repr__(self):
        return '<Guest {}>'.format(self.id)
    def to_dict(self):
        return {
            "id":self.id,
            "name":self.name,
            "phone":self.phone if self.phone else "",
            "arranged":1 if self.arranged else 0,
            "table":self.table,
            "seat":self.seat_id
        }
