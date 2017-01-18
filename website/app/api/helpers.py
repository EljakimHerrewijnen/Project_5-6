def date_convert(date):
    year, month, day = date.split('-')
    return {
        "year" : int(year),
        "month" : int(month),
        "day" : int(day)
    }