from uuid import UUID
from sqlmodel import select
from starlette import status
from typing import Annotated
from helper.model import Todo
from contextlib import asynccontextmanager
from fastapi import FastAPI, Query, HTTPException
from helper.database import SessionDep, create_db_and_tables
from helper.types import TodoCreateRequest, TodoUpdateRequest


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 🔵 Startup code
    print("App is starting...")
    create_db_and_tables()

    yield

    # 🔴 Shutdown code
    print("App is shutting down...")


app = FastAPI(lifespan=lifespan)


@app.get('/todo', response_model=list[Todo])
async def read_todos(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 10,):

    statement = select(Todo).offset(offset).limit(limit)
    todo = session.exec(statement).all()
    return todo


@app.get("/todo/{id}", response_model=Todo)
async def read_todo(id: UUID, session: SessionDep):

    todo = session.get(Todo, id)

    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


@app.post("/todo", status_code=status.HTTP_201_CREATED, response_model=Todo)
async def create_todo(todo_request: TodoCreateRequest, session: SessionDep):

    todo = Todo(**todo_request.model_dump())

    session.add(todo)
    session.commit()
    session.refresh(todo)

    return todo


@app.patch("/todo/{id}", status_code=status.HTTP_201_CREATED, response_model=Todo)
async def update_todo(id: UUID, update_request: TodoUpdateRequest, session: SessionDep):

    todo_db = session.get(Todo, id)

    if not todo_db:
        raise HTTPException(status_code=404, detail="Todo not found")

    update_data = update_request.model_dump(exclude_unset=True)

    todo_db.sqlmodel_update(update_data)
    session.add(todo_db)
    session.commit()
    session.refresh(todo_db)

    return todo_db

@app.delete("/todo/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def  delete_todo(id:UUID, session: SessionDep):
    todo_db = session.get(Todo, id)

    if not todo_db:
        raise HTTPException(status_code=404, detail="Todo not found")

    session.delete(todo_db)
    session.commit()

    return None
