from client import models
from client.telega import TelegaBot
from real_rock_parser import RealRockParser
from fastapi import FastAPI, BackgroundTasks

app = FastAPI()

bot = TelegaBot()
bot.set_webhook()


def add_songs_to_db_by_genre(genre: str, chat_id: int):
    done = RealRockParser().take_all_songs_from_current_genre(genre)
    bot.send_message(message=done, chat_id=chat_id, parse_mode='html')


@app.post('/songs', status_code=200)
def add_songs(item: models.UpdateResult, background_tasks: BackgroundTasks):
    if item.message.text.startswith('/add_songs'):
        genre = item.message.text.split(' ')[-1]
        background_tasks.add_task(add_songs_to_db_by_genre, genre, item.message.chat.id)
