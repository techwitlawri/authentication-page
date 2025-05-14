# user model(database structure)

from datetime import datetime
from.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(db.Model, UserMixin):
    """User model to store user credentials"""
    id = db.Column(db.Integer, primary_key=True)
    fullname= db.Column(db.String(100))
    username= db.Column(db.String(150), unique= True, nullable= False)
    password_hash = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password):
        """Hash the password and store the hash."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Check if the provided password matches the hashed password."""
        return check_password_hash(self.password_hash, password)