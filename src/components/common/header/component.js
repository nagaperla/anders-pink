import React from 'react'
import { Link } from 'react-router-dom';

const HeaderComponent = (props) => {
  const location = {
    pathname: '/bookmarks'
  };

  return (
    <nav className="navbar navbar-expand-lg navbar-light bg-light">
      <span className="navbar-brand">Anders Pink</span>

      <div className="collapse navbar-collapse" id="navbarSupportedContent">
        <ul className="navbar-nav mr-auto">
          <li className={`nav-item ${location.pathname === '/' && "active"}`}>
            <Link to="/" className="nav-link">Home</Link>
          </li>
          <li className={`nav-item ${location.pathname === '/bookmarks' && "active"}`}>
            <Link to="/bookmarks" className="nav-link">Bookmarks</Link>
          </li>
        </ul>
      </div>
    </nav>
  )
}

export default HeaderComponent
