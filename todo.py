from sqlmodel import select
from typing import Annotated
from helper.model import Todo
from contextlib import asynccontextmanager
from fastapi import FastAPI, Query, HTTPException
from helper.database import SessionDep, create_db_and_tables

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 🔵 Startup code
    print("App is starting...")
    create_db_and_tables()

    yield

    # 🔴 Shutdown code
    print("App is shutting down...")


app = FastAPI(lifespan=lifespan)


@app.get('/todo')
async def TodoLists(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=10)] = 10,):

    todo = session.exec(select(Todo).offset(offset).limit(limit)).all()
    return todo