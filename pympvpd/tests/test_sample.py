"""pympvpd.tests.test_sample."""
import unittest
import sys
from pympvpd import sample


class SampleTests(unittest.TestCase):
    """Tests pympvpd.sample."""

    def test_hello(self):
        """Hello() test."""
        self.assertEqual(sample.hello('Alice'), 'Hello, Alice.')

    def test_bmi(self):
        """Bmi test."""
        self.assertTrue(18.5 <= sample.bmi(1.68, 67.0) < 25)

    def test_bmi_zero_devide(self):
        """Bmi zero devide."""
        with self.assertRaises(ZeroDivisionError) as exc:
            sample.bmi(0, 67.0)
        if sys.version_info < (3, 0):
            self.assertIsNotNone(exc.exception.message)
        else:
            self.assertIsNotNone(exc.exception.__str__())
