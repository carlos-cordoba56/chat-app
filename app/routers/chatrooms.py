"""
module for chatroom routers
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.database.models import ChatRoom, Message
from app.routers.schemas import CreateChatroomRequest, PostMessageRequest


router = APIRouter(
    prefix= '/chatrooms',
    tags=['Chatrooms']
)

@router.get("/")
def get_chatrooms(db: Session = Depends(get_db)):
    """
    get_chatrooms
    returns all the chatrooms that are created on the application

    Returns:
        List: a list with all the chatrooms
    """
    chatrooms = db.query(ChatRoom).all()
    return chatrooms

@router.post("/")
def post_chatrooms(
    request: CreateChatroomRequest,
    db: Session = Depends(get_db)
):
    """
    post_chatrooms
    creates a chatroom within the application so
    a determined number of users can send messages

    Args:
        request (CreateChatroomRequest): specific request with application required fields
    """
    new_chatroom = ChatRoom(**request.dict())
    db.add(new_chatroom)
    db.commit()
    db.refresh(new_chatroom)
    return new_chatroom

@router.get("/{id}")
def get_messages(id: str, db: Session = Depends(get_db)):
    """
    get_messages
    returns all the messages from an specific chatroom

    Args:
        id (str): the specific chatroom id

    Returns:
        _type_: _description_
    """
    messages = db.query(Message).filter(Message.chatroom_id == id).all()
    return messages

@router.post("/{id}")
def post_message(id: str, message: PostMessageRequest, db: Session = Depends(get_db)):
    """
    post_message
    method in charge of posting a message in a determined chatroom

    Args:
        id (str): the specific chatroom id
        message (PostMessageRequest): message to be posted

    Returns:
        _type_: _description_
    """
    new_message = Message(**message.dict(), chatroom_id=id)
    db.add(new_message)
    db.commit()
    db.refresh(new_message)
    return new_message
