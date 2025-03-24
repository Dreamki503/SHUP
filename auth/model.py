from config import db
from flask_login import UserMixin
from  werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    phone = db.Column(db.String(100), nullable = False, default = 'Not Provided')
    role = db.Column(db.String(100), nullable = False, default = 'customer')
    profile_pic = db.Column(db.String(255), nullable = True)
    password_hash = db.Column(db.String(500), nullable = True)
    created_at = db.Column(db.DateTime , default = datetime.now)

    def _repr_(self):
        return f"<User {self.email}>"
    
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute!')
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)