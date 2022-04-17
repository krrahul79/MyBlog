from enum import unique
from blog import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(15), unique=True, nullable=False)
    first_name = db.Column(db.String(30), nullable=False)
    hashed_password = db.Column(db.String(128))
    comments = db.relationship('Comments', backref='user', lazy=True)
    rating = db.relationship('Rating', backref='user', lazy=True)

    def __repr__(self):
        return f"User('{self.user_id}',{self.email}', '{self.first_name}')"

    @property
    def password(self):
        raise AttributeError('Password is not readable.')

    @password.setter
    def password(self, password):
        self.hashed_password = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.hashed_password, password)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_title = db.Column(db.String(50), nullable=False)
    post_short_desc = db.Column(db.Text)
    post_desc = db.Column(db.Text)
    post_image = db.Column(db.String(30), unique=True, nullable=True)
    post_type = db.Column(db.String(10), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    comments = db.relationship('Comments', backref='post', lazy=True)
    rating = db.relationship('Rating', backref='post', lazy=True)


    def __repr__(self):
        return f"Post('{self.post_id}', '{self.post_short_desc}', '{self.post_full_desc}')"


class Post_Details(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    post_desc = db.Column(db.Text)
    post_image = db.Column(db.String(30), unique=True, nullable=True)


class Rating(db.Model):
    rating_id = db.Column(db.Integer, primary_key=True)
    rating_value = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)

    def __repr__(self):
        return f"Rating('{self.rating_id}', '{self.rating_value}')"


class Comments(db.Model):
    comment_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    comment_desc = db.Column(db.Text)

    def __repr__(self):
        return f"Rating('{self.comment_id}', '{self.comment_desc}')"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
