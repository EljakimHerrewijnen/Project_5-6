import unittest
from app.api.database import Database
from app.api.DAO import *

class TestMethods(unittest.TestCase):
    def setUp(self):   
        self.db = Database()

    # actual tests
    def test_get_all(self):
        self.assertIsInstance(self.db.get_all("product"), list)

    def test_get_one(self):
        self.assertIsInstance(self.db.get_one("product"), dict)

    
# Some examples
    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)
# End examples


# run tests
if __name__ == '__main__':
    unittest.main()