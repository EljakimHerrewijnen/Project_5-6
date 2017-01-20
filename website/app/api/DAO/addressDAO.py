from app.api.models.address import Address
from app.api.database import Database

def convert_to_json(db_dict):
    db_dict["postalCode"] = db_dict.pop("postal_code")
    db_dict["houseNumber"] = db_dict.pop("house_number")
    return db_dict


def convert_from_json(json):
    json["postal_code"] = json.pop("postalCode")
    json["house_number"] = json.pop("houseNumber")
    return json


def Create(address):
    db = Database()
    address = convert_from_json(address)
    return db.insert("address", address)


def Delete(address):
    db = Database()
    address = convert_from_json(address)
    db.where("postal_code", address.postal_code)
    db.where("house_number", street_number)
    return db.delete("address")


def Find(postal_code, street_number):
    db = Database()
    db.where("postal_code", postal_code)
    db.where("house_number", street_number)
    address = db.getOne("address")
    if address:
        address = convert_to_json(address)
    return address


def FindByUser(username):
    db = Database()
    db.join("Address a", "a.postal_code = p.postal_code AND a.house_number = p.house_number")
    db.where("username", username)
    addresses = db.getAll("user_address p", "a.*")
    addresses = [convert_to_json(address) for address in addresses]
    return addresses