from flask import Blueprint, request, jsonify, render_template, redirect, url_for, session
from Database.Database import Session, func
from Database.UserModel import Users

User = Blueprint("user", __name__)

session_instance = Session()

@User.after_request
def add_header(response):
    """
    Add an Access-Control-Allow-Origin header to the response.

    :param response: The Flask response object.
    """
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "content-type, authorization"
    return response

@User.route("/register", methods=["POST", "GET"])
async def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Check if username is already in the database
        existing_user = session_instance.query(Users).filter_by(Username=username).first()

        if existing_user:
            return render_template('register.html', message='Username already exists. Choose a different one.')

        # Check if passwords match
        if password != confirm_password:
            return render_template('register.html', message='Passwords do not match. Please try again.')

        # Add user to the database
        new_user = Users(Username=username, Password=password)
        session_instance.add(new_user)
        session_instance.commit()

        return redirect(url_for('user.login'))

    return render_template('register.html')

@User.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if username exists in the database
        user = session_instance.query(Users).filter_by(Username=username).first()

        if user and password:
            # Authentication successful, set session variable
            session['username'] = username
            return redirect(url_for("rustplus.makeBot"))
        else:
            return "not logged in"

    return render_template('login.html')

@User.route('/logout')
def logout():
    # Remove the username from the session if it's present
    session.pop('username', None)
    return redirect(url_for(User.login), message="You were logged out" )