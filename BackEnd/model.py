from . import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    password_hash = db.Column(db.String(150), nullable=True)
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
"""class Thread(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), db.ForeignKey('user.email'), unique=True, nullable=False)
    thread_id = db.Column(db.String(150), nullable=False)"""

class Thread(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), db.ForeignKey('user.email'), unique=True, nullable=False)
    thread_id = db.Column(db.String(150), nullable=False)
    thread_ids = db.relationship('ThreadID', backref='thread', lazy=True)

class ThreadID(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    thread_id = db.Column(db.String(150), nullable=False)
    thread_ref_id = db.Column(db.Integer, db.ForeignKey('thread.id'), nullable=False)


