from pymongo import MongoClient
from datetime import datetime
import settings


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

    # def get_habs(self) -> dict:
    #     habs = {}
    #     collection = self.db['habs']
    #     cursor = collection.find()
    #     # habs = map(lambda k, v: {k:v}, cursor)
    #     for each in cursor:
    #         habs[each['name']] = each['link']
    #
    #     return habs

    def add_hab(self, song):
        collection = self.db['songs']
        count = collection.find({'name': song['name']}).count()
        if count == 0:
            collection.insert({'name': song['name'], 'band_name': song['band_name'], 'link': song['link'], 'like': 0})

    # def del_hab(self, hab):
    #     collection = self.db['habs']
    #     collection.remove({"name": hab})
