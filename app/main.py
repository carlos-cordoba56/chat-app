"""
main file for application
"""
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from app.settings import settings
from app.routers.chatrooms import router
from app.database.database import engine
from app.database.models import Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(router)


@app.get("/", response_class=HTMLResponse)
async def home():
    """
    Root end-point for chat app
    """
    return f"this is the coolest chat-app name {settings.app_name}"
