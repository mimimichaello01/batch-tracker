import os

from dotenv import load_dotenv

load_dotenv()


SYNC_DATABASE_URL = (
    f'postgresql+psycopg2://{os.getenv("POSTGRES_USER")}:'
    f'{os.getenv("POSTGRES_PASSWORD")}@{os.getenv("POSTGRES_HOST")}:'
    f'{os.getenv("POSTGRES_PORT")}/{os.getenv("POSTGRES_NAME")}'
)

DATABASE_URL = (
    f'postgresql+asyncpg://{os.getenv("POSTGRES_USER")}:'
    f'{os.getenv("POSTGRES_PASSWORD")}@{os.getenv("POSTGRES_HOST")}:'
    f'{os.getenv("POSTGRES_PORT")}/{os.getenv("POSTGRES_NAME")}'
)
