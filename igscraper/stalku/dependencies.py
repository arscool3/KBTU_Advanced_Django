import database
from decouple import config
from ensta import Web


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_bot():
    bot = Web(config('LOGIN'), config('PASSWORD'))
    return bot
