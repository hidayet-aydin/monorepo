
import os
from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .models import Base

load_dotenv()

host = os.getenv('DB_HOST')
port = os.getenv('DB_PORT')
dbname = os.getenv('DB_NAME')
user = os.getenv('DB_USER')
pswd = os.getenv('DB_PASSWORD')

DATABASE_URL = f"postgresql://{user}:{pswd}@{host}:{port}/{dbname}"
engine = create_engine(DATABASE_URL)


def init():
    Base.metadata.create_all(engine)


Session = sessionmaker(bind=engine)


def get_db():
    session = Session()
    try:
        yield session
    finally:
        session.close()
