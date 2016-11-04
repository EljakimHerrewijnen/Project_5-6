from website.models.account import Account
from website.Database import Database
import website.DAO.addressDAO as addressDAO
import website.DAO.wishDAO as wishDAO
import website.DAO.favoritesDAO as favoritesDAO
import website.DAO.orderDAO as orderDAO
from datetime import date

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
    return db.insert("account", account)


def FindAll():
    db = Database()
    accounts = db.get_all("account")
    for account in accounts:
        GetFullProperties(account)
        
    return accounts

def Find(username):
    db = Database()
    db.where("username", username)
    account = db.get_one("account")
    GetFullProperties(account)
    return account


def Delete(username):
    db = Database()
    db.where("username", username)
    db.delete("username")


def Update(account):
    db = Database()
    d = account["birthDate"]
    birthDate = date(
        int(d["year"]),
        int(d["month"]),
        int(d["day"])
    ).isoformat()
    account["birthDate"] = birthDate

    db.update("account", account)


def GetFullProperties(account):
    username = account["username"]
    account["wishList"] = wishDAO.FindByUser(username)
    account["orders"] = orderDAO.FindByUser(username)
    account["favorites"] = favoritesDAO.FindByUser(username)
    account["addresses"] = addressDAO.FindByUser(username)