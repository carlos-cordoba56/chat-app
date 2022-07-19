"""
Tabel models for chat application
"""
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from .database import Base

# class User(Base):
#     __tablename__ = 'users'

#     id = Column(Integer, primary_key=True, nullable=False)
#     email = Column(String, nullable=False, unique=True)
#     password = Column(String, nullable=False)
#     created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('NOW()'))

class ChatRoom(Base):
    __tablename__ = 'chatroom'

    chatroom_id = Column(Integer, primary_key=True, nullable=False)
    chatroom_name = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('NOW()'))
    # owner_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)

    # owner = relationship("User")

class Message(Base):
    __tablename__ = 'message'
    
    id = Column(Integer, primary_key=True, nullable=False)
    chatroom_id = Column(Integer, ForeignKey('chatroom.chatroom_id', ondelete='CASCADE'), nullable=False)
    message = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('NOW()'))
    # owner_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)

    # owner = relationship("User")