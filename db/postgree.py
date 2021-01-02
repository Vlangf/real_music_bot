import psycopg2
from psycopg2.extras import execute_values


class DB(object):
    def __init__(self):
        self.conn = psycopg2.connect(dbname='realmusic', host='localhost', port=5532, user='postgres',
                                     password='mysecretpassword')
        self.cur = self.conn.cursor()

    def add_songs(self, songs: list):
        sql = f'INSERT INTO public.songs(like_,  genre, name, link, band_name, date_add_to_site) VALUES %s'
        execute_values(self.cur, sql, songs)
        self.conn.commit()


