from datetime import datetime, timedelta

class NegativeDeltaError(Exception): pass
class UnformattableError(Exception): pass

def humanize(future, ref=None):
    """
    Return a nice string representing a future datetime in english.
    If you need to explicitely set the reference that the future is relative
    to, just pass it in as a second datetime object.
    """

    if not ref:
        ref = datetime.now()

    delta = future - ref
    seconds = delta.seconds
    days = delta.days
    global_seconds = days * 24 * 60 * 60 + seconds
    minutes = int(round(seconds/60.) % 60)
    day_changes = (future - datetime(*ref.timetuple()[:3])).days

    if days < 0:
        raise NegativeDeltaError("Negative timedelta. I can only do futures!")

    if global_seconds <= 45:
        if seconds <= 15:
            return 'a moment'
        else:
            return english_number(seconds, 'second', 'seconds')

    elif global_seconds < 60 * 59.5:
        if seconds <= 90:
            return 'about a minute'
        elif seconds <= 60 * 4.5:
            return 'about %s' % english_number(minutes, 'minute', 'minutes')
        else:
            return english_number(minutes, 'minute', 'minutes')

    elif global_seconds < 60 * 60 * 2.5:
        return '%s%s' % (english_number(hours(seconds), 'hour', 'hours'),
            (lambda m: '' if m is 0 else ' and %s' % english_number(m, 'minute', 'minutes'))(minutes))

    elif global_seconds < 60 * 60 * 24 and ref.day == future.day:
        if future.hour == 23 and future.minute == 58:
            return 'two minutes to midnight'
        return english_time(future)

    elif (global_seconds <= 60 * 60 * 24 * 2 and day_changes == 1):
        if future.hour == 0:
            if future.minute == 0:
                return 'midnight tonight'
        return 'tomorrow at %s' % english_time(future)

    elif (global_seconds <= 60 * 60 * 24 * 8 and day_changes <= 7):
        if day_changes <= 3 or (future.weekday() == 6 and ref.weekday() != 6):
            return '%s at %s' % (future.strftime('%A'), english_time(future))
        elif (future.weekday() > ref.weekday() or ref.weekday() == 6) and day_changes <= 6:
            return 'this %s at %s' % (future.strftime('%A'), english_time(future))
        else:
            return 'next %s at %s' % (future.strftime('%A'), english_time(future))

    elif ref.year == future.year:
        return '%s at %s' % (english_date(future), english_time(future))

    else:
        return '%s, %d at %s' % (english_date(future), future.year, english_time(future))

    raise UnformattableError("Couldn't format date.")


def hours(seconds):
    return int(seconds/3600)

def english_number(num, unit=None, plural=None):
    eng_num = ['zero', 'one', 'two', 'three', 'four', 'five',
        'six', 'seven', 'eight', 'nine'][num] if num < 10 else str(num)
    if unit:
        if num is 1:
            return '%s %s' % (eng_num, unit)
        else:
            return '%s %s' % (eng_num, plural if plural else unit)
    return eng_num

def english_time(time):
    if time.hour == 12 and time.minute == 0:
        return 'noon'
    midi = 'am' if time.hour < 12 else 'pm'
    mins = str(time.minute).zfill(2) if time.minute else None
    hour = (lambda h: h if h is not 0 else 12)(time.hour % 12)
    hour = 12 if hour == 0 else hour
    return '%s %s' % ('%s:%s' % (hour, mins) if mins else hour, midi)

def english_date(time):
    return '%s %d' % (time.strftime('%B'), time.day)