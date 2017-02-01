import json
from flask import request, Response, session, render_template
from flask_cors import CORS, cross_origin
from app.api import api
from app.api.DAO import *
from app.api.auth import secure
from app.api.database import Database
from itsdangerous import URLSafeTimedSerializer
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import datetime
import time
import pdfkit
import sys
from functools import reduce
import threading
ts = URLSafeTimedSerializer("SECRET KEY FOR ENCRYPTING THE EMAIL")

"""
PRODUCTS
"""

@api.route("/products")
def products():
    json_result = json.dumps(productDAO.FindAll(), sort_keys=True, indent=4)
    return Response(json_result, mimetype="application/json")

@api.route("/products/<id>")
def product(id):
    product = productDAO.Find(id)
    product = json.dumps(product, sort_keys=True, indent=4)
    return Response(product, mimetype='application/json')

"""
AUTHENTICATION
"""

@api.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return "logged out", 200

@api.route('/login', methods=['POST'])
def login_account():
    post_data = request.get_json()
    print(post_data)
    username = post_data['username']
    password = post_data['password']
    account = accountDAO.Find(username)
    if not account:
        return "Account not found", 404
    if password != account['password']:
        return "Invalid password", 403
    if account['banned'] == 1:
        return "User Banned", 403
    session['username'] = username
    return "Success", 200

"""
ACCOUNT
"""

@api.route('/account', methods=['POST'])
def create_account():
    try:
        result = accountDAO.Create(request.get_json())
        return "success", 200
    except Exception as e:
        return str(sys.exc_info()), 500

@api.route('/account', methods=['GET'])
@secure()
def get_account(account):
    account['wishlist'] = wishDAO.FindByUser(account['username'])
    account['favorites'] = favoritesDAO.FindByUser(account['username'])
    account['orders'] = orderDAO.FindByUser(account['username'])
    account['addresses'] = addressDAO.FindByUser(account['username'])
    json_result = json.dumps(account)
    return Response(json_result, mimetype="application/json")

@api.route('/account', methods=['PUT'])
@secure()
def update_account(account):
    post_data = request.get_json()
    post_data['username'] = account['username']
    result = accountDAO.Update(post_data)
    return "Success", 200

@api.route('/account/address', methods=['POST'])
@secure()
def add_address(account):
    post_data = request.get_json()
    postal_code = post_data["postalCode"]
    house_number = post_data["houseNumber"]
    address = addressDAO.Find(postal_code, house_number)

    # address does not exist: create address
    if not address:
        addressDAO.Create(post_data)
    result = user_addressDAO.Create(postal_code, house_number, account['username'])
    return "success", 200

@api.route('/account/address', methods=['GET'])
@secure()
def get_address(account):
    result = addressDAO.FindByUser(account['username'])
    return Response(json.dumps(result), 200, mimetype='application/json', )

@api.route('/account/address', methods=['DELETE'])
@secure()
def delete_address(account):
    post_data = request.get_json()
    postal_code = post_data["postalCode"]
    house_number = post_data["houseNumber"]
    result = user_addressDAO.Delete(postal_code, house_number, account['username'])
    return "Success!", 200

@api.route('/account/favorites', methods=['POST'])
@secure()
def add_favorite(account):
    post_data = request.get_json()
    productId = post_data["id"]
    product = productDAO.Find(productId)
    if not product:
        return "Product does not exist", 404
    result = favoritesDAO.Create(account['username'], productId)
    return "Success!", 200

@api.route('/account/favorites', methods=['GET'])
@secure()
def get_favorite(account):
    result = favoritesDAO.FindByUser(account['username'])
    return Response(json.dumps(result), 200, mimetype='application/json')

@api.route('/account/favorites', methods=['DELETE'])
@secure()
def delete_favorite(account):
    productId = request.get_json()
    productId = productId["id"]
    result = favoritesDAO.Delete(account['username'], productId)
    return "Success", 200

@api.route('/account/wishlist', methods=['POST'])
@secure()
def add_wishlist(account):
    postData = request.get_json()
    productId = postData["id"]
    product = productDAO.Find(productId)
    if (not product):
        return "Product does not exist", 404
    result = wishDAO.Create(account['username'], productId)
    return "Success!", 200

@api.route('/account/wishlist', methods=['GET'])
@secure()
def get_wishlist(account):
    result = wishDAO.FindByUser(account['username'])
    return Response(json.dumps(result), 200, mimetype='application/json')

@api.route('/account/wishlist', methods=['DELETE'])
@secure()
def delete_wishlist(account):
    productId = request.get_json()
    productId = productId["id"]
    result = wishDAO.Delete(account['username'], productId)
    return "Success", 200

@api.route('/account/order', methods=['POST'])
@secure()
def add_order(account):
    postData = request.get_json()
    order = orderDAO.Create(account['username'], postData)
    send_order_mail(account, order)
    return Response(json.dumps(order), 200, mimetype='application/json')

@api.route('/account/order', methods=['GET'])
@secure()
def get_orders(account):
    orders = orderDAO.FindByUser(account['username'])
    response = Response(json.dumps(orders), 200, mimetype='application/json')
    return response

