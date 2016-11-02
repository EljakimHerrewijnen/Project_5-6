from website.models.account import Account
from website.Database import Database
import website.DAO.addressDAO as addressDAO
from datetime import date

def Create(account):
    db = Database()
    account = _toSqlArgs(account)
    print(account)
    return db.insert("account", account)


def FindAll():
    db = Database()
    sqlAccounts = db.get_all("account")
    print(sqlAccounts)
    accounts = list(map(lambda account: _fromSqlResult(account), sqlAccounts))
    return accounts


# Result may be none
def Find(username):
    db = Database()
    db.where("username", username)

    user = db.get_all("account")
    if (user):
        return _fromSqlResult(user[0])
    else:
        return None


def Delete(account):
    db = Database()
    db.where("username", username)
    db.delete(account.username)


def Update(account):
    db = Database()
    db.where("username", account.username)
    account = _toSqlArgs(account)
    return db.update("account", account)


def _fromSqlResult(sqlFile):
    address = addressDAO.Find(sqlFile["postal_code"], sqlFile["house_number"])

    return Account(
        sqlFile["username"],
        sqlFile["password"],
        sqlFile["name"],
        sqlFile["surname"],
        sqlFile["email"],
        splitDate(sqlFile["birth_date"]),
        splitDate(sqlFile["register_date"]),
        sqlFile["banned"],
        sqlFile["account_type"],
        sqlFile["wishlist_public"],
        address
    )

def _toSqlArgs(account):
    # dictionary where keys correspond with table in the DB.
    return {
        "username"          : account.username,
        "password"          : account.password,
        "name"              : account.name,
        "surname"           : account.surname,
        "birth_date"        : account.birthDate.isoformat(),
        "email"             : account.email,
        "banned"            : int(account.banned),
        "register_date"     : account.registerDate.isoformat(),
        "account_type"      : account.accountType,
        "wishlist_public"   : int(account.wishListPublic), 
        "postal_code"       : account.address.postal_code,
        "house_number"      : account.address.house_number
    }


def splitDate(d):
    thing = d.split("-")
    return date(int(thing[2]), int(thing[1]), int(thing[2]))