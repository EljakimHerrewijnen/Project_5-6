from app.api.models.account import Account
from app.api.database import Database
from app.api.DAO import productDAO
from app.api.DAO import accountDAO
from app.api.DAO import orderDAO
from datetime import date

global orders
global accounts
global products

# Create admin
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
    account["account_type"] = "admin"
    return db.insert("account", account)

# Get all admins
def FindAll():
    db = Database()
    db.where("account_type", "admin")
    accounts = db.get_all("account")
    retAccounts = []
    for account in accounts:
        GetFullProperties(account)
        retAccount.append(ToJsonObject(account))
    return retAccounts

# Get one admin by username
def Find(username):
    db = Database()
    db.where("username", username)
    db.where("account_type", "admin")
    account = db.get_one("account")
    if not account:
        return {}
    GetFullProperties(account)
    return ToJsonObject(account)

# Delete admin
def Delete(username):
    db = Database()
    db.where("username", username)
    db.delete("username")

# update information in admin
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
    db.update("account", account)

# Add user specific wishlist, order, favorites and adress information to given Account
def GetFullProperties(account):
    username = account["username"]
    account["wishList"] = wishDAO.FindByUser(username)
    account["orders"] = orderDAO.FindByUser(username)
    account["favorites"] = favoritesDAO.FindByUser(username)
    account["addresses"] = addressDAO.FindByUser(username)

def GetAllOrders():
    orders = orderDAO.FindAllByMonth()
    return orders

def GetAllAccounts():
    accounts = accountDAO.FindAll()
    return accounts

def GetAllProducts():
    products = productDAO.FindAll()
    return products

def ToggleUserBan(username):
    account = accountDAO.Find(username)
    db = Database()
    if(account["banned"] == 0):
        # account["banned"] = 1
        db.where("username", username)
        db.update("account", {'banned': 1})
        # accountDAO.Update(account)
    else:
        # account["banned"] = 0
        db.where("username", username)
        db.update("account", {'banned': 0})
        # accountDAO.Update(account)
    print("Success")

def RemoveUser(username):
    accountDAO.Delete(username)

# Converts the object received from the database to the expected json format
def ToJsonObject(databaseAccount):
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
    jsonRet['password'] = databaseAccount['password']

    return databaseAccount

def ConvertDateToObject(dateString):
    date = {}
    tempDateObject = dateString.split("-")
    return {
        "year": tempDateObject[0],
        "month": tempDateObject[1],
        "day": tempDateObject[2]
    }
