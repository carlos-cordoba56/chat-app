"""
Validation schemas for routers
"""
from datetime import datetime
import json
from pydantic import BaseModel


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
    class Config:
        orm_mode = True
    
    # @classmethod
    def get_dict_representation(self):
        return json.loads(self.json())
