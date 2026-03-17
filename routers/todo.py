from uuid import UUID
from model import Todo
from sqlmodel import select
from starlette import status
from typing import Annotated
from database import SessionDep
from helper.jwt import get_current_user
from fastapi import APIRouter, Query, HTTPException, Depends
from helper.types import TodoCreateRequest, TodoUpdateRequest


router = APIRouter(
    prefix = "/todo",
    tags = ["Todo"]
)


user_dependency = Annotated[dict, Depends(get_current_user)]


@router.get('', response_model=list[Todo])
async def read_todos(
        session: SessionDep,
        user: user_dependency,
        offset: int = 0,
        limit: Annotated[int, Query(le=100)] = 10,
    ):
    print(user)
    if user is None:
        raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication Failed"
            )

    if user.get('role') == 'admin':
        statement = select(Todo)
    else:
        statement = select(Todo).where(Todo.user_id == user.get('id'))

    statement = statement.offset(offset).limit(limit)
    todo = session.exec(statement).all()
    return todo


@router.get("/{id}", response_model=Todo)
async def read_todo(
        id: UUID,
        session: SessionDep,
        user: user_dependency
    ):

    if user is None:
        raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication Failed"
            )

    if user.get('role') == 'admin':
        statement = select(Todo).where(Todo.id == id)
    else:
        statement = select(Todo).where(
                Todo.id == id,
                Todo.user_id == user.get('id')
            )

    todo = session.exec(statement).first()

    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    return todo


@router.post("", status_code=status.HTTP_201_CREATED, response_model=Todo)
async def create_todo(
        session: SessionDep,
        user: user_dependency,
        request_body: TodoCreateRequest
    ):

    if user is None:
        raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication Failed"
            )

    todo = Todo(
            **request_body.model_dump(),
            user_id = user.get('id')
        )

    session.add(todo)
    session.commit()
    session.refresh(todo)

    return todo


@router.patch("/{id}", status_code=status.HTTP_201_CREATED, response_model=Todo)
async def update_todo(
        id: UUID,
        session: SessionDep,
        user: user_dependency,
        request_body: TodoUpdateRequest
    ):

    if user is None:
        raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication Failed"
            )

    statement = select(Todo).where(
        Todo.id == id,
        Todo.user_id == user.get('id')
    )

    todo_db = session.exec(statement).first()

    if not todo_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")

    update_data = request_body.model_dump(exclude_unset=True)

    todo_db.sqlmodel_update(update_data)
    session.add(todo_db)
    session.commit()
    session.refresh(todo_db)

    return todo_db


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def  delete_todo(
        id: UUID,
        session: SessionDep,
        user: user_dependency
    ):

    if user is None:
        raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication Failed"
            )

    statement = select(Todo).where(
        Todo.id == id,
        Todo.user_id == user.get('id')
    )

    todo_db = session.exec(statement).first()

    if not todo_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")

    session.delete(todo_db)
    session.commit()

    return None
