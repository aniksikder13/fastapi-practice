from starlette import status
from uuid import UUID
from typing import Annotated
from datetime import timedelta
from database import SessionDep
from helper.hash_password import verify_pass
from helper.types import AuthRefreshTokenRequest
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from helper.user_management import find_user_by_username
from helper.jwt import get_token, get_payload, save_token_db, remove_expire_token, check_token


router = APIRouter(
    prefix= "/auth",
    tags = ["Auth"]
)


@router.post('/token')
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: SessionDep
):
    # Remove expired tokens
    remove_expire_token(session)

    user = find_user_by_username(form_data.username, session)

    if not user:
        raise HTTPException(
                status_code= status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password"
            )

    if not verify_pass(form_data.password, user.password):
        raise HTTPException(
                status_code= status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password"
            )

    access_token = get_token(
            data = {
                    "user_id": str(user.id),
                    "username": user.username,
                    "role": user.role,
                    "type": "access"
                },
            timedelta=timedelta(minutes=15)
        )

    refresh_token = get_token(
            data = {
                    "user_id": str(user.id),
                    "username": user.username,
                    "role": user.role,
                    "type": "refresh"
                },
            timedelta=timedelta(days=30)
        )

    # Save refresh token in db
    save_token_db(session, user, refresh_token, timedelta(days=30))

    return {
        "token_type": "bearer",
        "access_token": access_token,
        "refresh_token": refresh_token
    }


@router.post("/refresh")
async def login_for_refresh_token(
        req_body: AuthRefreshTokenRequest,
        session: SessionDep
    ):

    # Remove expired tokens
    remove_expire_token(session)

    payload = get_payload(req_body.refresh_token)

    if payload.get('type') != 'refresh':
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Invalid Refresh token"
        )

    token_in_db = check_token(session, UUID(payload.get('user_id')))

    if token_in_db.refresh_token != req_body.refresh_token:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Invalid Refresh token"
        )

    access_token = get_token(
            data = {
                    "user_id": str(payload.get('user_id')),
                    "username": payload.get('username'),
                    "role": payload.get('role'),
                    "type": "access"
                },
            timedelta=timedelta(days=30)
        )

    return {
        "token_type": "bearer",
        "access_token": access_token,
    }
