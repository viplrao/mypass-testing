from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_mail import Mail

# Initialise and Config app, SQLAlchemy, and flask_login. Login user loader is in models for some reason.
app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

login = LoginManager(app)
login.login_view = 'login'

bootstrap = Bootstrap(app)

mail = Mail(app)

""" leave this here """
import routes
