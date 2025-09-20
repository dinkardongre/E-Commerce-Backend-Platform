from fastapi import FastAPI
from src.db.db import Base, engine
from src.routes.user_routes import userRouter

Base.metadata.create_all(engine)

server = FastAPI()
server.include_router(userRouter)


@server.get("/")
def welcome():
    return "Code is working fine"