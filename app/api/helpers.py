def convert_iso_to_json(dateString):
    tempDateObject = dateString.split("-")
    return {
        "year": tempDateObject[0],
        "month": tempDateObject[1],
        "day": tempDateObject[2]
    }

def convert_json_to_iso(json):
    return "{0}-{1}-{2}".format(int(json['year']), int(json['month']), int(json['day']))