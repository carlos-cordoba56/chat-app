"""
module for chatroom routers
"""
from datetime import datetime
from fastapi import APIRouter

from app.database.database import chat_rooms, messages
from app.routers.schemas import CreateChatroomRequest, PostMessageRequest


router = APIRouter(
    prefix= '/chatrooms',
    tags=['Chatrooms']
)

@router.get("/")
def get_chatrooms():
    """
    get_chatrooms
    returns all the chatrooms that are created on the application

    Returns:
        List: a list with all the chatrooms
    """
    return chat_rooms

import random
import string

@router.post("/")
def post_chatrooms(request: CreateChatroomRequest):
    """
    post_chatrooms
    creates a chatroom within the application so
    a determined number of users can send messages

    Args:
        request (CreateChatroomRequest): specific request with application required fields
    """
    chat_rooms.append(
        {
            "id":"".join(random.choice(string.ascii_lowercase + string.digits) for i in range(10)),
            "name":request.chatroom_name,
        }
    )
    return chat_rooms

@router.get("/{id}")
def get_messages(id: str):
    """
    get_messages
    returns all the messages from an specific chatroom

    Args:
        id (str): the specific chatroom id

    Returns:
        _type_: _description_
    """
    return [message for message in messages if message["chatroom_id"] == id]

@router.post("/{id}")
def post_message(id: str, message: PostMessageRequest):
    """
    post_message
    method in charge of posting a message in a determined chatroom

    Args:
        id (str): the specific chatroom id
        message (PostMessageRequest): message to be posted

    Returns:
        _type_: _description_
    """
    new_message = message.dict()
    new_message["chatroom_id"] = id
    new_message["time"] = datetime.now()
    messages.append(new_message)
    return messages
