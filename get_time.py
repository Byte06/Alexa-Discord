from datetime import datetime
from pytz import timezone

def get_time():
    date_and_time = datetime.now(timezone('Europe/Berlin'))
    time = str(date_and_time)
    time = time.split(" ")
    del time[0]
    time = ''.join(str(e) for e in time)
    time = time.split(".")
    del time[1]
    time = ''.join(str(e) for e in time)
    time = time.split(":")
    del time[2]
    time = ':'.join(str(e) for e in time)
    return time

def get_exact_time():
    date_and_time = datetime.now(timezone('Europe/Berlin'))
    time = str(date_and_time)
    time = time.split(" ")
    del time[0]
    time = ''.join(str(e) for e in time)
    time = time.replace(":", ".")
    return time