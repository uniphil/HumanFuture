import unittest
from datetime import datetime, timedelta
from .. import humanfuture as hf


class TestHumanFuture(unittest.TestCase):
    
    def setUp(self):
        # Sunday, jan 1, 2012
        self.ref_time = datetime(2012, 1, 1, 0, 0, 0)

    def assertHuman(self, future, human, ref=None):
        ref = ref if ref is not None else self.ref_time
        self.assertEqual(hf.humanize(future, ref), human)

    def testNegative(self):
        """Negative delta Raises an Exception"""
        self.assertRaises(hf.NegativeDeltaError, hf.humanize, 
            datetime(2011, 12, 31, 23, 59, 0),
            datetime(2012, 1, 1, 0, 0, 0))
        self.assertRaises(hf.NegativeDeltaError, hf.humanize,
            datetime(2012, 1, 1, 11, 59, 0),
            datetime(2012, 1, 1, 12, 0, 0))

    def testNegativeDay(self):
        delta = datetime(2011, 12, 31, 0, 0, 0) - self.ref_time
        self.assertRaises(hf.NegativeDeltaError, hf.humanize,
            datetime(2011, 12, 31, 0, 0, 0),
            datetime(2012, 1, 1, 0, 0, 0))
    
    def testNow(self):
        self.assertHuman(datetime(2012, 1, 1, 0, 0), 'a moment')
    
    def testSmallSeconds(self):
        self.assertHuman(datetime(2012, 1, 1, 0, 0, 1), 'a moment')
        self.assertHuman(datetime(2012, 1, 1, 0, 0, 15), 'a moment')
    
    def testMedSeconds(self):
        self.assertHuman(datetime(2012, 1, 1, 0, 0, 16), '16 seconds')
        self.assertHuman(datetime(2012, 1, 1, 0, 0, 45), '45 seconds')
    
    def testHighSeconds(self):
        self.assertHuman(datetime(2012, 1, 1, 0, 0, 46), 'about a minute')
        self.assertHuman(datetime(2012, 1, 1, 0, 1, 30), 'about a minute')
    
    def testLowMinutes(self):
        self.assertHuman(datetime(2012, 1, 1, 0, 1, 31), 'about two minutes')
        self.assertHuman(datetime(2012, 1, 1, 0, 4), 'about four minutes')
    
    def testMinutes(self):
        self.assertHuman(datetime(2012, 1, 1, 0, 5), 'five minutes')
        self.assertHuman(datetime(2012, 1, 1, 0, 10), '10 minutes')
        self.assertHuman(datetime(2012, 1, 1, 0, 59), '59 minutes')
    
    def testOnHours(self):
        self.assertHuman(datetime(2012, 1, 1, 1, 0), 'one hour')
        self.assertHuman(datetime(2012, 1, 1, 2, 0), 'two hours')
    
    def testOffHoursLowMinutes(self):
        self.assertHuman(datetime(2012, 1, 1, 1, 1), 'one hour and one minute')
        self.assertHuman(datetime(2012, 1, 1, 1, 2), 'one hour and two minutes')
        self.assertHuman(datetime(2012, 1, 1, 2, 9), 'two hours and nine minutes')
    
    def testOffHoursHighMinutes(self):
        self.assertHuman(datetime(2012, 1, 1, 1, 10), 'one hour and 10 minutes')
        self.assertHuman(datetime(2012, 1, 1, 2, 29), 'two hours and 29 minutes')
    
    def testToday(self):
        self.assertHuman(datetime(2012, 1, 1, 3, 0), '3 am')
        self.assertHuman(datetime(2012, 1, 1, 12, 1), '12:01 pm')
    
    def testNoon(self):
        self.assertHuman(datetime(2012, 1, 1, 12, 0), 'noon')
    
    def testMidnight(self):
        self.assertHuman(datetime(2012, 1, 2, 0, 0), 'midnight tonight')

    def testTodayAfterMidnight(self):
        self.assertHuman(datetime(2012, 1, 2, 0, 1), 'one minute past midnight')
        self.assertHuman(datetime(2012, 1, 2, 0, 25), '25 minutes past midnight')
        self.assertHuman(datetime(2012, 1, 2, 0, 26), 'tomorrow at 12:26 am')
    
    def testTomorrow(self):
        self.assertHuman(datetime(2012, 1, 2, 3, 0), 'tomorrow at 3 am')
        self.assertHuman(datetime(2012, 1, 2, 12, 1), 'tomorrow at 12:01 pm')
    
    def testTomorrowNoon(self):
        self.assertHuman(datetime(2012, 1, 2, 12, 0), 'tomorrow at noon')
    
    def testTomorrowMidnight(self):
        self.assertHuman(datetime(2012, 1, 3, 0, 0), 'tomorrow at midnight')
    
    def testTomorrowAfterMidnight(self):
        self.assertHuman(datetime(2012, 1, 3, 0, 1), 'one minute past midnight tomorrow')
        self.assertHuman(datetime(2012, 1, 3, 0, 25), '25 minutes past midnight tomorrow')
    
    def testTomorrowMinutesRollover(self):
        self.assertHuman(datetime(2012, 2, 1, 0, 0), 'about a minute',
            ref=datetime(2012, 1, 31, 23, 59, 0))
    
    def testTomorrowHoursRollover(self):
        self.assertHuman(datetime(2012, 2, 1, 0, 59), 'one hour',
            ref=datetime(2012, 1, 31, 23, 59, 0))

    def testTomorrowHoursRolloverThresh(self):
        self.assertHuman(datetime(2012, 2, 1, 2, 28, 0), 'two hours and 29 minutes',
                     ref=datetime(2012, 1, 31, 23, 59, 0))
        self.assertHuman(datetime(2012, 2, 1, 9, 0, 0), 'tomorrow at 9 am',
                     ref=datetime(2012, 1, 31, 23, 59, 0))
    
    def testWeekDaysFromSunday(self):
        # jan 1 2012 is a sunday.
        self.assertHuman(datetime(2012, 1, 3, 9, 0), 'Tuesday at 9 am')
        self.assertHuman(datetime(2012, 1, 4, 9, 0), 'Wednesday at 9 am')
        self.assertHuman(datetime(2012, 1, 5, 9, 0), 'this Thursday at 9 am')
        self.assertHuman(datetime(2012, 1, 6, 9, 0), 'this Friday at 9 am')
        self.assertHuman(datetime(2012, 1, 7, 9, 0), 'this Saturday at 9 am')
        self.assertHuman(datetime(2012, 1, 8, 9, 0), 'next Sunday at 9 am')

    def testWeekDaysFromMonday(self):
        mon = datetime(2012, 1, 2, 0, 0, 0)
        self.assertHuman(datetime(2012, 1, 4, 9, 0), 'Wednesday at 9 am', ref=mon)
        self.assertHuman(datetime(2012, 1, 5, 9, 0), 'Thursday at 9 am', ref=mon)
        self.assertHuman(datetime(2012, 1, 6, 9, 0), 'this Friday at 9 am', ref=mon)
        self.assertHuman(datetime(2012, 1, 7, 9, 0), 'this Saturday at 9 am', ref=mon)
        self.assertHuman(datetime(2012, 1, 8, 9, 0), 'Sunday at 9 am', ref=mon)
        self.assertHuman(datetime(2012, 1, 9, 9, 0), 'next Monday at 9 am', ref=mon)

    def testWeekDaysTuesday(self):
        tue = datetime(2012, 1, 3, 0, 0, 0)
        self.assertHuman(datetime(2012, 1, 5, 9, 0), 'Thursday at 9 am', ref=tue)
        self.assertHuman(datetime(2012, 1, 6, 9, 0), 'Friday at 9 am', ref=tue)
        self.assertHuman(datetime(2012, 1, 7, 9, 0), 'this Saturday at 9 am', ref=tue)
        self.assertHuman(datetime(2012, 1, 8, 9, 0), 'Sunday at 9 am', ref=tue)
        self.assertHuman(datetime(2012, 1, 9, 9, 0), 'next Monday at 9 am', ref=tue)
        self.assertHuman(datetime(2012, 1, 10, 9, 0), 'next Tuesday at 9 am', ref=tue)

    def testWeekDaysFromWednesday(self):
        wed = datetime(2012, 1, 4, 0, 0, 0)
        self.assertHuman(datetime(2012, 1, 6, 9, 0), 'Friday at 9 am', ref=wed)
        self.assertHuman(datetime(2012, 1, 7, 9, 0), 'Saturday at 9 am', ref=wed)
        self.assertHuman(datetime(2012, 1, 8, 9, 0), 'Sunday at 9 am', ref=wed)
        self.assertHuman(datetime(2012, 1, 9, 9, 0), 'next Monday at 9 am', ref=wed)
        self.assertHuman(datetime(2012, 1, 10, 9, 0), 'next Tuesday at 9 am', ref=wed)
        self.assertHuman(datetime(2012, 1, 11, 9, 0), 'next Wednesday at 9 am', ref=wed)

    def testWeekDaysFromThursday(self):
        thu = datetime(2012, 1, 5, 0, 0, 0)
        self.assertHuman(datetime(2012, 1, 7, 9, 0), 'Saturday at 9 am', ref=thu)
        self.assertHuman(datetime(2012, 1, 8, 9, 0), 'Sunday at 9 am', ref=thu)
        self.assertHuman(datetime(2012, 1, 9, 9, 0), 'next Monday at 9 am', ref=thu)
        self.assertHuman(datetime(2012, 1, 10, 9, 0), 'next Tuesday at 9 am', ref=thu)
        self.assertHuman(datetime(2012, 1, 11, 9, 0), 'next Wednesday at 9 am', ref=thu)
        self.assertHuman(datetime(2012, 1, 12, 9, 0), 'next Thursday at 9 am', ref=thu)

    def testWeekDaysFromFriday(self):
        fri = datetime(2012, 1, 6, 0, 0, 0)
        self.assertHuman(datetime(2012, 1, 8, 9, 0), 'Sunday at 9 am', ref=fri)
        self.assertHuman(datetime(2012, 1, 9, 9, 0), 'Monday at 9 am', ref=fri)
        self.assertHuman(datetime(2012, 1, 10, 9, 0), 'next Tuesday at 9 am', ref=fri)
        self.assertHuman(datetime(2012, 1, 11, 9, 0), 'next Wednesday at 9 am', ref=fri)
        self.assertHuman(datetime(2012, 1, 12, 9, 0), 'next Thursday at 9 am', ref=fri)
        self.assertHuman(datetime(2012, 1, 13, 9, 0), 'next Friday at 9 am', ref=fri)

    def testWeekDaysFromSaturday(self):
        fri = datetime(2012, 1, 7, 0, 0, 0)
        self.assertHuman(datetime(2012, 1, 9, 9, 0), 'Monday at 9 am', ref=fri)
        self.assertHuman(datetime(2012, 1, 10, 9, 0), 'Tuesday at 9 am', ref=fri)
        self.assertHuman(datetime(2012, 1, 11, 9, 0), 'next Wednesday at 9 am', ref=fri)
        self.assertHuman(datetime(2012, 1, 12, 9, 0), 'next Thursday at 9 am', ref=fri)
        self.assertHuman(datetime(2012, 1, 13, 9, 0), 'next Friday at 9 am', ref=fri)
        self.assertHuman(datetime(2012, 1, 14, 9, 0), 'next Saturday at 9 am', ref=fri)
    
    def testThisWeekRollover(self):
        mon = datetime(2012, 1, 30, 0, 0, 0)
        self.assertHuman(datetime(2012, 2, 1, 9, 0), 'Wednesday at 9 am', ref=mon)
        self.assertHuman(datetime(2012, 2, 4, 9, 0), 'this Saturday at 9 am', ref=mon)
    
    def testDate(self):
        self.assertHuman(datetime(2012, 1, 10, 9, 0), 'January 10 at 9 am')
        self.assertHuman(datetime(2012, 12, 31, 9, 0), 'December 31 at 9 am')

    def testYear(self):
        self.assertHuman(datetime(2013, 1, 1, 9, 0), 'January 1, 2013 at 9 am')
        self.assertHuman(datetime(2013, 12, 31, 9, 0), 'December 31, 2013 at 9 am')
        self.assertHuman(datetime(2014, 1, 1, 9, 0), 'January 1, 2014 at 9 am')


if __name__ == '__main__':
    unittest.main()

