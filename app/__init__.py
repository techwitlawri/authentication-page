#  Initializes the flask app
from flask import Flask
from .extensions import db, login_manager
from .models import User
from .auth import auth_bp
from .routes import main_bp  # The blueprint where dashboard lives


def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
   
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'  # Redirect if user not logged in

    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(main_bp)


    
    with app.app_context():
        db.create_all()  # Ensure this is here to create the tables

    return app


# Add this line to load the user by ID
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))