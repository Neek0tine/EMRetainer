from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin
from .config import Config
import os

template_dir = os.path.abspath('emrr/frontend/templates')
static_dir = os.path.abspath('emrr/frontend/assets')

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
app.config.from_object(Config)
app.app_context().push()              

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.login_message_category = "info"

from backend.auth.dbmodel import Staff 

@login_manager.user_loader
def load_user(user_id):
    return Staff.query.get(int(user_id))

from backend.auth import routes
# from backend.util.errors import defaultHandler
