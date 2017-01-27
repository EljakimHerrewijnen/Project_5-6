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

    def testDateConversion(self):
        newDate = self.AdminDAO.ConvertDateToObject(self.Date)
        keyTest = []

        for key in self.CorrectDate:
            keyTest.append(key)

        for key in keyTest:
            if not (key in newDate):
                return False

            if not (newDate[key] == self.CorrectDate[key]):
                return False

        return True



    def testJsonConversion(self):
        newJson = self.AdminDAO.ToJsonObject(self.WrongJsonObject)
        keyTest = []

        for key in self.CorrectJsonObject:
            keyTest.append(key)

        for key in keyTest:
            if not (key in newJson):
                return False

            if not (newJson[key] == self.CorrectJsonObject[key]):
                return False

        return True


    def TestAdmin(self):
        if not(self.testDateConversion()):
            return False
        if not(self.testJsonConversion()):
            return False
        return True
