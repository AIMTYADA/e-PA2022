from flask_login import UserMixin
from . import db


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column('id', db.Integer, primary_key=True)
    email = db.Column('email', db.String(), unique=True)
    password = db.Column('password', db.String())
    name = db.Column('name', db.String())
