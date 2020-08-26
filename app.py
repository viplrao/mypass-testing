from flask import Flask, redirect, render_template, request, flash, url_for
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, current_user, login_user, logout_user, login_required
from flask_bootstrap import Bootstrap
from logging.handlers import RotatingFileHandler
from flask_mail import Mail
import os

# Initizalise and Config app, SQLAlchemy, and flask_login. Login user loader is in models for some reason.
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
