from datetime import datetime
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

# Initialize SQL tables Users, Passwords


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    passwords = db.relationship('Password', backref="user", lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Password(db.Model):
    __tablename__ = "passwords"
    id = db.Column(db.Integer, primary_key=True)
    site = db.Column(db.String(256))
    s_un = db.Column(db.String(256))
    s_pass = db.Column(db.String(500))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    def __repr__(self):
        return '<Password {}>'.format(self.body)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))