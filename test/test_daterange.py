import unittest
from datetime import date

import daterange as dr


class TestDateRange(unittest.TestCase):
    def setUp(self):
        self.today = date.today()

    def test_week_range(self):
        """ Test loading week date ranges
        """
        first_week_2015 = (date(2014, 12, 29), date(2015, 1, 4))
        self.assertTupleEqual(first_week_2015,
                              dr._get_week_range(2015, 1))
        first_week_2012 = (date(2012, 1, 2), date(2012, 1, 8))
        self.assertTupleEqual(first_week_2012,
                              dr._get_week_range(2012, 1))
        _30th_week_2014 = (date(2014, 7, 21), date(2014, 7, 27))
        self.assertTupleEqual(_30th_week_2014,
                              dr._get_week_range(2014, 30))

    def test_current_week_range(self):
        self.assertTupleEqual(dr._get_week_range(self.today.year,
                                                 self.today.isocalendar()[1]),
                              dr._get_current_week_range())

    def test_first_day_of_week(self):
        self.assertEqual(date(2012, 1, 2), dr._get_first_day_of_week(2012, 1))
        self.assertEqual(date(2014, 7, 21), dr._get_first_day_of_week(2014, 30))
        self.assertEqual(date(2014, 12, 29), dr._get_first_day_of_week(2015, 1))

    def test_month_range(self):
        self.assertEqual(date(2015, 1, 31), dr._get_month_range(2015, 1)[1])
        self.assertEqual(date(2015, 2, 28), dr._get_month_range(2015, 2)[1])
        self.assertEqual(date(2000, 2, 29), dr._get_month_range(2000, 2)[1])
        self.assertEqual(date(2015, 3, 1), dr._get_month_range(2015, 3)[0])
        self.assertEqual(date(2015, 4, 30), dr._get_month_range(2015, 4)[1])

    def test_in_range(self):
        range_ = dr._get_month_range(2015, 3)
        self.assertTrue(dr.in_range(date(2015, 3, 1), range_))
        self.assertTrue(dr.in_range(date(2015, 3, 15), range_))
        self.assertTrue(dr.in_range(date(2015, 3, 31), range_))
        self.assertFalse(dr.in_range(date(2014, 3, 15), range_))
        self.assertFalse(dr.in_range(date(2015, 2, 28), range_))
        self.assertFalse(dr.in_range(date(2015, 4, 1), range_))
