import unittest
from app.api.database import Database
from app.api.DAO import *
import os

class TestOrderDAO(unittest.TestCase):
	# database connection
    @classmethod
    def setUpClass(self):
        self.db = Database()
        self.order = {'items': [{'quantity': 1, 'id': 1}], 'address': {'houseNumber': '1', 'postalCode': '9999AA'}}

    @classmethod
    def tearDownClass(self):
        # find test order id
        self.db.where("username", "Leeroy Jenkins")
        orderid = self.db.get_one("orders")
        # delete test order
        self.db.where("orders_id", orderid["orders_id"])
        self.db.delete("order_details"), 1
        self.db.where("username", "Leeroy Jenkins")
        self.db.delete("orders")

    # actual tests
    def test_Create(self):
        # create new order
        self.assertIsInstance(orderDAO.Create("Leeroy Jenkins", self.order), dict)

    def test_Find(self):
        # set up for test
        self.db.where("username", "Leeroy Jenkins")
        orderid = self.db.get_one("orders")
        # test
        self.assertIsInstance(orderDAO.Find(orderid["orders_id"]), dict)
    
    def test_FindAll(self):
        self.assertIsInstance(orderDAO.FindAll(), list)

    def test_FindByUser(self):
        self.assertIsInstance(orderDAO.FindByUser("Leeroy Jenkins"), list)

# run tests
if __name__ == '__main__':
    unittest.main()