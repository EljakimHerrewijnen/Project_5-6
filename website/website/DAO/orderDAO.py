from website.Database import Database
import website.DAO.productDAO as productDAO
from datetime import date

def Create(username, order_content):
    db = Database()
    order = {
        "username" : username,
        "order-date" : date.today().isoformat(),
        "postal_code" : order_content["address"]["postal_code"],
        "house_number" : order_content["address"]["house_number"]
    }
    order_id = db.insert("orders", order)

    for order_line in order_content["items"]:
        order_details = {
            "order_id" : order_id,
            "quanity" : order_line["quantity"]
        }
        db.insert("order_details", order_detail)


def Delete():
    pass


def Find(order_id):
    db = Database()
    db.where("orders_id", order_id)
    sqlResult = db.get_one("orders")
    sqlResult["products"] = productDAO.FindByOrder(sqlResult["order_id"])
    return sqlResult


def FindAll():
    db = Database()
    orders = db.get_all("orders")
    for order in orders:
        order["products"] = productDAO.FindByOrder(order["order_id"])
    return orders


def FindByUser(username):
    db = Database()
    db.where("username", username)
    orders = db.get_all("orders")
    for order in orders:
        order["products"] = productDAO.FindByOrder(order["order_id"])
    return orders