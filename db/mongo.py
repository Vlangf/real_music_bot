import settings
from pymongo import MongoClient
from client import models


class DB(object):
    def __init__(self):
        client = MongoClient(settings.mongo_host, int(settings.mongo_port),
                             username=settings.mongo_login,
                             password=settings.mongo_password)
        db = client.realMusic
        self.collection = db.songs

    def add_songs(self, songs: list):
        self.collection.insert_many(songs)

    def get_random_songs(self, size):
        songs = self.collection.aggregate([{'$match': {'like': 0}},
                                           {'$sample': {'size': size}}])
        songs_list = []
        for song in songs:
            songs_list.append(models.Song(**song))

        return songs_list

    def set_song_like_or_dislike(self, name, like):
        if like == '+':
            self.collection.update({'name': name}, {'$set': {'like': 1}})

        if like == '-':
            self.collection.update({'name': name}, {'$set': {'like': -1}})
