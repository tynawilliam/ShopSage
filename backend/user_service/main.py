from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from datetime import timedelta
from .config import Config
from .database import db
from .models.user import User
from .routes.user_routes import users
from .routes.auth_routes import auth
from .utils import bcrypt

app = Flask(__name__)
CORS(app)
app.config.from_object(Config)
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=1)
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=7)
bcrypt.init_app(app)

db.init_app(app)
migrate = Migrate(app, db)

jwt = JWTManager(app)

app.register_blueprint(users, url_prefix='/users')
app.register_blueprint(auth, url_prefix='/auth')
