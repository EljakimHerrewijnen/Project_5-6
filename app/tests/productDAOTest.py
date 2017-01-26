import unittest
from app.api.database import Database
from app.api.DAO import *
import os

class TestMethods(unittest.TestCase):
    # create database to test with
    # @classmethod
    # def setUpClass(self):
    #     self.testDBFileLocation = "app/test_db.db"
    #     self.db = Database(self.testDBFileLocation)
    #     self.db.reset_database()

    # delete test database to prevent errors
    # @classmethod
    # def tearDownClass(self):
    #     os.remove(self.testDBFileLocation)

    # actual tests
    # get a products
    def test_find(self):
        expectedResult = {
            "id": 1,
            "name": "Olympia Coffee Roasting - El Salvador Ricardo Ariz - Pacamara",
            "description": "This single origin is the product of a close relationship between Olympia Coffee and the grower, Ricardo Ariz. Over the years both have worked together to continue improving everything from the coffee cherries themselves to how the harvested cherries are processed. This varietal in particular takes a lot of extra attention and care, making it also more expensive. For Ricardo, it's all worth it because, put simply, 'It makes an awesome cup'. Enjoy this delicious coffee with us as we continue to follow along on this amazing process.",
            "price": 19.00,
            "roast": "Medium",
            "origin": "Americas",
            "aromas": ['Chocolate', "Nutty"]
        }
        self.assertIsInstance(productDAO.Find(1), dict)
        self.assertDictEqual(productDAO.Find(1), expectedResult, None)


    def test_FindAll(self):
        self.assertIsInstance(productDAO.FindAll(), list)

    def test_FindByOrder(self):
        self.assertIsInstance(productDAO.FindByOrder(1), list)

# run tests
if __name__ == '__main__':
    unittest.main()