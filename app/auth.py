from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import User
from .extensions import db
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash


auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        fullname = request.form.get('fullname')
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')


        # basic validation

        if not all([fullname, username, password, confirm_password]):
            flash('All fields are required.', 'error')
            return redirect(url_for('auth.register'))
        
        if password != confirm_password:
            flash('passwords do not match.', 'error')
            return redirect(url_for('auth.register'))
        
        #  Hash the password and save user

        hashed_password = generate_password_hash(password)
        new_user = User(fullname= fullname, username= username, password_hash=hashed_password)
        
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successfull', 'success')
        return redirect(url_for('auth.login'))
    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        #  get form data
        username = request.form.get('username')
        password = request.form.get('password')

        #  validate input
        if not all([username, password]):
            flash('Please enter username and password', 'error')
            return redirect(url_for('auth.login'))
        
        #   Find user by username
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        
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


        

