from flask import request
from flask import Response
from flask import session

from website import Models
from website import app
from flask_cors import CORS, cross_origin
import re
import json


@app.route('/api/logout', methods=['POST'])
def logout():
    if 'email' in session:
        session.clear()
        return "logged out"
    return "not logged in"


@app.route('/api/account', methods=['POST'])
def createAccount():
    request.form["username"]
    try:
        s = json.dumps(request.form)
        with open('account.json', 'w') as f:
            f.write(s)
            f.close
        return "Success!", 200
    except Exception as e:
        return "Failure!", 400


@app.route('/api/login', methods=['POST'])
def login_user():
    username = request.form['username']
    password = request.form['password']
    if (username == "test" and password == "test"):
        session['username'] = username
        return "Success", 200
    return "Failure", 400


@app.route('/api/account', methods=['GET'])
def getAccount():
    username = session['username']
    # is username in dabatase
    # if it is, return the json with 200 code
    # else return 400 error