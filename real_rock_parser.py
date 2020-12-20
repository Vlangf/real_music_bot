import requests
from bs4 import BeautifulSoup


class RealRockParser():
    def __init__(self):
        self.url = 'https://www.realrocks.ru/music/genres/'
        self.genres = [
            'expirement_rock',
            # 'alternative_metal', 'alternative_rock', 'bard_rock', 'bebop', 'black_metal',
            # 'blues_rock', 'britpop', 'glam_rock', 'gothic_rock', 'graindcor', 'granj', 'jazz_rock',
            # 'dum_metaldat_metal', 'dat_metal', 'indi_pop', 'indie_rock', 'instrumental_metal', 'instrument_rock',
            # 'punk', 'pop_pank', 'pop_rock', 'postpunk', 'post_rock', 'progressive_metal', 'progressive_rock',
            # 'psychedelic_rock', 'rock_n_roll', 'rapkor', 'sympho_rock', 'ska_pank', 'soft_rock', 'thrash_metal',
            # 'hard_rock', 'folk_rock', 'heavy_metal'
        ]

    def take_all_songs_from_current_genre(self, genre):
        genge_url = f'{self.url}{genre}/?page='
        i = 2
        # while True:
        page = requests.get(f'{genge_url}{i}')
        if 'Ничего не найдено.' in page.text:
            # break
            print('net nihuy')

        page_content = BeautifulSoup(page.text, 'html.parser')
        tracs_on_page = page_content.find_all('li',
                                              class_='level-box track rm-catalog__item sc__track-item rm-catalog__item_indent_l')
        for n, track in enumerate(tracs_on_page):
            track_name_and_id = track.find(class_='track__title')
            track_name = track_name_and_id.text
            track_id = track_name_and_id['href'].split('/')[-1]
            track_link = f'https://files.realrocks.ru/lofi/{track_id}/{track_id}.mp3'
            band_name = track.find(class_='track__artist-link').text

            date_add_to_site = track.find_all(class_='small-text small-text_size_s track__infbox-item')[-1]['title']
            date = date_add_to_site.split(' ')[1].split('.')
            iso_date_time = f'{date[2]}-{date[1]}-{date[0]}T{date_add_to_site.split(" ")[2]}:00.000000'
            print(n + 1, track_name, band_name, track_link)

    def take_all_songs_from_genres(self):
        pass


RealRockParser().take_all_songs_from_current_genre('folk_rock')
