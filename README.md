HumanFuture
===========

Python utility to write future dates in a human-friendly way.


Installing
==========

This packages is on PyPi, so assuming you have setup tools installed, it's just
a matter of doing

    pip install humanfuture


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
