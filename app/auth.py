from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import User
from .extensions import db
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        username = request.form.get('username')
        gender = request.form.get('gender')
        phone = request.form.get('phone')
        email = request.form.get('email')
        date_of_birth = request.form.get('date_of_birth')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        # basic validation

         # Basic validation
        if not all([first_name, last_name, username, gender, email, date_of_birth, password, confirm_password]):
            flash('Please fill in all required fields.', 'error')
            return redirect(url_for('auth.register'))

        if password != confirm_password:
            flash('Passwords do not match.', 'error')
            return redirect(url_for('auth.register'))

        # Check if username or email already exists
        if User.query.filter_by(username=username).first():
            flash('Username already taken.', 'error')
            return redirect(url_for('auth.register'))

        if User.query.filter_by(email=email).first():
            flash('Email already registered.', 'error')
            return redirect(url_for('auth.register'))

        # Create new user
        new_user = User(
            first_name=first_name,
            last_name=last_name,
            username=username,
            gender=gender,
            phone=phone,
            email=email,
            date_of_birth=datetime.strptime(date_of_birth, '%Y-%m-%d')
        )
        new_user.set_password(password)  # Hash password

        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful!', 'success')
        return redirect(url_for('auth.login'))

    return render_template('register.html')
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        #  get form data
        identifier = request.form.get('username')
        password = request.form.get('password')

        #  validate input
        if not all([identifier , password]):
            flash('Please enter username and password', 'error')
            return redirect(url_for('auth.login'))
        
        #   Find user by username
        user = User.query.filter_by( (User.username == identifier) | (User.email == identifier)
        ).first()
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('main.dashboard'))
        
        else:
            flash('Invalid username or password.', 'error')
            return redirect(url_for('auth.login'))

    # If GET, show login form
    return render_template('login.html')


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('you have been logged out.', 'info')
    return redirect(url_for('auth.login'))


        

