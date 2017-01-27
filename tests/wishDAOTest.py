import unittest
from app.api.database import Database
from app.api.DAO import *
import os

class TestMethods(unittest.TestCase):
    # actual tests
    def test_Create_Delete(self):
        self.assertIsInstance(wishDAO.Create("Leeroy Jenkins", 3), int)
        self.assertIsInstance(wishDAO.Delete("Leeroy Jenkins", 3), int)
        
    def test_FindAll(self):
        self.assertIsInstance(wishDAO.FindAll(), list)
    
    def test_FindByUser(self):
        self.assertIsInstance(wishDAO.FindByUser("Leeroy Jenkins"), list)

# run tests
if __name__ == '__main__':
    unittest.main()