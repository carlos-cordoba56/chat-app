"""
Validation schemas for routers
"""
from pydantic import BaseModel

class CreateChatroomRequest(BaseModel):
    """
    CreateChatroomRequest
    validation schema for creation of a chatroom
    """
    chatroom_name: str

class PostMessageRequest(BaseModel):
    """
    PostMessageRequest
    validation schema for posting of a message
    on a chatroom
    """
    message: str
