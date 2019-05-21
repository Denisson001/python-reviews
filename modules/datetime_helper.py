import datetime
import pytz


def apply_time_format(time_value):
    time_value = str(time_value)
    if len(time_value) == 1:
        time_value = '0' + time_value
    return time_value


def get_date():
    tz = pytz.timezone('Europe/Moscow')
    ctime = datetime.datetime.now(tz)
    return ctime


def get_current_date():
    ctime = get_date()
    current_date = str(ctime.year) + '-' + apply_time_format(ctime.month) + '-' + apply_time_format(ctime.day)
    return current_date


def get_tomorrow_date():
    ctime = get_date() + datetime.timedelta(days=1)
    current_date = str(ctime.year) + '-' + apply_time_format(ctime.month) + '-' + apply_time_format(ctime.day)
    return current_date


def get_current_time():
    ctime = get_date()
    current_date = apply_time_format(ctime.hour) + ':' + apply_time_format(ctime.minute) + ":00"
    return current_date


def get_current_timestamp():
    return get_current_date() + ' ' + get_current_time()


def compare_timestamps(dt1, dt2):
    t1 = list(map(int, dt1.split(':')))
    t2 = list(map(int, dt2.split(':')))
    return t1 > t2


def check_time_format(time_value):
    if len(time_value) != 5 or time_value[2] != ':':
        return False
    if not (time_value[:2] + time_value[3:]).isdigit():
        return False
    values = list(map(int, time_value.split(':')))
    if values[0] >= 24 or values[1] >= 60:
        return False
    return True
