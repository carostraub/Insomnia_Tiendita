import React from "react";
import { Link } from "react-router";
import AboutUs from "../views/AboutUs";

const Navbar = () => {
  return (
    <nav className="navbar navbar-expand-lg bg-body-tertiary">
      <div className="container-fluid">
        <Link className="navbar-brand" to="/">
        <img
        src="/logoBordeBlanco.png"
        alt="Logo"
        style={{ width: "auto", height: "55px" }}
        />
        </Link>
        {/* El boton de abajo es para que el menu se haga hamburguesa en pantallas chicas */}
        <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
          <span className="navbar-toggler-icon"></span>
        </button>
        <div className="collapse navbar-collapse" id="navbarSupportedContent">
          <ul className="navbar-nav ms-auto mb-2 mb-lg-0">
            <li className="nav-item"> 
              <a className="nav-link active" href="https://www.instagram.com/insomniatiendita/" target="_blank" rel="noopener noreferrer">
              <i className="fa-brands fa-lg fa-instagram"></i>
              </a>
            </li>
            <li className="nav-item">
              <Link className="nav-link active" aria-current="page" to="/aboutUs" >Sobre Nosotros</Link>
            </li>

            <li className="nav-item dropdown">
              <a className="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                Productos
              </a>
              <ul className="dropdown-menu dropdown-menu-start">
                <li><Link className="dropdown-item" href="#">Totebags</Link></li>
                <li><Link className="dropdown-item" href="#">Ilustraciones</Link></li>
                <li><Link className="dropdown-item" href="#">Fotocards fanmade</Link></li>
                <li><Link className="dropdown-item">Poleras</Link></li>
              </ul>
            </li>
            <li className="nav-item">
              <Link className="nav-link active" aria-current="page" to="/login" >
              <i className="fa-solid fa-lg fa-user"></i>
              </Link>
            </li>
            <li className="nav-item">
              <Link className="nav-link active" aria-current="page" to="/checkout" >
              <i className="fa-solid fa-lg fa-cart-shopping"></i>
              </Link>
            </li>

          </ul>
          
        </div>
      </div>
    </nav>
  )
}
export default Navbar;