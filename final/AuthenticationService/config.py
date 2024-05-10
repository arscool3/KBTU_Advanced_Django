from dotenv import load_dotenv
import os

load_dotenv()

DB_URL = os.environ.get("DB_URL1")
SECRET_KEY = os.environ.get("SECRET_KEY")
GATEWAY_TIMEOUT = 59
CUSTOMER_SERVICE_URL = os.environ.get('CUSTOMER_SERVICE_URL')
COURIER_SERVICE_URL = os.environ.get('COURIER_SERVICE_URL')
EMAIL_SERVICE_URL = os.environ.get('EMAIL_SERVICE_URL')
RESTAURANT_SERVICE_URL = os.environ.get('RESTAURANT_SERVICE_URL')
NOTIFICATION_SERVICE_URL = os.environ.get('NOTIFICATION_SERVICE_URL')
