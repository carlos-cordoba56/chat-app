import { Route, Routes, Navigate } from 'react-router-dom'
import './App.css';
import Chatroom from './components/chatroom/Chatroom';
import Layout from './components/layout/Layout';
import Lobby from './components/lobby/Lobby';
import Login from './components/login/Login';
import { authenticationService } from './components/login/loginHelpers';


function App() {
  return (
    <>
      <Routes>
        <Route path="/" element={<Layout/>}>
          <Route index element={<Navigate to="/lobby" />}/>
          <Route path="lobby" element={
          authenticationService.currentUserValue === null? <Navigate to="/login"/>: <Lobby/>}
          />
          <Route path="chatroom" element={<Chatroom/>} />
          <Route path="login" element={
          authenticationService.currentUserValue === null? <Login/>: <Navigate to="/lobby"/>}
          />
        </Route>
      </Routes>
    </>
  );
}

export default App;
