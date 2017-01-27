from app.api.DAO import adminDAO

class AdminDAOTest():
    def __init__(self):
        self.AdminDAO = adminDAO
        self.Date = ""
        self.WrongJsonObject = None

        self.CorrectDate = {}
        self.CorrectJsonObject = {}

    def setUp(self):
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
            "wishlist": {},
            "favorites": {},
            "account_type": "normal",
            "wishlist_public": 0,
            "password": "Lullerz"
        }

        self.CorrectDate = {
            "year": 1996,
            "month": 7,
            "day": 3
        }

        self.CorrectJsonObject = {
            "username": "LolLerz",
            "name": "Lol",
            "surname": "Lerz",
            "banned": 0,
            "email": "Lol@Lerz.com",
            "birthDate": self.CorrectDate,
            "registerDate": {"year": 2000, "month": 11, "day": 25},
            "orders": {},
            "wishlist": {},
            "favorites": {},
            "accountType": "normal",
            "wishlistPublic": 0,
            "password": "Lullerz"
        }

    def testDateConversion(self):
        newDate = self.AdminDAO.ConvertDateToObject(self.Date)
        if(newDate == self.CorrectDate):
            return True
        return False


    def testJsonConversion(self):
        newJson = self.AdminDAO.ToJsonObject(self.WrongJsonObject)
        if(newJson == self.CorrectJsonObject):
            return True
        return False
