import time
import requests
from db.postgree import DB
from bs4 import BeautifulSoup


class RealRockParser():
    def __init__(self):
        self.url = 'https://www.realrocks.ru/music/genres/'

    def take_all_songs_from_current_genre(self, genre):
        genre_url = f'{self.url}{genre}/?page='

        i = 1

        while True:
            if i > 2500:
                break

            page = requests.get(f'{genre_url}{i}')
            if 'Ничего не найдено.' in page.text:
                break

            batch = []
            page_content = BeautifulSoup(page.text, 'html.parser')
            tracs_on_page = page_content.find_all('li',
                                                  class_='level-box track rm-catalog__item sc__'
                                                         'track-item rm-catalog__item_indent_l')

            # noSql
            # for n, track in enumerate(tracs_on_page):
            #     song = {'like': 0, 'genre': genre}
            #     track_name_and_id = track.find(class_='track__title')
            #     song['name'] = track_name_and_id.text
            #     track_id = track_name_and_id['href'].split('/')[-1]
            #     song['link'] = f'https://files.realrocks.ru/lofi/{track_id}/{track_id}.mp3'
            #     song['band_name'] = track.find(class_='track__artist-link').text
            #
            #     date_add_to_site = track.find_all(class_='small-text small-text_size_s track__infbox-item')[-1]['title']
            #     date = date_add_to_site.split(' ')[1].split('.')
            #     song['date_add_to_site'] = f'{date[2]}-{date[1]}-{date[0]}T{date_add_to_site.split(" ")[2]}:00.000Z'
            #
            #     batch.append(song)
            #
            # DB().add_songs(batch)

            # sql
            for n, track in enumerate(tracs_on_page):
                song = [0, genre]
                track_name_and_id = track.find(class_='track__title')
                song.append(track_name_and_id.text)
                track_id = track_name_and_id['href'].split('/')[-1]
                song.append(f'https://files.realrocks.ru/lofi/{track_id}/{track_id}.mp3')
                song.append(track.find(class_='track__artist-link').text)
                date_add_to_site = track.find_all(class_='small-text small-text_size_s track__infbox-item')[-1]['title']
                date = date_add_to_site.split(' ')[1].split('.')
                song.append(f'{date[2]}-{date[1]}-{date[0]}T{date_add_to_site.split(" ")[2]}:00.000Z')

                batch.append(tuple(song))

            DB().add_songs(batch)

            i += 1

        return f'downloading songs from {genre} done {time.ctime()}'
