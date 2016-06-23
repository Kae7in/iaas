from sqlalchemy import Column, Integer as Int, String, ForeignKey
from sqlalchemy.orm import relationship
from iaas import db
from passlib.apps import custom_app_context as pwd_context


class User(db.Model):
    __tablename__ = 'users'
    id = Column(Int, primary_key = True)
    username = Column(String(32), index = True)
    password_hash = Column(String(128))
    integers = relationship('Integer', backref='user')

    def __init__(self, username=None, password_hash=None):
        self.username = username
        self.password_hash = password_hash

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def json(self):
        return {
            'id': self.id,
            'username': self.username
        }


class Integer(db.Model):
    __tablename__ = 'integers'
    id = Column(Int, primary_key=True)
    label = Column(String, unique=False)
    value = Column(Int, unique=False)
    user_id = Column(Int, ForeignKey('users.id'))

    def __init__(self, value=None, label=None, token=None):
        self.label = label
        self.value = value
        self.user_id = token  # TODO: Get user_id from User-Token table

    def __repr__(self):
        return 'value: %d' % self.value

    def json(self):
        return {
            'id': self.id,
            'label': self.label,
            'value': self.value
        }
