import unittest
from app.api.database import Database
from app.api.DAO import *
import os

class TestMethods(unittest.TestCase):
    # create database to test with
    @classmethod
    def setUpClass(self):
        self.testDBFileLocation = "app/test_db.db"
        self.db = Database(self.testDBFileLocation)
        self.db.reset_database()

    # delete test database to prevent errors
    @classmethod
    def tearDownClass(self):
        os.remove(self.testDBFileLocation)

    # actual tests
    # get all products
    def test_get_all(self):
        self.assertIsInstance(self.db.get_all("product"), list)


    # get one specific product
    def test_get_one(self):
        expectedResult = {
            "product_id": 1,
            "name": "Olympia Coffee Roasting - El Salvador Ricardo Ariz - Pacamara",
            "description": "This single origin is the product of a close relationship between Olympia Coffee and the grower, Ricardo Ariz. Over the years both have worked together to continue improving everything from the coffee cherries themselves to how the harvested cherries are processed. This varietal in particular takes a lot of extra attention and care, making it also more expensive. For Ricardo, it's all worth it because, put simply, 'It makes an awesome cup'. Enjoy this delicious coffee with us as we continue to follow along on this amazing process.",
            "price": 19.00,
            "roast_level": "Medium",
            "origin": "Americas"
        }
        self.db.where("name", "Olympia Coffee Roasting - El Salvador Ricardo Ariz - Pacamara")
        self.assertDictEqual(self.db.get_one("product"), expectedResult)

    # insert new user
    def test_insert_update_delete(self):
        # insert
        userDict = {"username": "testuser", "password": "testpasword", "name":"test", "surname":"user", "birth_date":"2017-01-23", "email":"test@email.com", "banned":0, "register_date":"2017-01-23", "account_type":"admin", "wishlist_public":1}
        self.assertEqual(self.db.insert("account", userDict), 1)
        self.assertDictEqual(self.db.get_one("account"), userDict)
        # update
        self.db.where("username", "testuser")
        userDict['banned'] = 1
        self.assertEqual(self.db.update("account", {"banned" : 1}), 1)
        self.assertDictEqual(self.db.get_one("account"), userDict)
        # delete
        self.db.where("username", "testuser")
        self.assertEqual(self.db.delete("account"), 1)
        self.assertDictEqual(self.db.get_one("account"), {})


# run tests
if __name__ == '__main__':
    unittest.main()
