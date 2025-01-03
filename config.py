import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
ADMIN_ID_0 = os.getenv('ADMIN_ID_0')
ADMIN_ID_1 = os.getenv('ADMIN_ID_1')
PG_HOST = os.getenv('PG_HOST')
PG_USER = os.getenv('PG_USER')
PG_PASS = os.getenv('PG_PASS')
API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')
