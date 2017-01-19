import json
from flask import request, Response, session
from flask_cors import CORS, cross_origin
from app.api import api
from app.api.DAO import *
from app.api.auth import secure
from app.api.database import Database


@api.route('/admin/account')
@secure(admin_only = True)
def get_all_accounts(account):
    accounts = accountDAO.FindAll()
    accounts = json.dumps(accounts, sort_keys=True, indent=4)
    return Response(accounts, mimetype='application/json')
