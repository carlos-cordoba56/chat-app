"""
module for chatroom routers
"""
import json
from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app import oauth2
from app.database import models
from app.database.database import get_db
from app.services.connections import connection_manager
from app.routers.schemas import (
    CreateChatroomRequest,
    CreateChatroomResponce,
    PostMessageRequest,
    PostMessageResponce
)


router = APIRouter(
    prefix= '/chatrooms',
    tags=['Chatrooms'],
    # Depends = (oauth2.get_current_user)
)

@router.get("/", response_model=List[CreateChatroomResponce])
def get_chatrooms(
    limit: str = 2,
    db: Session = Depends(get_db),
    currrent_user = Depends(oauth2.get_current_user),
) -> List[CreateChatroomResponce]:
    """
    get_chatrooms
    returns all the chatrooms that are created on the application

    Args:
        limit (str): the maximum amount of entries to return

    Returns:
        List[CreateChatroomResponce]: a list with all the chatrooms
    """
    chatrooms = db.query(models.ChatRoom).limit(limit).all()
    return chatrooms

@router.post("/", response_model=CreateChatroomResponce)
def post_chatrooms(
    request: CreateChatroomRequest,
    db: Session = Depends(get_db),
    currrent_user = Depends(oauth2.get_current_user),
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
    new_chatroom = models.ChatRoom(creator_id=currrent_user.id, **request.dict())
    db.add(new_chatroom)
    db.commit()
    db.refresh(new_chatroom)
    return new_chatroom

@router.get("/{id}", 
            # response_model=List[PostMessageResponce]
            )
def get_messages(
    id: str,
    limit: str = 13,
    db: Session = Depends(get_db),
    currrent_user = Depends(oauth2.get_current_user),
):
# ) -> List[PostMessageResponce]:
    """
    get_messages
    returns all the messages from an specific chatroom

    Args:
        id (str): the specific chatroom id
        limit (str): the maximum amount of entries to return

    Returns:
        List[PostMessageResponce]: list with last messages
    """
    messages = db.query(models.Message)\
        .filter(models.Message.chatroom_id == id)\
        .order_by(desc(models.Message.created_at))\
        .limit(limit)\
        .all()
    return messages

@router.post("/{id}", response_model=PostMessageResponce)
async def post_message(
    id: str,
    message: PostMessageRequest,
    db: Session = Depends(get_db),
    currrent_user = Depends(oauth2.get_current_user),
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
    new_message = models.Message(sender_id=currrent_user.id, **message.dict(), chatroom_id=id)
    db.add(new_message)
    db.commit()
    db.refresh(new_message)

    # Broadcast message to all users in the chatroom
    responce = PostMessageResponce(**(new_message.__dict__))\
        .get_dict_representation()
    await connection_manager.broadcast(responce, id)
    return new_message
