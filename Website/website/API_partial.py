from flask import request
from flask import Response
from flask import session
from website import Models
from website.models.account import Account
from website.models.account import Address
from website import app
from flask_cors import CORS, cross_origin
import json
import website.DAO.accountDAO as accountDAO
import website.DAO.addressDAO as addressDAO
import website.DAO.productDAO as productDAO
from website.Database import Database

@app.route('/api/account', methods=['GET'])
def getAccount():
    session['username'] = "Bryan-Turbo"
    try:
        sessionUsername = session['username']
        completeAccount = accountDAO.Find(sessionUsername)
    except:
        jsonResult = json.dumps({})
        return Response(jsonResult, mimetype="application/json")

    jsonResult = json.dumps(completeAccount, sort_keys=True, indent=4)
    return Response(jsonResult, mimetype="application/json") 

@app.route('/api/login', methods=['POST'])
def loginAccount():
    username = request.form['username']
    password = request.form['password']

    try:
        account = accountDAO.Find(username)
    except:
        return "Invalid Username", 400

    if(not password == account['password']):
        return "Invalid password", 400
    
    session['username'] = username