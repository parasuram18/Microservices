import os
from dotenv import load_dotenv
load_dotenv()


SYNC_DB_URL = os.getenv('SYNC_DB_URL')
ASYNC_DB_URL = os.getenv('ASYNC_DB_URL')
