import unittest
from python101.music_library.library import Song
from python101.music_library.utils import *


class TestSong(unittest.TestCase):
    def setUp(self):
        self.test_song = Song(title='habibi', artist='azis', album='???', song_length='2:03')

    def test_split_length(self):
        with self.subTest('Minutes only'):
            result = get_formatted_time(self.test_song.song_length)
            exp_data = [2, 3]
            self.assertEqual(result, exp_data)

        with self.subTest('With hours'):
            s = Song(title='habibi', artist='azis', album='???', song_length='1:04:05')
            result = get_formatted_time(s.song_length)
            exp_data = [1, 4, 5]
            self.assertEqual(result, exp_data)

    def test_creating_song_with_invalid_length_should_raise_attribute_error(self):
        with self.subTest('Invalid minutes'):
            with self.assertRaises(ValueError):
                s = Song(title='habibi', artist='azis', album='???', song_length='76:23')

            with self.assertRaises(ValueError):
                Song(title='habibi', artist='azis', album='???', song_length='aa:23')

    def test_length_minutes_true(self):
        result = Song(title='habibi', artist='azis', album='???', song_length='1:23:45')
        exp_data = 83
        self.assertEqual(result.length(minutes=True), exp_data)

    def test_length_seconds_true(self):
        result = Song(title='habibi', artist='azis', album='???', song_length='1:23:45')
        exp_data = 5025
        self.assertEqual(result.length(seconds=True), exp_data)

    def test_length_hours_true(self):
        result = Song(title='habibi', artist='azis', album='???', song_length='1:23:45')
        exp_data = 1
        self.assertEqual(result.length(hours=True), exp_data)

    def test_length_multiple_arguments_should_raise_value_error(self):
        with self.assertRaises(Exception):
            self.test_song.length(seconds=True, minutes=True)

    def test_unknown_argument_should_raise_value_error(self):
        with self.assertRaises(Exception):
            self.test_song.length(sekundi=True)


if __name__ == '__main__':
    unittest.main()


