from uuid import UUID
from model import User
from starlette import status
from database import SessionDep
from helper.hash_password import hash_pass
from fastapi import APIRouter, HTTPException
from helper.user_management import find_user_by_username
from helper.types import UserCreateRequest, UserResponse


router = APIRouter(
    prefix = "/user",
    tags = ["User"]
)


@router.post("", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
async def create_user(request_body: UserCreateRequest, session: SessionDep):

    existing_user = find_user_by_username(request_body.username, session)

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="username already registered"
        )

    user = User(
            **request_body.model_dump(exclude={"password"}),
            password=hash_pass(request_body.password)
        )

    session.add(user)
    session.commit()
    session.refresh(user)

    return user


