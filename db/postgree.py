import psycopg2
from psycopg2.extras import execute_values
from client import models


class DB(object):
    def __init__(self):
        self.conn = psycopg2.connect(dbname='realmusic', host='localhost', port=5532, user='postgres',
                                     password='mysecretpassword')
        self.cur = self.conn.cursor()

    def add_songs(self, songs: list):
        sql = f'INSERT INTO public.songs(like_, genre, name, link, band_name, date_add_to_site) VALUES %s'
        execute_values(self.cur, sql, songs)
        self.conn.commit()

    def get_random_songs(self, size):
        self.cur.execute(f"""SELECT t.*
                  FROM public.songs t
                  WHERE like_='0'
                  ORDER BY RANDOM() limit {size}""")
        songs = self.cur.fetchall()
        songs_list = []
        for song in songs:
            songs_list.append(models.Song(**{'id': song[1], 'name': song[3], 'band_name': song[5], 'link': song[4],
                                             'like': song[0], 'date_add_to_site': song[6], 'genre': song[2]}))

        return songs_list

    def set_song_like_or_dislike(self, _id, like):
        self.cur.execute(f"""UPDATE public.songs SET like_ = {like} WHERE id = {_id}""")
        self.conn.commit()
