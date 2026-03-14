from model import User
from sqlmodel import select
from database import SessionDep
from helper.jwt import remove_expire_token

def find_user_by_username(username:str, session: SessionDep):

    # Remove expired tokens
    remove_expire_token(session)

    statement = select(User).where(User.username == username)
    user = session.exec(statement).first()

    return user
