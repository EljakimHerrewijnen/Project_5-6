from flask import request
from flask import Response
from flask import session
from website import Models
from website import app
from flask_cors import CORS, cross_origin
import json


@app.route('/API/Login', methods=['POST'])
def login_user():
    email = request.form['email']
    password = request.form['password']
    if (email == "test" and password == "test"):
        session['email'] = email
        return "Success"
    return "Failure"

@app.route('/API/User', methods=['POST'])
def user():
    email = request.form['email']
    password = request.form['password']
    postal_code = request.form['postal_code']
    street_number = request.form['number']
    # validate user input
    # create new user
    # persist user to db
    # if valid return valid
    print("registered user")
    return ""

@app.route('/API/Logout', methods=['POST'])
def logout():
    if 'email' in session:
        session.clear()
        return "logged out"
    return "not logged in"