from app.api.models.account import Account
from app.api.database import Database
from app.api.DAO import addressDAO
from app.api.DAO import wishDAO
from app.api.DAO import favoritesDAO
from app.api.DAO import orderDAO
from app.api.helpers import convert_json_to_iso
from datetime import date
import json


def create(json):
    db = Database()
    json["birth_date"] = convert_json_to_iso(json.pop('birthDate'))
    json["register_date"] = date.today().isoformat()
    json["banned"] = 0
    json["wishlist_public"] = 0
    json["account_type"] = "user"
    db.insert("account", json)


def convert_to_json(account):
    print(account)
    account['birthDate'] = ConvertDateToObject(account.pop('birth_date'))
    account['registerDate'] = ConvertDateToObject(account.pop('register_date'))
    account['accountType'] = account.pop("account_type")
    account['wishlistPublic'] = account.pop("wishlist_public")
    account['password'] = account.pop("password")
    return account


def Create(account):
    db = Database()
    account = create(account)


def FindAll():
    db = Database()
    accounts = db.get_all("account")
    accounts = [convert_to_json(account) for account in accounts]
    return accounts


def Find(username):
    db = Database()
    db.where("username", username)
    account = db.get_one("account")
    return convert_to_json(account)


def Delete(username):
    db = Database()
    db.where("username", username)
    db.delete("username")


# Update has all optional arguments!
def Update(account):
    db = Database()
    if "accountType" in account: 
        account['account_type'] = account.pop('accountType')
    if "birthDate" in account:
        account['birth_date'] = convert_json_to_iso(account.pop('birthDate'))
    if "registerDate" in account:
        account['register_date'] = convert_json_to_iso(account.pop('registerDate'))
    if "wishlistPublic" in account:
        account['wishlist_public'] = account.pop('wishlistPublic')
    db.where("username", account['username'])
    db.update("account", account)

def ConvertDateToObject(dateString):
    tempDateObject = dateString.split("-")
    return {
        "year": tempDateObject[0],
        "month": tempDateObject[1],
        "day": tempDateObject[2]
    }
