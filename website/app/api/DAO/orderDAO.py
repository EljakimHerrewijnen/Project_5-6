from website.Database import Database
import website.DAO.productDAO as productDAO
from datetime import date
import sqlite3

# Create order
def Create(username, order_content):
    db = Database()
    order = {
        "username" : username,
        "orders_date" : date.today().isoformat(),
        "postal_code" : order_content["address"]["postal_code"],
        "house_number" : order_content["address"]["house_number"]
    }
    order_id = db.insert("orders", order)
    if type(order_id) == sqlite3.Error:
        return order_id
    for order_line in order_content["items"]:
        order_details = {
            "orders_id" : order_id,
            "product_id" : order_line["id"],
            "quantity" : order_line["amount"]
        }
        res = db.insert("order_details", order_details)
        if type(res) == sqlite3.Error:
            db.reset_querry()
            db.where("orders_id", order_id)
            db.delete("orders")
            return res

    return True

def Delete():
    pass

# Get order with products
def Find(order_id):
    db = Database()
    db.where("orders_id", order_id)
    sqlResult = db.get_one("orders")
    sqlResult["products"] = productDAO.FindByOrder(sqlResult["orders_id"])
    return sqlResult

# Get all orders
def FindAll():
    db = Database()
    orders = db.get_all("orders")
    for order in orders:
        order["products"] = productDAO.FindByOrder(order["orders_id"])
    return orders

# Get all orders for by user
def FindByUser(username):
    db = Database()
    db.where("username", username)
    orders = db.get_all("orders")

    for order in orders:
        order["products"] = productDAO.FindByOrder(order["orders_id"])
    return orders