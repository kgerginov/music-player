
def convert_to_int(time):
    try:
        res = [int(t.strip()) for t in time]
    except Exception:
        raise ValueError
    else:
        return res


def get_formatted_time(st):
    return convert_to_int(st.split(':'))


def validate_minutes(time):
    if time[0] > 59 or time[0] < 0:
        return True
    if time[1] > 59 or time[1] < 0:
        return True
    return False


def validate_hours(time):
    if time[0] < 0:
        return True
    if time[1] > 59 or time[1] < 0:
        return True
    if time[2] > 59 or time[2] < 0:
        return True
    return False


def validate_length(time):
    if len(time) == 2:
        return validate_minutes(time)

    if len(time) == 3:
        return validate_hours(time)

    if len(time) > 3:
        return True

    else:
        return False














