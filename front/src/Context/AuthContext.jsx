import React, { createContext, useContext, useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { baseURL } from "../config/index"; // Asegúrate de tener este archivo

//Falta hacer el logout y  actualizar el perfil

// Crear el contexto de autenticación
const AuthContext = createContext();

// Hook personalizado para acceder al contexto fácilmente
export const useAuth = () => {
    return useContext(AuthContext);
};

// Proveedor de autenticación que manejará el estado del usuario
export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);
    const navigate = useNavigate();

    //  Comprobar si el usuario está autenticado al cargar la app
    useEffect(() => {
        const checkAuth = async () => {
            try {
                const token = localStorage.getItem("access_token");

                // Si no hay token, usuario no está autenticado
                if (!token) {
                    setUser(null);
                    setLoading(false);
                    return;
                }

                // Verificar token con el endpoint correcto
                const response = await fetch(`${baseURL}/api/profile`, {
                    method: "GET",
                    headers: {
                        "Authorization": `Bearer ${token}`
                    },
                    credentials: "include" // credentials es para enviar cookies si las hay, se necesita CORS en el backend
                });

                if (response.ok) {
                    const data = await response.json();
                    setUser(data.user || data); // Flexible con la estructura de respuesta
                } else {
                    // Token inválido o expirado - limpiar localStorage
                    console.log("Token inválido, limpiando...");
                    localStorage.removeItem("access_token");
                    setUser(null);
                }
            } catch (error) {
                console.error("Error verificando autenticación:", error);
                setUser(null);
            } finally {
                setLoading(false);
            }
        };

        checkAuth();
    }, []); // Solo se ejecuta una vez al montar el componente

    // Función para manejar el login
    const login = async (email, password) => {
        try {
            const response = await fetch(`${baseURL}/api/login`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ email, password }),
                credentials: "include"
            });
            const data = await response.json();

            if (response.ok) {
                localStorage.setItem("access_token", data.access_token);
                setUser(data.user || data); // Flexible con la estructura de respuesta
                navigate("/"); // Redirigir a la página principal u otra ruta
            } else {
                alert("Error al iniciar sesión: " + (data.message || "Credenciales inválidas"));
            }
        } catch (error) {
            console.error("Error en login:", error);
            alert("Error al iniciar sesión. Inténtalo de nuevo.");
        } finally {
            setLoading(false);
        }
    };
    // Función para manejar el registro
    const register = async (name, email, password) => {
        try {
            const response = await fetch(`{baseURL}/api/register`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ name, email, password }),
                credentials: "include"
            });
            const data = await response.json();

            if (response.ok) {
                localStorage.setItem("access_token", data.access_token);
                setUser(data.user || data); // Flexible con la estructura de respuesta
                navigate("/login"); // Redirigir a la página de login
            } else {
                alert("Error al registrarse: " + (data.message || "No se pudo registrar"));
            }
        } catch (error) {
            console.error("Error en registro:", error);
            alert("Error al registrarse. Inténtalo de nuevo.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <AuthContext.Provider
            value={{ user, loading, login, register }}
        >
            {children}
        </AuthContext.Provider>
    );


};
export default AuthProvider;