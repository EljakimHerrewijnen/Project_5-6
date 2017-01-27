import unittest
from app.api.database import Database
from app.api.DAO import *
import os
class TestMethods(unittest.TestCase):
    #setup
    def SetUp(self):
        self.testDBFileLocation = "app/test_db.db"
        self.db = Database(self.testDBFileLocation)
        self.db.reset_database()
        accountDAO.Delete("testuser")

    def TearDown(self):
        os.remove(self.testDBFileLocation)
        accountDAO.Delete("testuser")

    #Testing Create in accountDAO
    def test_create(self):
        accountDAO.Delete("testuser")
        #Testing Update
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

    #Testing Update in accountDAO
    def test_update(self):
        accountjson = {
            "username" : "testuser",
            "password" : "testuser",
            "surname"  : "testuser",
            "birthDate": {"year":1990, "month":12, "day":12},
            "email": "testuser@coffeesupre.me",
            "banned": 0,
            "account_type": 0,
        }
        result = accountDAO.Update(accountjson)
        print(result)

    #Testing find in accountDAO
    def test_find(self):
        expectedresult = {
            'accountType': 'user',
            'banned': 0,
            'birthDate': {'day': '12', 'month': '12', 'year': '1990'},
            'email': 'testuser@coffeesupre.me',
            'name': None,
            'password': 'testuser',
            'registerDate': {'day': '27', 'month': '01', 'year': '2017'},
            'surname': 'testuser',
            'username': 'testuser',
            'wishlistPublic': 0
        }
        # Testing Finder
        self.assertDictEqual(accountDAO.Find("testuser"), expectedresult)
    
        #Testing find all
        self.assertIsInstance(accountDAO.FindAll(), list)

    # def test_delete(self):
    #     accountDAO.Delete("testuser")

# run tests
if __name__ == '__main__':
    unittest.main() 