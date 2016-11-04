from website.Database import Database

# Add adress to user
def Create(postal_code, house_number, username):
    db = Database()
    sql = {
        "postal_code" : postal_code,
        "house_number" : house_number,
        "username" : username
    }
    return db.insert("user_address", sql)

# Remove adress from user
def Delete(postal_code, house_number, username):
    db = Database()
    db.where("postal_code", postal_code)
    db.where("house_number", house_number)
    db.where("username", username)
    return db.delete("user_address")