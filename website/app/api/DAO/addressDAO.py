from app.api.models.address import Address
from app.api.database import Database

# Create adress
def Create(address):
    db = Database()
    return db.insert("address", address)

# Delete address
def Delete(address):
    db = Database()
    db.where("postal_code", address.postal_code)
    db.where("house_number", street_number)
    return db.delete("address")

# Get address
def Find(postal_code, street_number):
    db = Database()
    db.where("postal_code", postal_code)
    db.where("house_number", street_number)

    address = db.get_one("address")
    return ToJsonObject(address)

# get addresses by user
def FindByUser(username):
    db = Database()
    db.join("Address a", "a.postal_code = p.postal_code AND a.house_number = p.house_number")
    db.where("username", username)
    return ToJsonList(db.get_all("user_address p", "a.*"))

def ToJsonList(databaseList):
    jsonRet = []

    for address in databaseList:
        jsonRet.append(ToJsonObject(address))

    return jsonRet

def ToJsonObject(databaseObject):
    jsonRet = {}

    jsonRet["country"] = databaseObject["country"]
    jsonRet["city"] = databaseObject["city"]
    jsonRet["street"] = databaseObject["street"]
    jsonRet["postalCode"] = databaseObject["postal_code"]
    jsonRet["houseNumber"] = databaseObject["house_number"]

    return jsonRet
