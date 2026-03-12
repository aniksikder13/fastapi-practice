from starlette import status
from typing import Annotated
from datetime import timedelta
from database import SessionDep
from helper.hash_password import verify_pass
from helper.jwt import get_token, get_payload
from helper.types import AuthRefreshTokenRequest
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from helper.user_management import find_user_by_username


router = APIRouter(
    prefix= "/auth",
    tags = ["Auth"]
)


@router.post('/token')
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: SessionDep
):
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
                    "sub": str(user.id),
                    "type": "access"
                },
            timedelta=timedelta(minutes=15)
        )

    refresh_token = get_token(
            data = {
                    "sub": str(user.id),
                    "type": "refresh"
                },
            timedelta=timedelta(minutes=15)
        )


    return {
        "token_type": "bearer",
        "access_token": access_token,
        "refresh_token": refresh_token
    }


@router.post("/refresh")
async def login_for_refresh_token(req_body: AuthRefreshTokenRequest):
    payload = get_payload(req_body.refresh_token)

    if payload.get('type') != 'refresh':
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Invalid Refresh token"
        )

    access_token = get_token(
            data = {
                    "sub": str(payload.get('sub')),
                    "type": "access"
                },
            timedelta=timedelta(minutes=15)
        )

    return {
        "token_type": "bearer",
        "access_token": access_token
    }
