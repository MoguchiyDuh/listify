from dotenv import load_dotenv
from os import environ

load_dotenv()

DB_URL = f"postgresql+psycopg2://{environ.get('DB_USERNAME')}:{environ.get('DB_PASSWORD')}@localhost/{environ.get('DB_NAME')}"
ASYNC_DB_URL = DB_URL.replace("psycopg2", "asyncpg")
TEST_DB_URL = DB_URL.replace(environ.get("DB_NAME"), "test_db")
ASYNC_TEST_DB_URL = TEST_DB_URL.replace("psycopg2", "asyncpg")
SECRET_KEY = environ.get("SECRET_KEY")
RAWG_API_KEY = environ.get("RAWG_API_KEY")
TMDB_API_KEY = environ.get("TMDB_API_KEY")
