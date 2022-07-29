from typing import Any, Dict, List

from fastapi import WebSocket


class ChatroomConnection:
    """
    ChatroomConnection
    connection object that contains the socket objec and chatroom
    where the object is connected
    """
    def __init__(self, websocket, chatroom_id) -> None:
        self.socket: WebSocket = websocket
        self.chatroom: str = chatroom_id


class ConnectionManager:
    """
    ConnectionManager
    object to record websockets objects created on the server
    """
    def __init__(self):
        self.active_connections: List[ChatroomConnection] = []

    async def connect(self, connection: ChatroomConnection):
        """
        connect
        it connects and record the web socket object to communicate with the client

        Args:
            connection (ChatroomConnection): connection object
        """
        await connection.socket.accept()
        self.active_connections.append(connection)

    def disconnect(self, connection: ChatroomConnection):
        """
        disconnect
        shut down the connection in a socket and removes it from the record

        Args:
            connection (ChatroomConnection): connection object
        """
        self.active_connections.remove(connection)

    async def broadcast(self, message: Dict[str, Any], chatroom_id: str):
        """
        broadcast
        share all the messages with all the clients connected to the same chatroom

        Args:
            message (Dict[str, Any]): message to be send to all clients
            chatroom_id (str): the id where the object will send the message
        """
        for connection in self.active_connections:
            if connection.chatroom == chatroom_id:
                await connection.socket.send_json(message)

connection_manager = ConnectionManager()
