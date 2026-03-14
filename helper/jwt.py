import os
from uuid import UUID
from model import Token
from starlette import status
from fastapi import HTTPException
from sqlmodel import delete, Session, select
from helper.types import UserResponse
from datetime import datetime, timezone
from jose import jwt, JWTError, ExpiredSignatureError



def get_token(data:dict, timedelta ):

    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta
    to_encode.update({'exp': expire})

    token = jwt.encode(
                to_encode,
                os.environ['SECRET_KEY'],
                algorithm = os.environ['ALGORITHM']
            )
    return token


def get_payload(refresh_token:str):
    try:
        payload = jwt.decode(
                    refresh_token,
                    os.environ['SECRET_KEY'],
                    algorithms = [os.environ['ALGORITHM']]
                )
        return payload

    except ExpiredSignatureError:
        raise HTTPException(
                    status_code = status.HTTP_401_UNAUTHORIZED,
                    detail = "Token is expired"
                )

    except JWTError:
          raise HTTPException(
                    status_code = status.HTTP_401_UNAUTHORIZED,
                    detail = "Token is invalid"
                )


def remove_expire_token(session: Session):

    now = datetime.now(timezone.utc)
    statement = delete(Token).where(Token.expire < now)
    session.exec(statement)
    session.commit()


def check_token(session: Session, user_id: UUID):
    statement = select(Token).where(Token.user_id == user_id)
    exist_token = session.exec(statement).first()
    return exist_token


def save_token_db(session: Session, user: UserResponse, token: str, delta_expire):
    exist_token = check_token(session, user.id)
    expire_time = datetime.now(timezone.utc) + delta_expire

    if exist_token:
        exist_token.refresh_token = token
        exist_token.expire = expire_time
        session.add(exist_token)
    else:
        token_to_store = Token(
            user_id = user.id,
            refresh_token = token,
            expire = expire_time
        )
        session.add(token_to_store)

    session.commit()

