from uuid import UUID
from sqlmodel import select
from starlette import status
from typing import Annotated
from model import User
from helper.hash_password import hash_pass
from fastapi import APIRouter, Query, HTTPException
from database import SessionDep
from helper.types import UserCreateRequest, UserResponse

router = APIRouter(
    prefix = "/user",
    tags = ["User"]
)

@router.post("", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
async def create_user(request_body: UserCreateRequest, session: SessionDep):

    statement = select(User).where(User.email == request_body.email)
    existing_user = session.exec(statement).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    user = User(**request_body.model_dump(exclude={"password"}), password=hash_pass(request_body.password))

    session.add(user)
    session.commit()
    session.refresh(user)

    return user
