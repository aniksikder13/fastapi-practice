from model import User
from sqlmodel import select
from database import SessionDep


def find_user_by_username(username:str, session: SessionDep):
    statement = select(User).where(User.username == username)
    user = session.exec(statement).first()

    return user
