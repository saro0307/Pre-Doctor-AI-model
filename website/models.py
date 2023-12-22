from . import db
from flask_login import UserMixin


class History(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bot = db.Column(db.String(500))
    user = db.Column(db.String(50))
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
#
#
# class User(db.Model, UserMixin):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(20), unique=True)
#     email = db.Column(db.String(50), unique=True)
#     password = db.Column(db.String(30))
#     hist = db.relationship('History')
#
#     def is_authenticated(self):
#         return True
#
#     def is_active(self):
#         return True
#
#     def is_anonymous(self):
#         return False
#
#     def get_id(self):
#         return str(self.id)

