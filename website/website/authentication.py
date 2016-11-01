from flask import request
from flask import Response
from flask import session

from website import Models
from website import app
from flask_cors import CORS, cross_origin
import re

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
    email_regex = re.compile("(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
    if (not email_regex.match(email)):
        return "invalid email", 400
    
    # create new user


    # persist user to db
    # if valid return valid
    return "Successful", 200

@app.route('/API/Logout', methods=['POST'])
def logout():
    if 'email' in session:
        session.clear()
        return "logged out"
    return "not logged in"