from app.api.models.account import Account
from app.api.database import Database
from app.api.DAO import addressDAO
from app.api.DAO import wishDAO
from app.api.DAO import favoritesDAO
from app.api.DAO import orderDAO
from datetime import date
import json

# Create user
def Create(account):
    db = Database()
    d = account["birth_date"]
    print(d)
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
    for account in accounts:

        GetFullProperties(account)
    return accounts

# Get one user by username
def Find(username):
    db = Database()
    db.where("username", username)
    account = db.get_one("account")
    if not account:
        return {}
    GetFullProperties(account)
    return ToJsonObbject(account)

# Delete user
def Delete(username):
    db = Database()
    db.where("username", username)
    db.delete("username")

# update information in user
def Update(account):
    db = Database()
    if ("birth_date" in account):
        bd = account["birth_date"]
        birth_date = date(
            int(bd["year"]),
            int(bd["month"]),
            int(bd["day"])
        ).isoformat()
        account["birth_date"] = birth_date
    db.where("username", account["username"])
    print(json.dumps(account, indent=4, sort_keys=True))
    db.update("account", account)

# Add user specific wishlist, order, favorites and adress information to given Account
def GetFullProperties(account):
    username = account["username"]
    account["wishList"] = wishDAO.FindByUser(username)
    account["orders"] = orderDAO.FindByUser(username)
    account["favorites"] = favoritesDAO.FindByUser(username)
    account["addresses"] = addressDAO.FindByUser(username)

# Converts the object received from the database to the expected json format
def ToJsonObbject(databaseAccount):
    jsonRet = {}

    jsonRet['username'] = databaseAccount['username']
    jsonRet['name'] = databaseAccount['name']
    jsonRet['surname'] = databaseAccount['surname']
    jsonRet['banned'] = databaseAccount['banned']
    jsonRet['email'] = databaseAccount['email']
    jsonRet['birthDate'] = ConvertDateToObject(databaseAccount['birth_date'])
    jsonRet['registerDate'] = ConvertDateToObject(databaseAccount['register_date'])
    jsonRet['orders'] = databaseAccount['orders']
    jsonRet['wishlist'] = databaseAccount['wishList']
    jsonRet['favorites'] = databaseAccount['favorites']
    jsonRet['accountType'] = databaseAccount['account_type']
    jsonRet['wishlistPublic'] = databaseAccount['wishlist_public']

    return jsonRet

def ConvertDateToObject(dateString):
    date = {}
    tempDateObject = dateString.split("-")
    return {
        "year": tempDateObject[0],
        "month": tempDateObject[1],
        "day": tempDateObject[2]
    }
