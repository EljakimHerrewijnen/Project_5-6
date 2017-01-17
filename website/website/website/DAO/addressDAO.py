from website.models.address import Address
from website.Database import Database

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
    return address

# get addresses by user
def FindByUser(username):
    db = Database()
    db.join("Address a", "a.postal_code = p.postal_code AND a.house_number = p.house_number")
    db.where("username", username)
    return db.get_all("user_address p", "a.*")