from typing import Optional

from fastapi import FastAPI
from api.routers import users,room
from starlette.middleware.cors import CORSMiddleware
from db.models.db import define

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

define(provider='sqlite', filename='db.sqlite', create_db=True)

app.include_router(users.router)
app.include_router(room.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
