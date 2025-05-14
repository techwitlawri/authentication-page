#  Routes for register & login

from flask_login import login_required, current_user
from flask import Blueprint, render_template,redirect,url_for

main_bp = Blueprint('main', __name__)

# Create a route for the homepage (root URL)
@main_bp.route('/')
def home():
    return redirect(url_for('auth.login'))

@main_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', user=current_user)