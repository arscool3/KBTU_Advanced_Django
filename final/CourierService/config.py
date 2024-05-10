from dotenv import load_dotenv
import os

load_dotenv()

DB_URL = os.environ.get("DB_URL1")
SECRET_KEY = os.environ.get("SECRET_KEY")
