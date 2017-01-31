import unittest
import time
from app.api.DAO import adminDAO
from app.api.models.account import Account
from app.api.database import Database

class TestAdminDAO(unittest.TestCase):
    def setUp(self):
        self.adminDAO = adminDAO
        self.day = time.strftime("%d")
        self.month = time.strftime("%m")
        self.year = time.strftime("%Y")
        self.CorrectDate = {
            "year": '1996',
            "month": '03',
            "day": '07'
        }

        self.account = {
            "username": "LolLerz",
            "name": "Lol",
            "surname": "Lerz",
            "password": "Lullerz",
            "email": "Lol@Lerz.com",
            "birth_date": self.CorrectDate,
            "account_type": "admin"
        }

        self.CorrectJsonObject = {
            "username": "LolLerz",
            "name": "Lol",
            "surname": "Lerz",
            "banned": 0,
            "email": "Lol@Lerz.com",
            "birthDate": self.CorrectDate,
            "registerDate": {"year": self.year, "month": self.month, "day": self.day},
            "orders": [],
            "wishlist": [],
            "favorites": [],
            "accountType": "admin",
            "wishlistPublic": 0,
            "password": "Lullerz"
        }

    def test_create(self):
        print(adminDAO.Find("LolLerz"))
        if(adminDAO.Find("LolLerz") != {}):
            adminDAO.Delete("LolLerz")
        self.assertIsInstance(self.adminDAO.Create(self.account), int)

    def test_date_conversion(self):
        WrongDate = "1996-03-07"
        newDate = self.adminDAO.ConvertDateToObject(WrongDate)
        self.assertEqual(newDate, self.CorrectDate)

    def test_json_conversion(self):
        admin = adminDAO.Find("LolLerz")
        self.assertEqual(admin, self.CorrectJsonObject)

    def test_user_ban(self):
        banned = adminDAO.Find("LolLerz")["banned"]
        adminDAO.ToggleUserBan("LolLerz")
        self.assertNotEqual(adminDAO.Find("LolLerz")["banned"], banned)
        adminDAO.ToggleUserBan("LolLerz")
        self.assertEqual(adminDAO.Find("LolLerz")["banned"], banned)

    def TearDown(self):
        adminDAO.Delete("LolLerz")
