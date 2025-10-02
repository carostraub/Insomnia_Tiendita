import React from "react";
import { Link } from "react-router";

const Navbar = () => {
  return (
    <nav className="navbar navbar-expand-lg bg-body-tertiary">
      <div className="container-fluid">
        <Link className="navbar-brand" to="/">
        <img
        src="/logo borde blanco.png"
        />
        </Link>
        <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
          <span className="navbar-toggler-icon"></span>
        </button>
        <div className="collapse navbar-collapse" id="navbarSupportedContent">
          <ul className="navbar-nav me-auto mb-2 mb-lg-0">
            <li className="nav-item">
              <Link className="nav-link active" aria-current="page" href="#">Instagram</Link>
            </li>

            <li className="nav-item dropdown">
              <a className="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                Productos
              </a>
              <ul className="dropdown-menu">
                <li><Link className="dropdown-item" href="#">Totebags</Link></li>
                <li><Link className="dropdown-item" href="#">Ilustraciones</Link></li>
                <li><Link className="dropdown-item" href="#">Fotocards fanmade</Link></li>
                <li><Link className="dropdown-item">Poleras</Link>
              </li>
              </ul>
            </li>

          </ul>
          
        </div>
      </div>
    </nav>
  )
}
export default Navbar;