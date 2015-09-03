from __future__ import division

import unittest
from ..weekday_count import get_weekday_count_month


class TestWeekdayCount(unittest.TestCase):
    def test_month_2015_01(self):
        counts = get_weekday_count_month(2015, 1)
        self.assertEqual(counts[0], 4)
        self.assertEqual(counts[1], 4)
        self.assertEqual(counts[2], 4)
        self.assertEqual(counts[3], 5)
        self.assertEqual(counts[4], 5)
        self.assertEqual(counts[5], 5)
        self.assertEqual(counts[6], 4)

    def test_month_2015_02(self):
        counts = get_weekday_count_month(2015, 2)
        for weekday in range(7):
            self.assertEqual(counts[weekday], 4)

    def test_month_2015_03(self):
        counts = get_weekday_count_month(2015, 3)
        self.assertEqual(counts[0], 5)
        self.assertEqual(counts[1], 5)
        self.assertEqual(counts[2], 4)
        self.assertEqual(counts[3], 4)
        self.assertEqual(counts[4], 4)
        self.assertEqual(counts[5], 4)
        self.assertEqual(counts[6], 5)

    def test_month_2015_04(self):
        counts = get_weekday_count_month(2015, 4)
        self.assertEqual(counts[0], 4)
        self.assertEqual(counts[1], 4)
        self.assertEqual(counts[2], 5)
        self.assertEqual(counts[3], 5)
        self.assertEqual(counts[4], 4)
        self.assertEqual(counts[5], 4)
        self.assertEqual(counts[6], 4)

    def test_month_2015_08(self):
        counts = get_weekday_count_month(2015, 8)
        self.assertEqual(counts[0], 5)
        self.assertEqual(counts[1], 4)
        self.assertEqual(counts[2], 4)
        self.assertEqual(counts[3], 4)
        self.assertEqual(counts[4], 4)
        self.assertEqual(counts[5], 5)
        self.assertEqual(counts[6], 5)
