from decouple import config
from ensta import Host

import database


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_bot():
    bot = Host(config('LOGIN'), config('PASSWORD'))
    return bot
