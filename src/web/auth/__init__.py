from flask import Blueprint, request, jsonify, render_template, redirect, url_for, session
from ...database import session as db
from ...database.models.user_model import User

auth = Blueprint("authorization", __name__, url_prefix='/authorization')

@auth.after_request
def add_header(response):
    """
    Add an Access-Control-Allow-Origin header to the response.

    :param response: The Flask response object.
    """
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "content-type, authorization"
    return response

@auth.route("/register", methods=["POST", "GET"])
async def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Check if username is already in the database
        existing_user = db.query(User).filter_by(username=username).first()

        if existing_user:
            return render_template('register.html')

        # Check if passwords match
        if password != confirm_password:
            return render_template('register.html')

        # Add user to the database
        new_user = User(username=username, password=password)
        db.add(new_user)
        db.commit()

        return redirect(url_for('authorization.login'))

    return render_template('register.html')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if username exists in the database
        user = db.query(User).filter_by(username=username).first()

        if user and password:
            # Authentication successful, set session variable
            session['username'] = username
            return redirect(url_for("manager.makebot"))
        return "not logged in"

    return render_template('login.html')

@auth.route('/logout')
def logout():
    # Remove the username from the session if it's present
    session.pop('username', None)
    return redirect(url_for("authorization.login"))