"""
module for chatroom routers
"""
import json
from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import desc, inspect

from app.database.database import get_db
from app.database.models import ChatRoom, Message
from app.routers.schemas import CreateChatroomRequest, CreateChatroomResponce, PostMessageRequest, PostMessageResponce
from app.services.connections import connection_manager


router = APIRouter(
    prefix= '/chatrooms',
    tags=['Chatrooms']
)

@router.get("/", response_model=List[CreateChatroomResponce])
def get_chatrooms(
    limit: str = 2,
    db: Session = Depends(get_db)
) -> List[CreateChatroomResponce]:
    """
    get_chatrooms
    returns all the chatrooms that are created on the application

    Args:
        limit (str): the maximum amount of entries to return

    Returns:
        List[CreateChatroomResponce]: a list with all the chatrooms
    """
    chatrooms = db.query(ChatRoom).limit(limit).all()
    return chatrooms

@router.post("/", response_model=CreateChatroomResponce)
def post_chatrooms(
    request: CreateChatroomRequest,
    db: Session = Depends(get_db)
) -> CreateChatroomResponce:
    """
    post_chatrooms
    creates a chatroom within the application so
    a determined number of users can send messages

    Args:
        request (CreateChatroomRequest): specific request with application required fields

    Returns:
        CreateChatroomResponce: metadata for created chatroom
    """
    new_chatroom = ChatRoom(**request.dict())
    db.add(new_chatroom)
    db.commit()
    db.refresh(new_chatroom)
    return new_chatroom

@router.get("/{id}", response_model=List[PostMessageResponce])
def get_messages(
    id: str,
    limit: str = 13,
    db: Session = Depends(get_db)
) -> List[PostMessageResponce]:
    """
    get_messages
    returns all the messages from an specific chatroom

    Args:
        id (str): the specific chatroom id
        limit (str): the maximum amount of entries to return

    Returns:
        List[PostMessageResponce]: list with last messages
    """
    messages = db.query(Message)\
        .filter(Message.chatroom_id == id)\
        .order_by(desc(Message.created_at))\
        .limit(limit).all()
    return messages

@router.post("/{id}", response_model=PostMessageResponce)
async def post_message(
    id: str,
    message: PostMessageRequest,
    db: Session = Depends(get_db)
) -> PostMessageResponce:
    """
    post_message
    method in charge of posting a message in a determined chatroom

    Args:
        id (str): the specific chatroom id
        message (PostMessageRequest): message to be posted

    Returns:
        PostMessageResponce: responce message after posting message
    """
    # Save message into the database
    new_message = Message(**message.dict(), chatroom_id=id)
    db.add(new_message)
    db.commit()
    db.refresh(new_message)

    # Broadcast message to all users in the chatroom
    responce = PostMessageResponce(**(new_message.__dict__))\
        .get_dict_representation()
    await connection_manager.broadcast(responce, id)
    return new_message
