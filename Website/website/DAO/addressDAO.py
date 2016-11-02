from website.models.address import Address
from website.Database import Database

def Create(address):
    db = Database()
    address = _toSqlArgs(address)
    return db.insert("address", address)


def Delete(address):
    db = Database()
    db.where("postal_code", address.postal_code)
    db.where("house_number", street_number)
    return db.delete("address")


def Update(address):
    db = Database()
    db.where("postal_code", address.postal_code)
    db.where("house_number", street_number)
    address = _toSqlArgs(address)
    return db.update("account", address)


def Find(postal_code, street_number):
    db = Database()
    db.where("postal_code", postal_code)
    db.where("house_number", street_number)

    address = db.get_all("address")
    if (address):
        return _fromSqlResult(address[0])
    else:
        return None


def _fromSqlResult(sqlResult):
    print(sqlResult)
    return Address(
        sqlResult["postal_code"],
        sqlResult["house_number"],
        sqlResult["country"],
        sqlResult["city"],
    )


def _toSqlArgs(address):
    return {
        "postal_code"   : address.postal_code,
        "house_number"  : address.house_number,
        "country"       : address.country,
        "city"          : address.city
    }