# user model(database structure)

from datetime import datetime
from.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(db.Model, UserMixin):
    """User model to store user credentials"""
    id = db.Column(db.Integer, primary_key=True)
    first_name= db.Column(db.String(100), nullable= False)
    last_name = db.Column(db.String(100), nullable= False)
    username= db.Column(db.String(150), unique= True, nullable= False)
    gender = db.Column(db.String(20))
    phone = db.Column(db.String(20), unique= True)
    email = db.Column(db.String(200), unique= True, nullable= False)
    date_of_birth= db.Column(db.Date)
    password_hash = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password):
        """Hash the password and store the hash."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Check if the provided password matches the hashed password."""
        return check_password_hash(self.password_hash, password)