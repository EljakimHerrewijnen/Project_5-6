from app.api.database import Database
from app.api.DAO import productDAO
from app.api.DAO import addressDAO
from app.api.helpers import convert_iso_to_json
from datetime import date
import sqlite3

def convert_to_json(order):
    order["address"] = addressDAO.Find(order.pop('postal_code'), order.pop("house_number"))
    order['id'] = order.pop('orders_id')
    order['orderDate'] = convert_iso_to_json(order.pop('orders_date'))
    order['products'] = productDAO.FindByOrder(order["id"])
    return order


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
            "quantity" : order_line["quantity"]
        }
        res = db.insert("order_details", order_details)
    return Find(order_id)


def Find(order_id):
    db = Database()
    db.where("orders_id", order_id)
    order = db.get_one("orders")
    convert_to_json(order)
    return order


def FindAll():
    db = Database()
    orders = db.get_all("orders")
    orders = [convert_to_json(order) for order in orders]
    return orders


def FindByUser(username):
    db = Database()
    db.where("username", username)
    orders = db.get_all("orders")
    orders = [convert_to_json(order) for order in orders]
    return orders


def FindAllByMonth():
    db = Database()
    db.order_by("orders_date")
    orders = db.get_all("orders")
    orders = [convert_to_json(order) for order in orders]
    return orders