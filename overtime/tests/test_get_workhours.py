import unittest
from datetime import datetime

from .. import overtime #get_workhours


class TestWorkHours(unittest.TestCase):
    def setUp(self):
        overtime.workhours_per_day = [1, 2, 4, 8, 16, 0, 0]

    def test_get_workhours(self):
        start = datetime(2015, 8, 1)
        end = datetime(2015, 8, 31)
        self.assertEqual(overtime.get_workhours(start, end), 125)
