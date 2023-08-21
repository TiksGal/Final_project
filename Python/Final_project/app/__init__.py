import os
from flask import Flask
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

# Base directory
basedir = os.path.abspath(os.path.dirname(__file__))

# Flask App setup
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "game.db")
app.config["SECRET_KEY"] = "7e00696cd12d5df1dea20f5056a5f47e"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Flask-Session setup
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# Flask-SQLAlchemy setup
db = SQLAlchemy(app)

# Flask-Bcrypt setup
bcrypt = Bcrypt(app)

# Flask-Login setup
login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message_category = "info"

# App context - Important for certain operations like creating tables
with app.app_context():
    # Import the Player model 
    from app.models.models import Player
    
    # Create the tables
    db.create_all()

    # User loader callback for Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        return Player.query.get(int(user_id))

    # Import routes at the end to avoid circular imports
    from app import routes



