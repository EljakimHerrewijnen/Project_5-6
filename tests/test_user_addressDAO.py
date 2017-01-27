import os
import unittest
from app.api.DAO.user_addressDAO import Create, Delete
from app.api.database import Database

class TestUserAddress(unittest.TestCase):
    def test_create(self):
        create = Create("0999AZ", 109, "test_user_address")
        result = 10
        self.assertEqual(create, result)

    def test_delete(self):
        delete = Delete("0999AZ", 109, "test_user_address")
        result = 1
        self.assertEqual(delete, result)