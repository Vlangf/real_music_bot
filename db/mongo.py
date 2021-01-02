import settings
from pymongo import MongoClient
from client import models


class DB(object):
    def __init__(self):
        self.host = settings.mongo_host
        self.port = int(settings.mongo_port)
        self.login = settings.mongo_login
        self.password = settings.mongo_password
        client = MongoClient(self.host, self.port,
                             username=settings.mongo_login,
                             password=settings.mongo_password)
        self.db = client.realMusic

    def add_song(self, song: dict):
        collection = self.db['songs']
        count = collection.find({'name': song['name']}).count()
        if count == 0:
            collection.insert({'name': song['name'], 'band_name': song['band_name'], 'link': song['link'], 'like': 0,
                               'date_add_to_site': song['date'], 'genre': song['genre']})

    def get_random_songs(self, size):
        collection = self.db['songs']
        songs = collection.aggregate([{'$match': {'like': 0}},
                                      {'$sample': {'size': size}}])
        songs_list = []
        for song in songs:
            songs_list.append(models.Song(**song))

        return songs_list

    def set_song_like_or_dislike(self, name, like):
        collection = self.db['songs']
        if like == '+':
            collection.update({'name': name}, {'$set': {'like': 1}})

        if like == '-':
            collection.update({'name': name}, {'$set': {'like': -1}})
