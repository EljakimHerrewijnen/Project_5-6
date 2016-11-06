from website.models.account import Account
from website.Database import Database
import website.DAO.addressDAO as addressDAO
import website.DAO.wishDAO as wishDAO
import website.DAO.favoritesDAO as favoritesDAO
import website.DAO.orderDAO as orderDAO
from datetime import date

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
    return account

# Delete user
def Delete(username):
    db = Database()
    db.where("username", username)
    db.delete("username")

# update information in user
def Update(account):
    db = Database()
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