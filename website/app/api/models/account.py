from app.api.models.address import Address
from datetime import date
import sys
import json

class Account:
    def __init__(self, username, name = None, surname = None, password = None, email = None, birthDate = None, registerDate = None, banned = None, accountType = None, wishListPublic = None):
        self.username = username
        self.name = name
        self.surname = surname
        self.password = password
        self.email = email
        self.birthDate = birthDate
        self.registerDate = registerDate
        self.banned = banned
        self.accountType = accountType
        self.wishListPublic = wishListPublic
        self.address = address

    def toDict(self):
        return {
            "username"      : self.username,
            "name"          : self.name,
            "surname"       : self.surname,
            "email"         : self.email,
            "birthDate"     : dateToDict(self.birthDate),
            "banned"        : self.banned,
            "registerDate"  : dateToDict(self.registerDate),
            "wishlist"      : [],
            "orders"        : [],
            "favorites"     : [],
            "accountType"   : self.accountType,
            "wishListPublic": self.wishListPublic,
            "address"       : self.address.toDict()
        }


    def toJson(self):
        return json.dumps(self.toDict())


    @staticmethod
    def fromPost(json):
        account = Account(json["username"])
        account.name = json['name']
        account.surname = json['surname']
        account.password = json['password']
        account.email = json['email']
        account.birthDate = date(json['birthDate']['year'], json['birthdate']['month'], json['birthdate']['day'])
        account.registerDate = date.today()
        account.wishListPublic = False

    def fromUpdate(json)


    def fromForm(form):
        account_dict = {}
        for key in form:
            account_dict[key] = form[key]

        address = Address(
            form["postal_code"],
            int(form["number"]),
            form["country"],
            form["city"],
        ).toDict()

        account_dict["address"] = address
        account_dict["accountType"] = "user"
        account_dict["banned"] = False
        account_dict["birthDate"] = form
        account_dict["wishListPublic"] = False
        return Account.fromDict(account_dict)


def dateToDict(d):
    return {
        "year"  : d.year,
        "month" : d.month,
        "day"   : d.day
    }

def dateFromDict(d):
    return date(
        int(d["year"]),
        int(d["month"]),
        int(d["day"])
    )