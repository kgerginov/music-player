from python101.music_library.utils import *
import datetime
import random
from prettytable import PrettyTable
import json
import os
import mutagen


class Song:
    def __init__(self, title, artist, album, song_length):
        if validate_length(get_formatted_time(song_length)):
            raise ValueError('Invalid Song Length')
        self.title = title
        self.artist = artist
        self.album = album
        self.song_length = song_length

    def __str__(self):
        return f'{self.artist} - {self.title} from {self.album} - {self.song_length}'

    def __eq__(self, other):
        return (
            self.title == other.title
            and self.artist == other.artist
            and self.album == other.album
            and self.length(seconds=True) == other.length(seconds=True)
        )

    def __hash__(self):
        return hash(str(self))

    @staticmethod
    def to_seconds(time):
        if len(time) == 2:
            return time[0]*60 + time[1]
        return time[0]*3600 + time[1]*60 + time[2]

    @staticmethod
    def to_minutes(time):
        if len(time) == 2:
            return time[0]
        return time[0]*60 + time[1]

    @staticmethod
    def to_hours(time):
        if len(time) == 3:
            return time[0]
        return 0

    def get_converted_time(self, dict_, time):
        """ Checks if keyword arguments are what we are expecting """

        arguments = ('seconds', 'minutes', 'hours')
        for argument, value in dict_.items():
            if argument not in arguments:
                raise ValueError('Enter right command')
            if argument == 'seconds' and value:
                return self.to_seconds(time)
            if argument == 'minutes' and value:
                return self.to_minutes(time)
            if argument == 'hours' and value:
                return self.to_hours(time)

    def length(self, **kwargs):
        """ Returns length of song by given param: seconds=True, minutes=Trie or hours=True """

        time = get_formatted_time(self.song_length)
        if len(kwargs) > 1:
            raise Exception('Enter only 1 command')
        if kwargs:
            return self.get_converted_time(kwargs, time)
        return self.song_length


class Playlist:
    def __init__(self, name, repeat=False, shuffle=False):
        assert isinstance(repeat, bool)
        assert isinstance(shuffle, bool)
        self.name = name
        self.repeat = repeat
        self.shuffle = shuffle
        self._songs = []
        self._played_songs = set()
        self.current_song = None

    def add_song(self, song):
        if isinstance(song, Song):
            if not self._songs:
                self.current_song = song
            self._songs.append(song)
        else:
            raise TypeError('This is not a song!')

    def remove_song(self, song):
        if song in self._songs:
            self._songs.remove(song)

    def add_songs(self, songs):
        for song in songs:
            self.add_song(song)

    def total_length(self):
        total_len_seconds = sum(song.length(seconds=True) for song in self._songs)
        return str(datetime.timedelta(seconds=total_len_seconds))

    def artists(self):
        res = {}
        for song in self._songs:
            artist = song.artist
            if artist in res.keys():
                res[artist] += 1
            else:
                res[artist] = 1
        return res

    def get_random_song(self):
        return random.choice(self._songs)

    def shuffle_songs(self):
        song = self.get_random_song()

        while song in self._played_songs:
            song = self.get_random_song()

        self._played_songs.add(song)

        if len(self._songs) == len(self._played_songs):
            self._played_songs.clear()

        self.current_song = song
        return self.current_song

    def next_song(self):
        if not self._songs:
            raise Exception('Playlist is empty!')

        if self.shuffle:
            return self.shuffle_songs()

        if self.current_song != self._songs[-1]:
            current_song_index = self._songs.index(self.current_song)
            self.current_song = self._songs[current_song_index + 1]
            return self.current_song

        else:
            if self.repeat:
                self.current_song = self._songs[0]
                return self.current_song

            else:
                raise Exception('Reached end of Playlist!')

    def pprint_playlist(self):
        table = PrettyTable()
        table.field_names = ['Artist', 'Song', 'Length']

        for song in self._songs:
            table.add_row([song.artist, song.title, song.length()])

        print(table)

    def prep_for_serialization(self):
        dict_ = {
            'name': self.name,
            'repeat': self.repeat,
            'shuffle': self.shuffle,
            '_songs': [song.__dict__ for song in self._songs]
        }
        return dict_

    def create_json_name(self):
        return f'{self.name.replace(" ", "-")}.json'

    def save(self):
        with open(os.path.join('playlist-data', self.create_json_name()), 'w') as f:
            json.dump(self.prep_for_serialization(), f, indent=4)

    @staticmethod
    def load(filename):
        with open(os.path.join('playlist-data', filename), 'r') as f:
            data = json.load(f)

        playlist = Playlist(
            name=data.get('name'),
            repeat=data.get('repeat'),
            shuffle=data.get('shuffle')
        )

        for song in data.get('_songs'):
            s = Song(
                title=song.get('title'),
                artist=song.get('artist'),
                album=song.get('album'),
                song_length=song.get('song_length')
            )
            playlist.add_song(s)

        return playlist


class MusicCrawler:
    def __init__(self, path):
        self.path = path

    @staticmethod
    def extract_song_data(dict_):
        song_info = {}
        song_info['title'] = dict_.get('TIT2')
        song_info['artist'] = dict_.get('TPE1')
        song_info['album'] = dict_.get('TALB')
        length = dict_.info.length // 1
        song_info['song_length'] = str(datetime.timedelta(seconds=length))
        return song_info

    @staticmethod
    def check_if_song_attribute_is_none(dict_, key):
        if dict_.get(key) is None:
            return f'Unknown {key.title()}'
        return dict_.get(key).text[0]

    def create_playlist(self, name, shuffle=False, repeat=False):
        playlist = Playlist(name, repeat, shuffle)
        with os.scandir(self.path) as it:
            for file in it:
                if file.name.endswith('.mp3') and file.is_file():
                    path_to_mp3 = os.path.join(self.path, file.name)
                    mp3_data = mutagen.File(path_to_mp3)
                    song_data = self.extract_song_data(mp3_data)
                    song = Song(
                        title=self.check_if_song_attribute_is_none(song_data, 'title'),
                        artist=self.check_if_song_attribute_is_none(song_data, 'artist'),
                        album=self.check_if_song_attribute_is_none(song_data, 'album'),
                        song_length=song_data.get('song_length')
                    )
                    playlist.add_song(song)

        return playlist










