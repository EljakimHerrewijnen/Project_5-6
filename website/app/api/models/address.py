import json

class Address:
    def __init__(self, postal_code, house_number, country, city):
        self.postal_code = postal_code
        self.house_number = house_number
        self.country = country
        self.city = city

    def toDict(self):
        return {
            "postal_code"   : self.postal_code,
            "house_number"  : self.house_number,
            "country"       : self.country,
            "city"          : self.city
        }

    def toJson(self):
        return json.dumps(self.toDict())

    @staticmethod
    def fromDict(json):

        return Address(
            json["postal_code"],
            int(json["house_number"]),
            json["country"],
            json["city"],
        )