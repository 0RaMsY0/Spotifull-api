import datetime

def date() -> datetime:
    """
        Returns the current datime
    """
    _date = f"{datetime.datetime.now().year}-{datetime.datetime.now().month}-{datetime.datetime.now().day}-{datetime.datetime.now().hour}"
    print(_date)
    
    return _date

def hour() -> int:
    """
        Returns the current hour
    """
    _hour = datetime.datetime.now().hour

    return _hour

def today() -> int:
    """
        Returns the current day
    """
    _day = datetime.datetime.now().day

    return _day
