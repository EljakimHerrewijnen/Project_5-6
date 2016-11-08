from website.models.account import Account
from website.Database import Database
import website.DAO.productDAO as productDAO
import website.DAO.accountDAO as accountDAO
import website.DAO.orderDAO as orderDAO
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
    for account in accounts:
        GetFullProperties(account)
    return accounts

# Get one admin by username
def Find(username):
    db = Database()
    db.where("username", username)
    db.where("account_type", "admin")
    account = db.get_one("account")
    if not account:
        return {}
    GetFullProperties(account)
    return account

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

def GetAllInformation():
    orders = orderDAO.FindAll()
    accounts = accountDAO.FindAll()
    product = productDAO.FindAll()

def ToggleUserBan(username):
    account = accountDAO.Find(username)
    if(account["banned"] == 0):
        account["banned"] = 1
    else:
        account["banned"] = 0
    
def RemoveUser(username):
    accountDAO.Delete(username)]

