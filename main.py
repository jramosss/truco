from typing import Optional

from fastapi import FastAPI
from api.routers import register,login
from starlette.middleware.cors import CORSMiddleware
import db.models.db

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}


app.include_router(register.router)
app.include_router(login.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)