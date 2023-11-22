from datetime import datetime
from pytz import timezone


def get_date():
    date_and_time = datetime.now(timezone('Europe/Berlin'))
    date = str(date_and_time)
    date = date.split(" ")
    del date[1]
    date = ''.join(str(e) for e in date)
    date = date.split("-")
    date = str(date[2] + "." + date[1] + "." + date[0])
    return date

def get_date_in_ten_years():
    date_and_time = datetime.now(timezone('Europe/Berlin'))
    date = str(date_and_time)
    date = date.split(" ")
    del date[1]
    date = ''.join(str(e) for e in date)
    date = date.split("-")
    year_in_ten_years = int(date[0]) + 10
    date = date[2] + "." + date[1] + "." + str(year_in_ten_years)
    return date