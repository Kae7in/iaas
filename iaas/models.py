# from sqlalchemy import Column, Integer as Int, String, ForeignKey
from iaas import db
from passlib.apps import custom_app_context as pwd_context


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(32), index = True)
    password_hash = db.Column(db.String(128))
    integers = db.relationship('Integer', backref='user', lazy='dynamic')
    authenticated = db.Column(db.Boolean, default=False)

    def is_authenticated(self):
        return self.authenticated

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def __init__(self, username=None, password=None, integers=[]):
        self.username = username
        self.set_password(password)
        self.integers = integers

    def get_id(self):
        return unicode(self.id)

    def set_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def json(self):
        return {
            'id': self.id,
            'username': self.username,
            'integers': self.integers
        }


class Integer(db.Model):
    __tablename__ = 'integer'
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String, unique=False)
    value = db.Column(db.Integer, unique=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

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
