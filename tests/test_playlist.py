import unittest
from python101.music_library.library import Playlist
from python101.music_library.library import Song


class TestPlaylist(unittest.TestCase):
    def setUp(self):
        self.test_playlist = Playlist(name='My Playlist', repeat=True, shuffle=True)
        self.test_song = Song(title='Jaza', artist='Slavi', album='???', song_length='4:34')
        self.test_song2 = Song(title='Leb', artist='Rammstein', album='??', song_length='2:45')
        self.test_song3 = Song(title='Ad i Rai', artist='Slavi', album='???', song_length='3:45')
        self.two_songs = [self.test_song, self.test_song2]
        self.three_songs = [self.test_song, self.test_song2, self.test_song3]

    def test_initialization_with_invalid_attributes_should_raise_assertion_error(self):
        with self.subTest('Repeat attribute not bool'):
            self.setUp()
            with self.assertRaises(AssertionError):
                Playlist(name='asd', repeat=1, shuffle=True)

        with self.subTest('Shuffle attribute not bool'):
            self.setUp()
            with self.assertRaises(AssertionError):
                Playlist(name='asd', repeat=False, shuffle=23)

    def test_add_song_with_invalid_data_raises_type_error(self):
        self.setUp()
        with self.assertRaises(TypeError):
            self.test_playlist.add_song('asd')

    def test_total_length(self):
        self.setUp()
        self.test_playlist.add_songs(self.two_songs)
        exp_data = '0:07:19'
        result = self.test_playlist.total_length()
        self.assertEqual(result, exp_data)

    def test_artists_one_song_per_artist(self):
        self.setUp()
        self.test_playlist.add_songs(self.two_songs)
        exp_data = {
            'Slavi': 1,
            'Rammstein': 1
        }
        result = self.test_playlist.artists()
        self.assertEqual(result, exp_data)

    def test_artist_more_than_one_song(self):
        self.setUp()
        s = Song(title='Kombainera', artist='Slavi', album='???', song_length='2:14')
        self.test_playlist.add_songs(self.two_songs)
        self.test_playlist.add_song(s)
        exp_data = {
            'Slavi': 2,
            'Rammstein': 1
        }
        result = self.test_playlist.artists()
        self.assertEqual(result, exp_data)

    def test_next_song_if_playlist_is_empty_should_raise_exception(self):
        self.setUp()
        with self.assertRaises(Exception):
            self.test_playlist.next_song()

    # def test_next_song_repeatTrue_shuffleTrue(self):
    #     self.setUp()
    #     self.test_playlist.add_songs(self.two_songs)
    #     result = self.test_playlist.next_song()
    #     exp_data = self.test_song2
    #     self.assertEqual(result, exp_data)

    def test_new_song_repeat_True_shuffle_False(self):
        self.setUp()
        ply = Playlist(name='New', repeat=True)
        ply.add_songs(self.three_songs)
        self.assertEqual(ply.current_song, self.test_song)

        ply.next_song()
        self.assertEqual(ply.current_song, self.test_song2)

        ply.next_song()
        self.assertEqual(ply.current_song, self.test_song3)

        ply.next_song()
        self.assertEqual(ply.current_song, self.test_song)

    def test_next_song_repeat_False_shuffle_False_raises_Exception(self):
        with self.assertRaises(Exception):
            self.setUp()
            ply = Playlist(name='new')
            ply.add_song(self.test_song)
            ply.next_song()

    # def test_played_songs(self):
    #     self.setUp()
    #     ply = self.test_playlist
    #     ply.add_songs(self.two_songs)
    #     ply.next_song()
    #     result = ply._played_songs
    #     exp_data = set()
    #     exp_data.add(self.test_song)
    #     self.assertEqual(result, exp_data)
    #     ply.next_song()
    #     self.assertEqual(set(), ply._played_songs)

    def test_if_played_songs_clears(self):
        self.setUp()
        ply = self.test_playlist
        ply.add_songs(self.two_songs)
        ply.next_song()
        result = ply._played_songs
        exp_data = set()
        ply.next_song()
        self.assertEqual(result, exp_data)

    # def test_pprint_playlist(self):
    #     self.setUp()
    #     ply = self.test_playlist
    #     ply.add_songs(self.three_songs)
    #     ply.pprint_playlist()

    def test_prep_for_serialization(self):
        self.setUp()
        ply = self.test_playlist
        ply.add_song(self.test_song)
        result = ply.prep_for_serialization()
        exp_data = {
            'name': 'My Playlist',
            'repeat': True,
            'shuffle': True,
            '_songs': [{
                'title': 'Jaza',
                'artist': 'Slavi',
                'album': '???',
                'song_length': '4:34'
            }]
        }
        self.assertEqual(result, exp_data)

    def test_create_json_name(self):
        self.setUp()
        ply = self.test_playlist
        result = ply.create_json_name()
        exp_data = 'My-Playlist.json'
        self.assertEqual(result, exp_data)

    def test_load_playlist(self):
        self.setUp()
        pl = Playlist(name='nova chalga')
        pl.add_songs(self.three_songs)
        pl.save()
        ply = Playlist.load('nova-chalga.json')
        self.assertEqual(ply.name, 'nova chalga')
        self.assertFalse(ply.shuffle)
        self.assertFalse(ply.repeat)


if __name__ == '__main__':
    unittest.main()
