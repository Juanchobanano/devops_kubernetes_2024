import os
from sqlmodel import create_engine


PORT = int(os.environ.get("PORT", 8002))

POSTGRES_DB = os.environ.get("POSTGRES_DB", None)
POSTGRES_USER = os.environ.get("POSTGRES_USER", None)
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD", None)
DATABASE_PORT = os.environ.get("DATABASE_PORT", None)
DATABASE_HOST = os.environ.get("DATABASE_HOST", None)
MAX_CHARACTERS = 140
NATS_ENDPOINT = os.environ.get("NATS_ENDPOINT", None)

DATABASE_URL = (
    f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}"
    f"@{DATABASE_HOST}:{DATABASE_PORT}/{POSTGRES_DB}"
)
#  DATABASE_URL = "sqlite:///database.db"
print(f"DATABASE_URL={DATABASE_URL}")
engine = create_engine(DATABASE_URL)
