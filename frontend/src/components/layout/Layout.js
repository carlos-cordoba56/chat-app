import { Outlet } from 'react-router-dom'
import './Layout.css'

const Layout = () => {
  return (
    <div className="App">
      <div className="page">
        <Outlet />
      </div>
    </div>
  )
}

export default Layout