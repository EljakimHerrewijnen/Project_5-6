import unittest
from app.api.database import Database
from app.api.DAO import *
import os

class TestMethods(unittest.TestCase):
    #setup
    def setUp(self):
        self.address = {'houseNumber': 3, 'postalCode': '9999AA', 'country': 'Neverland', 'street': 'kikkerveen', 'city': 'Spijk'}

    # actual tests
    # create, find and delete an address
    # added all three functions to the same method to prevent issues with deleting the record before looking it up ect.
    def test_Create_Find_Delete(self):
        self.assertIsInstance(addressDAO.Create(self.address), int)
        self.setUp()
        self.assertDictEqual(addressDAO.Find(self.address["postalCode"], self.address["houseNumber"]), self.address)
        self.setUp()
        self.assertIsInstance(addressDAO.Delete(self.address), int)

    def test_FindByUser(self):
        self.assertIsInstance(addressDAO.FindByUser('a'), list)

# run tests
if __name__ == '__main__':
    unittest.main()