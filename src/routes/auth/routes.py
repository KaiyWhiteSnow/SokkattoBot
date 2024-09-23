from flask import request, render_template, redirect, url_for, session
from ...database import session as db
from ...database.models.user_model import User
from . import auth
from .forms import RegistrationForm, LoginForm

@auth.route("/register", methods=["POST", "GET"])
async def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        # Check if username is already in the database
        existing_user = db.query(User).filter_by(username=username).first()

        if existing_user:
            return render_template('auth/register.html', form=form)

        # Add user to the database
        new_user = User(username=username, password=password)
        db.add(new_user)
        db.commit()

        return redirect(url_for('auth.login'))

    return render_template('auth/register.html', form=form)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        # Check if username exists in the database
        user = db.query(User).filter_by(username=username).first()

        if user and password:
            session['username'] = username
            return redirect(url_for("manager.makebot"))
        return "not logged in"

    return render_template('auth/login.html', form=form)
