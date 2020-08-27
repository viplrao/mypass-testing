from flask import Flask, redirect, render_template, request, flash, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from flask_login import LoginManager, UserMixin, current_user, login_user, logout_user, login_required
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app import app, db, migrate, login
from models import User, Password
from werkzeug.urls import url_parse
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import re
import forms
from app import login


@app.route('/', methods=["GET", "POST"])
@login_required
def index():
    # Find # of passwords per page, what page, total number of passwords
    ppp = app.config["POSTS_PER_PAGE"]
    page = request.args.get('page', 1, type=int)
    passwords = current_user.passwords.paginate(
        page, ppp, True)

    # Calculate how many pages needed -- used in index.html
    all_pass = current_user.passwords.all()
    l = len(all_pass)
    isint = (l / ppp).is_integer()
    if isint:
        num_pages = (l / ppp)
    else:
        num_pages = int((l / ppp)) + 1

    # Create links for forward and back buttons
    next_url = url_for('index', page=passwords.next_num) \
        if passwords.has_next else None

    prev_url = url_for('index', page=passwords.prev_num) \
        if passwords.has_prev else None

    return render_template('index.html', passwords=passwords.items, next_url=next_url,
                           prev_url=prev_url, num_pages=int(num_pages))


@app.route('/login', methods=["GET", "POST"])
def login():
    # inverse of @login_required
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = forms.LoginForm()

    # If submitting the WTForm:
    if form.validate_on_submit():

        # Look for an existing user
        user = db.session.query(User).filter(
            User.username == form.username.data).first()

        # If no user or wrong password:
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))

        login_user(user, remember=form.remember_me.data)

        # If a ?next was specified, use it:
        next = request.args.get("next")
        if not next or url_parse(next).netloc != "":
            next = url_for("index")

        return redirect(next)

    # If not submitting the form:
    return render_template('login.html', form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route('/register', methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    form = forms.RegistrationForm()

    if form.validate_on_submit():
        # Create user, use user method set_password
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)

        # Add user to db, save
        db.session.add(user)
        db.session.commit()

        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))

    else:
        return render_template("register.html", form=form)


@app.route("/hello/<name>")
def hello_there(name):
    now = datetime.now()
    formatted_now = now.strftime("%A, %d %B, %Y at %X.")

    # Filter the name argument to letters only using regular expressions. URL arguments
    # can contain arbitrary text, so we restrict to safe characters only.
    match_object = re.match("[a-zA-Z]+", name)

    if match_object:
        clean_name = match_object.group(0)
    else:
        clean_name = "Friend"

    content = "Hello there, " + clean_name + "! It's " + formatted_now
    return content


@app.route("/add", methods=["GET", "POST"])
@login_required
def add():

    form = forms.PassForm()

    if form.validate_on_submit():
        site = form.site.data
        username = form.username.data
        password = form.password.data

        # Add Site, Username, Password to db
        addition = Password(site=site, s_un=username, s_pass=password,
                            user_id=current_user.id)

        # Upload and save
        db.session.add(addition)
        db.session.commit()

        flash("Password Successfully added!")
        return redirect(url_for("index"))

    else:
        return render_template("add.html", form=form)


@app.route("/del", methods=["GET", "POST"])
@login_required
def delete():
    form = forms.DelForm()
    if form.validate_on_submit and request.method == "POST":
        username = form.username.data
        site = form.site.data
        password = Password.query.filter_by(s_un=username, site=site)
        
        db.session.delete(password)
        db.session.commit()
        flash(f"Password Deleted!")
        return redirect(url_for("index"))

    else:
        return render_template('delete.html', form=form)


@app.shell_context_processor
def make_shell_context():
    # Adds db, User, Password objects to `flask shell`
    return {'db': db, 'User': User, 'Password': Password}
