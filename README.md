HumanFuture
===========

Python utility to write future dates in a human-friendly way.

The module was motivated by a need to represent future events in a friendly,
but not fuzzy way for the tweet-scheduling tool, 
[antictweet](http://anticitweet.com). Friendly language without sacrificing
precision is what makes HumanFuture different.

The module is currently hard-coded in 12-hour english, with a precision of one
minute.


Installing
==========

This packages is on PyPi, so assuming you have setup tools installed, it's just
a matter of doing

    pip install humanfuture


Examples
--------

    >>> import humanfuture as future
    >>> from datetime import datetime
    >>> ref = datetime(2012, 8, 6, 9, 0)
    >>> future.humanize(datetime(2012, 8, 6, 9, 1), ref)
    'about a minute'
    >>> future.humanize(datetime(2012, 8, 6, 9, 5), ref)
    'five minutes'
    >>> future.humanize(datetime(2012, 8, 6, 10, 30), ref)
    'one hour and 30 minutes'
    >>> future.humanize(datetime(2012, 8, 6, 12, 0), ref)
    'noon'
    >>> future.humanize(datetime(2012, 8, 7, 12, 0), ref)
    'tomorrow at noon'
    >>> future.humanize(datetime(2012, 8, 7, 18, 0), ref)
    'tomorrow at 6 pm'
    >>> future.humanize(datetime(2012, 8, 9, 14, 30), ref)
    'Thursday at 2:30 pm'
    >>> future.humanize(datetime(2012, 8, 13, 9, 15), ref)
    'next Monday at 9:15 am'
    >>> future.humanize(datetime(2012, 10, 13, 12, 0), ref)
    'October 13 at noon'
    >>> future.humanize(datetime(2013, 4, 13, 23, 11), ref)
    'April 13, 2013 at 11:11 pm'


For a more complete -- though, also uglier -- reference of what this module
outputs, see `test_humanfuture.py` in `tests`.


Humanizing Your Future
======================

The `humanize` function in `humanfuture` is the one you want. Just pass in a
datetime object for sometime in the future and it should spit out a nice
english string.

If you need to get out relative futures from some time other than now, you can
pass in a reference datetime as the second arguement.


Dealing with Your Past
======================

Two exceptions could be thrown by this module, a
`humanfuture.NegativeDeltaError`, or a `humanfuture.UnformattableError`. The
second one should never actually occur. Please let me know if you ever come
across it. But the first one you need to watch out for.

This module's scope is restricted to future times, so it throws that
`humanfuture.NegativeDeltaError` if you give it a futures past. To avoid this,
either check your futures before submitting, or if you're unsure, put the
conversion in a `try/catch` block and deal with it there.


Credits
=======

Although this is a completely new module, some inspiration was taken from the
lovely [`humanize`](https://github.com/jmoiron/humanize) module.
