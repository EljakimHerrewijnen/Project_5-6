from app.api.models.account import Account
from app.api.database import Database
from app.api.DAO import addressDAO
from app.api.DAO import wishDAO
from app.api.DAO import favoritesDAO
from app.api.DAO import orderDAO
from datetime import date
import json


def create(json):
    account = {
        "username" : json["username"],
        "name" : json['name'],
        "surname" : json['surname'],
        "password" : json['password'],
        "email" : json['email'],
        "birth_date" : date(json['birthDate']['year'], json['birthdate']['month'], json['birthdate']['day']).isoformat(),
        "register_date" : date.today().isoformat(),
        "banned" : 0,
        "wishlist_public" : 0,
        "account_type" : "user"
    }
    db.insert("account", account)

def format_from_db(db_dict):
    jsonRet = {
        "username" : db_dict['username'],
        'name' : db_dict['name'],
        'surname' : db_dict['surname'],
        'banned' : db_dict['banned'],
        'email' : db_dict['email'],
        'birthDate' :  ConvertDateToObject(db_dict['birth_date']),
        'registerDate' : ConvertDateToObject(db_dict['register_date']),
        'accountType' : db_dict['account_type'],
        'wishlistPublic' : db_dict['wishlist_public'],
        'password' : db_dict['password']
    }
    return jsonRet


# Create user
def Create(account):
    db = Database()
    d = account["birth_date"]
    birthDate = date(
        int(d["year"]),
        int(d["month"]),
        int(d["day"])
    ).isoformat()
    registrationDate = date.today().isoformat()
    account["birth_date"] = birthDate
    account["register_date"] = registrationDate
    account["banned"] = 0
    account["wishlist_public"] = 0
    account["account_type"] = "user"
    return db.insert("account", account)

# Get all users
def FindAll():
    db = Database()
    accounts = db.get_all("account")
    accounts = [format_from_db(account) for account in accounts]
    return accounts

# Get one user by username
def Find(username):
    db = Database()
    db.where("username", username)
    account = db.get_one("account")
    return format_from_db(account)

# Delete user
def Delete(username):
    db = Database()
    db.where("username", username)
    db.delete("username")

# update information in user
def Update(account):
    db = Database()
    db.update("account", account)

def ConvertDateToObject(dateString):
    date = {}
    tempDateObject = dateString.split("-")
    return {
        "year": tempDateObject[0],
        "month": tempDateObject[1],
        "day": tempDateObject[2]
    }
