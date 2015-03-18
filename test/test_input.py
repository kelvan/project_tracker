import unittest
import tempfile
from datetime import date

from input import convert_dict, load_from_csv


class TestCSVInput(unittest.TestCase):
    def setUp(self):
        pass

    def test_load_valid_csv(self):
        """ Test csv load module
        test type conversions
        """
        with tempfile.NamedTemporaryFile() as f:
            f.write(b'date;project;hours;note\n'
                    b'2000-01-01;Testproject;1.0;test note 1\n'
                    b'2000-01-02;Testproject;2.5;test note 2\n')
            f.seek(0)

            lst = load_from_csv(f.name)
            self.assertEqual(2, len(lst))
            for i, l in enumerate(lst):
                self.assertIn('date', l)
                self.assertEqual(date(2000, 1, i+1), l['date'])
                self.assertIn('project', l)
                self.assertEqual('Testproject', l['project'])
                self.assertIn('hours', l)
                hours = 1 + i + i * 0.5
                self.assertEqual(hours, l['hours'])
                self.assertIn('note', l)
                self.assertEqual('test note %d' % (i+1), l['note'])

    def test_load_invalid_csv(self):
        """ Test loading an invalid broken
        """
        with tempfile.NamedTemporaryFile() as f:
            f.write(b'date;project;hours;note\n'
                    b'2000-01-01;Testproject;1.\n0;test note 1\n'
                    b'2000-01-02;Testproject;2.5;test note 2\n')
            f.seek(0)

            self.assertRaises(ValueError, load_from_csv, f.name)

    def test_load_invalid_csv_date(self):
        """ Test load csv with invalid date
        """
        with tempfile.NamedTemporaryFile() as f:
            f.write(b'date;project;hours;note\n'
                    b'2000-02-30;Testproject;1.0;test note 1\n'
                    b'2000-01-02;Testproject;2.5;test note 2\n')
            f.seek(0)

            self.assertRaises(ValueError, load_from_csv, f.name)
