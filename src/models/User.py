from datetime import datetime
from flask_login import UserMixin
from flask import current_app

from src import db, login, bcrypt


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    email = db.Column(db.String(255), index=True, unique=True)
    password = db.Column(db.String(255))
    hourly_rate = db.Column(db.Integer, default=0)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = bcrypt.generate_password_hash(
            password, current_app.config["BCRYPT_LOG_ROUNDS"]
        ).decode()


def create_user(name, email, password):
    user = User(name, email, password)
    db.session.add(user)
    db.session.commit()

    return user


def get_user_by_email(email):
    return User.query.filter_by(email=email).first()


def get_user_by_id(user_id):
    return User.query.get(user_id)


def change_user_password(user_id, password):
    user = get_user_by_id(user_id)
    user.password = bcrypt.generate_password_hash(
        password, current_app.config["BCRYPT_LOG_ROUNDS"]
    ).decode()

    db.session.commit()

    return True


def update_user(user_id, name, email, hourly_rate):
    user = get_user_by_id(user_id)
    user.name = name
    user.email = email
    user.hourly_rate = hourly_rate

    db.session.commit()

    return True


def get_all_users():
    return User.query.all()


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
