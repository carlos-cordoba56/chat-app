"""
Validation schemas for routers
"""
import json
from datetime import datetime
from pydantic import BaseModel


class UserResponce(BaseModel):
    username: str
    email: str

    class Config:
        orm_mode = True

class User(UserResponce):
    password: str


class CreateChatroomRequest(BaseModel):
    """
    CreateChatroomRequest
    validation schema for creation of a chatroom
    """
    chatroom_name: str

class CreateChatroomResponce(CreateChatroomRequest):
    """
    CreateChatroomResponce
    validation schema for completed chatroom request
    """
    chatroom_id: str
    created_at: datetime
    class Config:
        orm_mode = True

class PostMessageRequest(BaseModel):
    """
    PostMessageRequest
    validation schema for posting of a message
    on a chatroom
    """
    message: str

class PostMessageResponce(PostMessageRequest):
    """
    PostMessageResponce
    validation schema for message posted on the chatroom
    """
    chatroom_id: str
    created_at: datetime
    # sender_id: UserResponce
    class Config:
        orm_mode = True
    
    # @classmethod
    def get_dict_representation(self):
        return json.loads(self.json())
