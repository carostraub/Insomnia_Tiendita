import React, {useState} from 'react'
import { useAuth } from '../Context/AuthContext'

const Login = () => {
  const { login } = useAuth();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    await login(email, password);
  };






  return (
    <form className="container w-50 mt-4" onSubmit={handleSubmit}>
      <h2>Iniciar Sesión</h2>
      <div className="mb-3 pt-5">
        <label htmlFor="exampleInputEmail1" className="form-label">
          Dirección de email
        </label>
        <input
          type="email"
          className="form-control"
          id="exampleInputEmail1"
          value={email}
          aria-describedby="emailHelp"
          onChange={(e) => setEmail(e.target.value)}
          required
        />
        
      </div>
      <div className="mb-3">
        <label htmlFor="exampleInputPassword1" className="form-label">
          Contraseña
        </label>
        <input
          type="password"
          className="form-control"
          id="exampleInputPassword1"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
      </div>
      <button type="submit" className="btn btn-light">
        Iniciar sesión
      </button>
    </form>
  );
};


export default Login