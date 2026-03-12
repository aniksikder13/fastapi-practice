from fastapi import FastAPI
from contextlib import asynccontextmanager
from routers.todo import router as todo_router
from routers.user import router as user_router
from routers.auth import router as auth_router
from database import create_db_and_tables
from dotenv import load_dotenv


load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 🔵 Startup code
    print("App is starting...")
    create_db_and_tables()

    yield

    # 🔴 Shutdown code
    print("App is shutting down...")


app = FastAPI(lifespan=lifespan)

app.include_router(auth_router)
app.include_router(todo_router)
app.include_router(user_router)
