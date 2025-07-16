from dotenv import load_dotenv
import os

load_dotenv()

ASYNC_DB_URL = os.getenv('ASYNC_DB_URL')
SYNC_DB_URL = os.getenv('SYNC_DB_URL')
SECRET_KEY = os.getenv('SECRET_KEY')
JWT_EXPIRE_TIME = os.getenv('JWT_EXPIRE_TIME')
JWT_AUTH_HEADER_PREFIX = os.getenv('JWT_AUTH_HEADER_PREFIX')
JWT_ALGORITHM = os.getenv('JWT_ALGORITHM')