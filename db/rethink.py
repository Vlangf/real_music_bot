from rethinkdb import RethinkDB
import settings


class DB(object):
    def __init__(self):
        self.r = RethinkDB()
        self.r.connect(host=settings.mongo_host, port=int(settings.r_port)).repl()

        if 'realMusic' not in self.r.db_list().run():
            self.r.db_create('realMusic').run()

        if 'songs' not in self.r.db('realMusic').table_list().run():
            self.r.db('realMusic').table_create('songs').run()

    def add_songs(self, songs: list):
        self.r.db('realMusic').table("songs").insert(songs).run()
