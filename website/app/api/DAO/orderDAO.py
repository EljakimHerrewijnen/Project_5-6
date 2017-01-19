from app.api.database import Database
from app.api.DAO import productDAO
from datetime import date
import sqlite3

# Create order
def Create(username, orderContent):
    db = Database()
    order = {
        "username" : username,
        "orders_date" : date.today().isoformat(),
        "postal_code" : orderContent["address"]["postal_code"],
        "house_number" : orderContent["address"]["house_number"]
    }
    orderId = db.insert("orders", order)
    if type(orderId) == sqlite3.Error:
        return orderId
    for orderLine in orderContent["items"]:
        orderDetails = {
            "orders_id" : orderId,
            "product_id" : orderLine["id"],
            "quantity" : orderLine["amount"]
        }
        res = db.insert("orderDetails", orderDetails)
        if type(res) == sqlite3.Error:
            db.reset_querry()
            db.where("orders_id", orderId)
            db.delete("orders")
            return res

    return orderId

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