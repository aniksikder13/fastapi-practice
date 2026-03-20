import os
import time
import psycopg2
from typing import Annotated

from fastapi import Depends
from sqlmodel import Session, SQLModel, create_engine

DATABASE_SOURCE = os.environ.get('DATABASE_URL')

engine = create_engine(DATABASE_SOURCE)

def wait_for_db(max_retries=10, delay=2):
    for i in range(max_retries):
        try:
            with engine.connect() as conn:
                print("✅ Database is ready!")
                return
        except psycopg2.OperationalError:
            print(f"⏳ Waiting for database... retry {i+1}/{max_retries}")
            time.sleep(delay)
    raise RuntimeError("❌ Database not ready after multiple retries.")


def create_db_and_tables():
    wait_for_db()
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