@api.route('/account/order/<order_id>')
@secure()
def get_order(account, order_id):
    print(order_id)
    order = orderDAO.Find(order_id)
    if (order['username'] == account['username']):
        return Response(json.dumps(order), 200, mimetype='application/json', )
    return "Unauthorized", 401

"""
PUBLIC WISH LISTS
"""

@api.route('/wishlist')
def get_public_wishlists():
    db = Database()
    db.where("wishlist_public", 1)
    accounts = db.get_all("account", select = "username, name")
    json_result = json.dumps(accounts, sort_keys=True, indent=4)
    return Response(json_result, mimetype="application/json")

@api.route('/wishlist/<username>')
def get_public_wishlist(username):
    db = Database()
    account = accountDAO.Find(username)
    print(account)
    if account['wishlistPublic']:
        response = {
            "wishlist" : wishDAO.FindByUser(username),
            "name" : account["name"],
            "surname" : account['surname']
        }
        json_result = json.dumps(response, sort_keys=True, indent=4)
        return Response(json_result, mimetype='application/json')
    else:
        return "Unauthorized", 401

@api.route('/admin/ban/<username>', methods = ['POST'])
def BanUser(username):
    adminDAO.ToggleUserBan(username)
    return "Success", 200

@api.route('/request-password-reset', methods=['POST'])
def get_password_reset_token():
    postData = request.get_json()
    db = Database()
    db.where("email", postData['email'])
    try:
        user = db.get_one("account")
        if not user:
            return "Could not find user associated with email", 500
        key = user['username'] + "_" + str(time.time())
        key = ts.dumps(key, salt='email-confirm-key')
        from_address = "noreply@coffeesupre.me"
        to_addresss = postData['email']

        msg = MIMEMultipart("alternative")
        msg['Subject'] = 'Coffeesupreme password reset'
        msg['From'] = from_address
        msg['To'] = to_addresss

        text_version = render_template("password-reset.txt", hash=key, user = {"name" : user['name'], "surname" : user['surname']})
        html_version = render_template("password-reset.html", hash=key, user = {"name" : user['name'], "surname" : user['surname']})

        part1 = MIMEText(text_version, "text")
        part2 = MIMEText(html_version, "html")

        msg.attach(part1)
        msg.attach(part2)

        server = smtplib.SMTP_SSL("mail.privateemail.com", 465)
        server.login("noreply@coffeesupre.me", "password")
        server.sendmail(from_address, to_addresss, msg.as_string())
        server.quit()
        return "success", 200
    except Exception as e:
        return str(sys.exc_info()), 500

@api.route('/password-reset', methods=['POST'])
def reset_password():
    postData = request.get_json()
    key = postData['hash']
    try:
        key = ts.loads(key, salt="email-confirm-key", max_age=86400)
        username, date = key.split('_')
        date = datetime.datetime.fromtimestamp(float(date))
        if (date - datetime.datetime.now()).total_seconds () > 1800:
            return "Password reset expired", 500
        accountDAO.Find(username);
        password = postData['password']
        accountDAO.Update({"password" : password, "username" : username})
        return "Success", 200
    except:
        return "Could not update user, are you sure it exists?", 500


def send_order_mail(account, order):
    order_total = reduce(lambda x, y: x + y['quantity'] * y['product']['price'], order['products'], 0)
    string = render_template("order-pdf.html", order = order, account=account, order_total=order_total)
    text_version = render_template("invoice-email.txt", user = account, order=order)
    html_version = render_template("invoice-email.html", user = account, order=order)
    
    def send_mail(string, text_versiom, html_version):
        options = {
            'page-size' : 'a5',
            'margin-top' : '0in',
            'margin-left' : '0in',
            'margin-right' : '0in',
            'margin-bottom' : '0in',
            'encoding': "UTF-8",
            'zoom': 1.5,
            'no-outline': None,
            'disable-smart-shrinking' : None,
        }
        pdf = pdfkit.from_string(string, False, options=options)
        from_address = "noreply@coffeesupre.me"
        to_addresss = "bartrijnders14@gmail.com"
        msg = MIMEMultipart("mixed")
        msg['Subject'] = 'Coffeesupreme order ' + str(order['id'])
        msg['From'] = from_address
        msg['To'] = to_addresss

        pdfAttachment = MIMEApplication(pdf, _subtype = "pdf")
        pdfAttachment.add_header('content-disposition', 'attachment', filename = ('utf-8', '', 'invoice_' + str(order['id']) +'.pdf'))
        part1 = MIMEText(text_version, "text")
        part2 = MIMEText(html_version, "html")

        print("dix")
        sys.stderr.write("dix")
        sys.stdout.write("dix")
        msg.attach(part2)
        msg.attach(pdfAttachment)
        server = smtplib.SMTP_SSL("mail.privateemail.com", 465)
        server.login("noreply@coffeesupre.me", "password")
        server.sendmail(from_address, to_addresss, msg.as_string())
        server.quit()

    threading.Thread(target=send_mail, args=(string, text_version, html_version)).start()