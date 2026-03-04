from uuid import UUID
from sqlmodel import select
from starlette import status
from typing import Annotated
from model import Todo
from fastapi import APIRouter, Query, HTTPException
from database import SessionDep
from helper.types import TodoCreateRequest, TodoUpdateRequest

router = APIRouter(
    prefix = "/todo",
    tags = ["Todo"]
)

@router.get('', response_model=list[Todo])
async def read_todos(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 10,):

    statement = select(Todo).offset(offset).limit(limit)
    todo = session.exec(statement).all()
    return todo


@router.get("/{id}", response_model=Todo)
async def read_todo(id: UUID, session: SessionDep):

    todo = session.get(Todo, id)

    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


@router.post("", status_code=status.HTTP_201_CREATED, response_model=Todo)
async def create_todo(request_body: TodoCreateRequest, session: SessionDep):

    todo = Todo(**request_body.model_dump())

    session.add(todo)
    session.commit()
    session.refresh(todo)

    return todo


@router.patch("/{id}", status_code=status.HTTP_201_CREATED, response_model=Todo)
async def update_todo(id: UUID, request_body: TodoUpdateRequest, session: SessionDep):

    todo_db = session.get(Todo, id)

    if not todo_db:
        raise HTTPException(status_code=404, detail="Todo not found")

    update_data = request_body.model_dump(exclude_unset=True)

    todo_db.sqlmodel_update(update_data)
    session.add(todo_db)
    session.commit()
    session.refresh(todo_db)

    return todo_db

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def  delete_todo(id:UUID, session: SessionDep):
    todo_db = session.get(Todo, id)

    if not todo_db:
        raise HTTPException(status_code=404, detail="Todo not found")

    session.delete(todo_db)
    session.commit()

    return None
