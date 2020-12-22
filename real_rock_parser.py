import requests
from db.mongo import DB
from datetime import datetime
from bs4 import BeautifulSoup


class RealRockParser():
    def __init__(self):
        self.url = 'https://www.realrocks.ru/music/genres/'

    def take_all_songs_from_current_genre(self, genre):
        genre_url = f'{self.url}{genre}/?page='

        i = 1
        while True:
            page = requests.get(f'{genre_url}{i}')
            if 'Ничего не найдено.' in page.text:
                break

            page_content = BeautifulSoup(page.text, 'html.parser')
            tracs_on_page = page_content.find_all('li',
                                                  class_='level-box track rm-catalog__item sc__'
                                                         'track-item rm-catalog__item_indent_l')
            for n, track in enumerate(tracs_on_page):
                song = {'like': 0, 'genre': genre}
                track_name_and_id = track.find(class_='track__title')
                song['name'] = track_name_and_id.text
                track_id = track_name_and_id['href'].split('/')[-1]
                song['link'] = f'https://files.realrocks.ru/lofi/{track_id}/{track_id}.mp3'
                song['band_name'] = track.find(class_='track__artist-link').text

                date_add_to_site = track.find_all(class_='small-text small-text_size_s track__infbox-item')[-1]['title']
                date = date_add_to_site.split(' ')[1].split('.')
                song['date'] = datetime.strptime(
                    f'{date[2]}-{date[1]}-{date[0]}T{date_add_to_site.split(" ")[2]}:00.000Z',
                    '%Y-%m-%dT%H:%M:%S.000Z')

                DB().add_song(song)

            i += 1

        return f'downloading songs from {genre} done'
