import unittest
from app.api.DAO import adminDAO

class TestMethods(unittest.TestCase):
    def setUp(self):
        self.adminDAO = adminDAO
        self.Date = "1996-03-07"
        self.WrongJsonObject = {
            "username": "LolLerz",
            "name": "Lol",
            "surname": "Lerz",
            "banned": 0,
            "email": "Lol@Lerz.com",
            "birth_date": self.Date,
            "register_date": "2000-11-25",
            "orders": {},
            "wishList": {},
            "favorites": {},
            "account_type": "normal",
            "wishlist_public": 0,
            "password": "Lullerz"
        }

        self.CorrectDate = {
            "year": '1996',
            "month": '03',
            "day": '07'
        }

        self.CorrectJsonObject = {
            "username": "LolLerz",
            "name": "Lol",
            "surname": "Lerz",
            "banned": 0,
            "email": "Lol@Lerz.com",
            "birthDate": self.CorrectDate,
            "registerDate": {"year": '2000', "month": '11', "day": '25'},
            "orders": {},
            "wishlist": {},
            "favorites": {},
            "accountType": "normal",
            "wishlistPublic": 0,
            "password": "Lullerz"
        }


    def test_date_conversion(self):
        newDate = self.adminDAO.ConvertDateToObject(self.Date)
        self.assertEqual(newDate, self.CorrectDate)

    def test_json_conversion(self):
        newJson = self.adminDAO.ToJsonObject(self.WrongJsonObject)
        self.assertEqual(newJson, self.CorrectJsonObject)


    def TestAdmin(self):
        if not(self.testDateConversion()):
            return False
        if not(self.testJsonConversion()):
            return False
        return True
