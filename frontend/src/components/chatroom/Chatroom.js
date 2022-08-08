import React, { useState, useEffect, useRef } from 'react'
import {useLocation, Link} from "react-router-dom";
import useWebSocket, { ReadyState } from 'react-use-websocket';
import { authenticationService } from '../login/loginHelpers'
import './Chatroom.css'

const renderMessage = ({chatroom_id, message, created_at, sender_id}) => {
  return (<div className='message' key={chatroom_id}>
            <p><span>from:</span> {sender_id} at:{created_at}</p>
            <p>{message}</p>
          </div>)
}

const Chatroom = () => {
  // const [data, setData] = useState([]);
  const [messageHistory, setMessageHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const location = useLocation()
  const {chatroom_id, name} = location.state

  const inputRef = useRef(null);

  const requestOptions = {
    method: 'GET',
    headers: {
      'Authorization': `Bearer ${authenticationService.currentUserValue.access_token}`,
      'accept': 'application/json'
    }
  };

  useEffect(() => {
    fetch(`http://localhost/chatrooms/${chatroom_id}`, requestOptions)
    .then((response) => {
      if (!response.ok) {
        throw new Error(
          `This is an HTTP error: The status is ${response.status}`
        );
      }
      return response.json();
    })
    .then((actualData) => {
      console.log(actualData)
      setMessageHistory(actualData.slice().reverse());
      setError(null);
    })
    .catch((err) => {
      setError(err.message);
      setMessageHistory([]);
    })
    .finally(() => {
      setLoading(false);
    });
    }, []);
  
    // const [socketUrl, setSocketUrl] = useState(`ws://localhost/ws/${chatroom_id}`);
    const socketUrl = `ws://localhost/ws/${chatroom_id}`;

    const { sendMessage, lastMessage, readyState } = useWebSocket(socketUrl);

    useEffect(() => {
      if (lastMessage !== null) {
        console.log(lastMessage.data)
        setMessageHistory((prev) => prev.concat(JSON.parse(lastMessage.data)));
      }
    }, [lastMessage, setMessageHistory]);

    // const handleClickChangeSocketUrl = useCallback(
    //   () => setSocketUrl('wss://demos.kaazing.com/echo'),
    //   []
    // );

    // const connectionStatus = {
    //   [ReadyState.CONNECTING]: 'Connecting',
    //   [ReadyState.OPEN]: 'Open',
    //   [ReadyState.CLOSING]: 'Closing',
    //   [ReadyState.CLOSED]: 'Closed',
    //   [ReadyState.UNINSTANTIATED]: 'Uninstantiated',
    // }[readyState];

    const handleClickSendMessage = (event) => {
      event.preventDefault();
      sendMessage(`{"message":"${inputRef.current.value}", "sender_id":"1"}`);
      console.log(inputRef.current.value)
      inputRef.current.value = ''
      };

  return (
    <>
      <h1>Chatroom {name} {chatroom_id}</h1>
      <h2>Your username: <span id="ws-id">{authenticationService.currentUserValue.username}</span></h2>
      <div class="message-stack" id="message-stack">
        {loading && <div>A moment please...</div>}
        {error && (
          <div>{`There is a problem fetching the post data - ${error}`}</div>
        )}
        {messageHistory && messageHistory.map(({ chatroom_id, message, created_at, sender_id }) => (
          renderMessage({ chatroom_id, message, created_at, sender_id })
          ))}
      </div>
      <form action="" onsubmit="sendMessage(event)">
        <input
          type="text"
          id="messageText"
          ref={inputRef}
          autocomplete="off"
          onSubmit={handleClickSendMessage}
        />
        <button
          onClick={handleClickSendMessage}
          disabled={readyState !== ReadyState.OPEN}
        >
          Send
        </button>
      </form>
      <ul id='messages'>
      </ul>
      <div>
          <Link to="/lobby">Return</Link>
      </div>
    </>
  )
}

export default Chatroom