from dotenv import load_dotenv
import os

load_dotenv()

DB_URL = os.environ.get("DB_URL")
SECRET_KEY = os.environ.get("SECRET_KEY")
GATEWAY_TIMEOUT = 59
CUSTOMER_SERVICE_URL = 'http://customer_service:8000'
COURIER_SERVICE_URL = 'http://localhost:8001'
EMAIL_SERVICE_URL = 'http://email_service:8000'
RESTAURANT_SERVICE_URL = 'http://restaurant_service:8001'
NOTIFICATION_SERVICE_URL = 'http://notification_service:8000'
