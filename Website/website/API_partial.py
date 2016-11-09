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
import website.DAO.adminDAO as AdminDAO
from website.Database import Database

@app.route("/api/test/1")
def test0():
    orders = AdminDAO.GetAllOrders()
    return Response(json.dumps(orders), mimetype="appliaction/json")

@app.route("/api/test/2")
def test1():
    accounts = AdminDAO.GetAllAccounts()
    return Response(json.dumps(accounts), mimetype="appliaction/json")

@app.route("/api/test/3")
def test2():
    products = AdminDAO.GetAllProducts()
    return Response(json.dumps(products), mimetype="appliaction/json")