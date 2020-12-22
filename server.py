from client import telega
from fastapi import FastAPI, BackgroundTasks
from client import models
from real_rock_parser import RealRockParser

app = FastAPI()
telega.TelegaBot().set_webhook()


def add_songs_to_db_by_genre(genre: str):
    RealRockParser().take_all_songs_from_current_genre(genre)


@app.post('/songs', status_code=200)
def add_songs(item: models.UpdateResult, background_tasks: BackgroundTasks):
    if item.message.text.startswith('/add_songs'):
        genre = item.message.text.split(' ')[-1]
        background_tasks.add_task(add_songs_to_db_by_genre, genre)
