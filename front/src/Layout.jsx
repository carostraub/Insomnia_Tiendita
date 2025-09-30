
import React from 'react';
import { Routes, Route } from "react-router-dom"
import Navbar from './components/Navbar';
import Register from './views/Register';
import Login from './views/Login';
import Home from './views/Home';
import Products from './views/Products';
import CheckOut from './views/CheckOut';
import AboutUs from './views/AboutUs';


export const Layout = () => {


  return (
    <>
      <Navbar />
      <Routes>
        <Route path="/register" element={<Register />} />
        <Route path="/login" element={<Login />} />
        <Route path="/" element={<Home />} />
        <Route path="/products" element={<Products />} />
        <Route path="/checkout" element={<CheckOut />} />
        <Route path="/aboutUs" element={<AboutUs />} />
      </Routes>

    </>
  )



}


