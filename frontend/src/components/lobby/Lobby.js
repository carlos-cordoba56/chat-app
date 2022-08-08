import React, { useState, useEffect } from 'react'
import {Link, useNavigate} from 'react-router-dom'
import { authenticationService } from '../login/loginHelpers'
import './Lobby.css'

const Lobby = () => {
  const [chatrooms, setChatrooms] = useState([])
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const navigate = useNavigate()
  const handleLogOut = (event) => {
    event.preventDefault()
    authenticationService.logout()
    navigate(0, {replace: true })
  }
  const requestOptions = {
    method: 'GET',
    headers: {
      'Authorization': `Bearer ${authenticationService.currentUserValue.access_token}`,
      'accept': 'application/json'
    }
  };

  useEffect(() => {
    fetch(`http://localhost/chatrooms`, requestOptions)
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
      setChatrooms(actualData.slice().reverse());
      setError(null);
    })
    .catch((err) => {
      setError(err.message);
      setChatrooms([]);
    })
    .finally(() => {
      setLoading(false);
    });
    }, []);

  return (
    <div>
      <h1>Coding Challenge</h1>
      <h2>Chat-Rooms</h2>
      <div class="chatrooms">
        {loading && <div>A moment please...</div>}
        {error && (
          <div>{`There is a problem fetching the post data - ${error}`}</div>
        )}
        {chatrooms.map(({ chatroom_id, chatroom_name }) => (
          <Link to="/chatroom"
            state={{ chatroom_id: chatroom_id, name: chatroom_name}}
            >
              {chatroom_name}-{chatroom_id}
          </Link>
        ))}
      </div>
      <div>
        <button
          onClick={handleLogOut}
        >
          Log Out
        </button>
      </div>
    </div>
  )
}

export default Lobby