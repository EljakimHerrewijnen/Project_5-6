import unittest
from app.api.database import Database
from app.api.DAO import *
import os
class TestMethods(unittest.TestCase):
    #setup
    def setUpClass(self):
        self.db = Database()

        #Creating user
        accountjson = {
            "username" : "testuser",
            "password" : "testuser",
            "surname"  : "testuser",
            "birthDate": {"year":1990, "month":12, "day":12},
            "email": "testuser@coffeesupre.me",
            "banned": 0,
            "account_type": 0,
        }
        accountDAO.Create(accountjson)

    def TearDownClass(self):
        accountDAO.Delete("testuser")

        #self.address = {'houseNumber': 3, 'postalCode': '9999AA', 'country': 'Neverland', 'street': 'kikkerveen', 'city': 'Spijk'}

    # actual tests
    # create, find and delete an address
    # added all three functions to the same method to prevent issues with deleting the record before looking it up ect.
    def test_Create_Find_Delete(self):
        self.assertIsInstance(accountDAO.Find("testuser"), list)

# run tests
if __name__ == '__main__':
    unittest.main() 