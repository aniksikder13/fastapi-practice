import os
from starlette import status
from fastapi import HTTPException
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
