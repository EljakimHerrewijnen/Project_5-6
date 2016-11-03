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


def Find(postal_code, street_number):
    db = Database()
    db.where("postal_code", postal_code)
    db.where("house_number", street_number)

    address = db.get_all("address")
    return addres[0]


def FindByUser(username):
    db = Database()
    db.join("Address a", "a.postal_code = p.postal_code AND a.house_number = p.house_number")
    db.where("username", username)
    return db.get_all("player_address p", "a.*")