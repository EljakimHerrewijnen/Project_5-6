from flask import request, Response, session
from functools import wraps, partial
from app.api.DAO import accountDAO

def secure(admin_only = False):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not ('username' in session):
                return '403: UNAUTHORIZED BABY, NO SESSION', 401
            account = accountDAO.Find(session['username'])
            if not account:
                return '401: UNAUTHORIZED BABY, YOUR ACCOUNT DOES NOT EXIST', 401

            if admin_only and account['account_type'] != 'admin':
                return '401: UNAUTHORIZED BABY, YOUR ACCOUNT DOES NOT HAVE ADMIN PRIVILEGES', 401
            
            dix = partial(func, account)
            result = dix(*args, **kwargs)
            return result
        return wrapper
    return decorator


"""


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
        return e, 400

@app.route('/api/account', methods=['GET'])
def getAccount():
    try:
        username = "Arjen" 
        #session['username']
    except:
        return "failed", 400
    SQLaccount = Models.Account.find(username)
    if(SQLaccount == None):
        return "Failure!", 400
    
    account = Models.Account._fromSql(SQLaccount[0])
    # return "Succes!", 200

    # accounts = Models.Account._getAll()
    return Response(Models.Account.ToJson(account), mimetype="application/json")


@app.route('/api/login', methods=['POST'])
def login_user():
    username = request.form['username']
    password = request.form['password']
    if (username == "bart" and password == "bart"):
        session['username'] = username
        return "Success", 200
    return "Failure", 400
"""