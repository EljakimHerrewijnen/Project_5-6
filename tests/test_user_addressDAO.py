import os
import unittest
from app.api.DAO.user_addressDAO import Create, Delete
from app.api.database import Database

class TestUserAddress(unittest.TestCase):    
    # def test_create(self):
    #     db = Database()
    #     Setup.create()
    #     result = db.get_one_querry("SELECT * FROM user_address WHERE username='useraddresstest'")        
    #     self.assertEqual({'postal_code': '1234AB', 'house_number': 1, 'username': 'useraddresstest'}, result)

    # def test_delete(self):
    #     db = Database()
    #     Setup.delete()
    #     result = db.raw_get_one_querry("SELECT * FROM user_address WHERE username='useraddresstest'")        
    #     self.assertEqual({'house_number': 1, 'postal_code': '1234AB', 'username': 'useraddresstest'}, result)

    # def test_create(self):
    #     create = Create("4321BA", 1, "testuser2")
    #     result = "{}"
    #     self.assertEqual(create, result)

    def test_test(self):
        self.assertEqual(1,1)

if __name__ == '__main__':
    unittest.main()