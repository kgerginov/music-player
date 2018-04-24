import unittest
from python101.music_library.utils import *


class TestUtils(unittest.TestCase):

    def test_validate_length_valid_data_minute_seconds(self):
        data = [23, 45]
        self.assertFalse(validate_length(data))

    def test_validate_length_valid_data_hours_mins_sec(self):
        data = [23, 45, 56]
        self.assertFalse(validate_length(data))

    def test_validate_length_invalid_seconds(self):
        data = [2, 34, 67]
        self.assertTrue(validate_length(data))

    def test_validate_length_invalid_negative_time(self):
        data = [-2, -34, 24]
        self.assertTrue(validate_length(data))

    def test_validate_length_invalid_minutes(self):
        data = [2, 67, 12]
        self.assertTrue(validate_length(data))


if __name__ == '__main__':
    unittest.main()
