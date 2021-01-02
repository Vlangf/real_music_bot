from client import models
from client.telega import TelegaBot
from real_rock_parser import RealRockParser
from fastapi import FastAPI, BackgroundTasks
from db.postgree import DB
import time
import uvicorn

app = FastAPI()

bot = TelegaBot()
bot.set_webhook()


def add_songs_to_db_by_genre(genre: str, chat_id: int):
    bot.send_message(message=f'start {time.ctime()}', chat_id=chat_id, parse_mode='html')
    done = RealRockParser().take_all_songs_from_current_genre(genre)
    if done:
        bot.send_message(message=done, chat_id=chat_id, parse_mode='html')
    else:
        bot.send_message(message='Net nichego', chat_id=chat_id, parse_mode='html')


def send_random_songs(chat_id: int, size: int):
    songs = DB().get_random_songs(size)
    for song in songs:
        bot.send_audio(audio=song.link, caption=song.id_, chat_id=chat_id,
                       inline_keyboard=[
                           [{'text': 'like', 'callback_data': '1'}, {'text': 'not like', 'callback_data': '-1'}],
                       ])


@app.post('/songs', status_code=200)
def add_songs(item: models.UpdateResult, background_tasks: BackgroundTasks):
    if item.edited_message:
        return 'ok'

    elif item.callback_query:
        song = item.callback_query.message.caption
        DB().set_song_like_or_dislike(song, item.callback_query.data)
        if item.callback_query.data == '1':
            bot.answer_callback_query(item.callback_query.id, 'like')
        if item.callback_query.data == '-1':
            bot.answer_callback_query(item.callback_query.id, 'DisLike')

    elif item.message.text.startswith('/add_songs'):
        genre = item.message.text.split(' ')[-1]
        background_tasks.add_task(add_songs_to_db_by_genre, genre, item.message.chat.id)

    elif item.message.text.startswith('/grs'):
        size = 1
        if len(item.message.text.split(' ')) > 1:
            size = int(item.message.text.split(' ')[1])
        background_tasks.add_task(send_random_songs, item.message.chat.id, size)


if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=8000)
