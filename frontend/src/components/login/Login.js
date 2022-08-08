import React from 'react'
import './Login.css'
import { useNavigate } from 'react-router-dom';
import { authenticationService } from './loginHelpers'


const Login = () => {
  const navigate = useNavigate();
  const handlesubmit = (event) => {
    event.preventDefault()
    const user = authenticationService.login(event.target[0].value, event.target[1].value)
    event.target[0].value  = ''
    event.target[1].value  = ''
    if (user) {
      navigate(0, { replace: true })
    }
  }
  return (
    <>
      <h1>Coding Challenge</h1>
      <h2>Financial Chat</h2>
      <form onSubmit={handlesubmit} id='login-form'>
          <div>
              <legend for="username">Username:</legend>
              <input
                type="text"
                name="username"
              />
          </div>
          <div>
              <legend for="password">Password:</legend>
              <input
                type="password"
                name="password"
              />
          </div>
          <div>
              <input type="submit"/>
          </div>
      </form>
    </>
  )
}

export default Login