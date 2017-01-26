from app.api.models.address import Address
from app.api.database import Database
import re

postal_code_pattern = re.compile("\d{4}[a-zA-Z]{2}")

def convert_to_json(db_dict):
    db_dict["postalCode"] = db_dict.pop("postal_code")
    db_dict["houseNumber"] = db_dict.pop("house_number")
    return db_dict


def convert_from_json(json):
    json["postal_code"] = json.pop("postalCode").upper()
    json["house_number"] = json.pop("houseNumber")
    return json

def verify_address(address):
    fields = ["postalCode", "houseNumber", "city", "street", "country"]
    print(address)
    for key in fields:
        if not key in address:
            raise KeyError("Address does not contain " + key)
        if not address[key]:
            raise ValueError(key + " cannot be empty.")
    #if type(address['houseNumber']) != int:
        #raise ValueError("House number is not an integer value.")
    if not re.match(address['postalCode']):
        raise ValueError("Postal code is of the incorrect format.");

def Create(address):
    db = Database()
    verify_address(address)
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
    address = db.get_one("address")
    if address:
        address = convert_to_json(address)
    return address


def FindByUser(username):
    db = Database()
    db.join("Address a", "a.postal_code = p.postal_code AND a.house_number = p.house_number")
    db.where("username", username)
    addresses = db.get_all("user_address p", "a.*")
    addresses = [convert_to_json(address) for address in addresses]
    return addresses