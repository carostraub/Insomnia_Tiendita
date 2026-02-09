import React, { useState } from 'react'
import { baseURL } from '../config'
import { useNavigate } from 'react-router-dom'

const Register = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    password: "",
    subscribe: false
  });
  const handleChange = (e) => {
    const { name, type, checked, value } = e.target;
    setFormData({
      ...formData,
      [name]: type == "checkbox" ? checked: value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    const dataToSend = new FormData();
    for (const key in formData) {
      dataToSend.append(key, formData[key]);
    }

    try {
      const response = await fetch(`${baseURL}/api/register`, {
        method: "POST",
        body: dataToSend
      });

      const result = await response.json();

      if (response.ok) {
        alert("Registro exitoso");
        console.log("Usuario registrado", result);
        navigate("/login");
      } else {
        alert("Error en el registro: " + result.error);
      }
    } catch (error) {
      console.error("Error en la petición", error);
      alert("Hubo un problema con el registro.");
    }
  };







  return (
    <div className="container w-50 mt-4">
      <h2>Registro</h2>
      <form onSubmit={handleSubmit}>
        <div className="row">
          <div className="col-md-12">

            <h6>Nombre completo</h6>
            <input 
            className="mb-3" 
            type="text" 
            name="name" 
            placeholder="Nombre" 
            value={formData.name} 
            onChange={handleChange} 
            required />

            <h6>Email</h6>
            <input 
            className='mb-3' 
            type="email" 
            name="email" 
            placeholder='email' 
            value={formData.email} 
            onChange={handleChange} 
            required />

            <h6>Contraseña</h6>
            <input 
            className="mb-3" 
            type="password" 
            name="password" 
            placeholder="Contraseña" 
            value={formData.password} 
            onChange={handleChange} 
            required />
            
            <div className="form-check">
              <input 
              className="form-check-input" 
              type="checkbox" 
              name='subscribe'
              checked={formData.subscribe} 
              id="checkDefault" 
              onChange={handleChange} />
                <label className="form-check-label" for="checkDefault">
                  Subscribirse para recibir promociones y notificaciones de eventos realizados por Insomnia
                </label>
            </div>
            <button type='submit' className='btn btn-light'>
              Registrarse
            </button>

          </div>
        </div>
      </form>

    </div>
  )
}

export default Register