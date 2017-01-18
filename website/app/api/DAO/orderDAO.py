from app.api.database import Database
from app.api.DAO import productDAO
from app.api.DAO import addressDAO
from app.api.helpers import date_convert
from datetime import date
import sqlite3

# Create order
def Create(username, order_content):
    db = Database()
    order = {
        "username" : username,
        "orders_date" : date.today().isoformat(),
        "postal_code" : order_content["address"]["postalCode"],
        "house_number" : order_content["address"]["houseNumber"]
    }
    order_id = db.insert("orders", order)
    for order_line in order_content["items"]:
        order_details = {
            "orders_id" : order_id,
            "product_id" : order_line["id"],
            "quantity" : order_line["amount"]
        }
        res = db.insert("order_details", order_details)
    return order_id

def Delete():
    pass

# Get order with products
def Find(order_id):
    db = Database()
    db.where("orders_id", order_id)
    sqlResult = db.get_one("orders")
    return toJsonFormat(sqlResult)

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

def toJsonFormat(order):
    return {
        "address" : addressDAO.Find(order['postal_code'], order['house_number']),
        "id" : order['orders_id'],
        "orderDate" : date_convert(order['orders_date']),
        "products" : productDAO.FindByOrder(order["orders_id"]),
        "username" : order['username']
    }