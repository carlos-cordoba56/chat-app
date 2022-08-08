"""
main file for application
"""
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
# from app import oauth2
from app.routers.schemas import PostMessageResponce

from app.settings import settings
from app.routers import chatrooms, users, auth
from app.database.database import engine, get_db
from app.database.models import Base
from app.database.models import Message
from app.services.connections import ChatroomConnection, connection_manager

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(chatrooms.router)
app.include_router(users.router)
app.include_router(auth.router)

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", response_class=HTMLResponse)
async def home():
    """
    Root end-point for chat app
    """
    return f"this is the coolest chat-app name {settings.app_name}"

from fastapi import WebSocket, WebSocketDisconnect
@app.websocket("/ws/{id}")
async def chat_websocket_endpoint(
    websocket: WebSocket,
    id: str,
    db: Session = Depends(get_db),
    # currrent_user = Depends(oauth2.get_current_user),
):
    """
    chat_websocket_endpoint
    socket to mantain the connection between server and client

    Args:
        websocket (WebSocket): socket objec to cummunicate with the client
        id (str): the id from the chatroom to broadcast the message to
    """
    connection = ChatroomConnection(websocket, id)
    await connection_manager.connect(connection)
    try:
        while True:
            # receive information
            data = await websocket.receive_json()
            # save message in the db
            new_message = Message(
                message=data["message"],
                chatroom_id=id,
                sender_id=data["sender_id"]
            )
            db.add(new_message)
            db.commit()
            db.refresh(new_message)

            # Broadcast message to all users in the chatroom
            responce = PostMessageResponce(**(new_message.__dict__))\
                .get_dict_representation()
            await connection_manager.broadcast(responce, id)

    except WebSocketDisconnect:
        connection_manager.disconnect(connection)
