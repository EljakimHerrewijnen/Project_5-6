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


