"""
ORM for User.
"""
import datetime
from . import db
from sqlalchemy.orm import validates
from typing import Optional
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    email = db.Column(db.String(320), nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    date_created = db.Column(db.DateTime)

    def __init__(self, username: str, email: str, password: str) -> None:
        if len(password) < 8:
            raise ValueError('Password too short')
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)
        self.date_created = datetime.datetime.now()

    @classmethod
    def get_by_username(cls, username: str) -> Optional['User']:
        """
        Get User from database - query by username.
        :param username: Username string.
        :return: User object or None.
        """
        return cls.query.filter_by(username=username).first()

    @classmethod
    def get_by_id(cls, _id) -> Optional['User']:
        """
        Get User from database - query by ID.
        :param _id: Numeric ID.
        :return: User object or None.
        """
        return cls.query.get(_id)

    @classmethod
    def get_by_email(cls, email: str) -> Optional['User']:
        """
        Get User from database - query by email.
        :param email: Email string.
        :return: User object or None.
        """
        return cls.query.filter_by(email=email).first()

    def password_correct(self, password: str) -> bool:
        """
        Check plaintext password against hashed password in database.
        :param password: Password string.
        :return: Boolean value.
        """
        return check_password_hash(self.password, password)

    @validates('username')
    def validate_username(self, key, value):
        if len(key) < 2:
            raise ValueError('Username too short')
        return value

    @validates('email')
    def validate_email(self, key, value):
        if '@' not in value or len(key) < 3:
            raise ValueError('Incorrect email format')
        return value

    def __repr__(self):
        return f'<User id:{self.id} username: {self.username}>'

    def json(self):
        return {'username': self.username, 'id': self.id}

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()