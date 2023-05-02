import React from "react";
import { Link, useLocation } from "react-router-dom";
import jwtDecode from 'jwt-decode';
import { useState, useEffect } from 'react';
import api from '../api/api.js'



export function Navbar() {
  const location = useLocation();

  useEffect(() => {
    const interval = setInterval(() => {
      isUserLoggedIn();
    }, 60000); // Actualiza el token cada 50 segundos

    return () => clearInterval(interval);
  }, []);



  const isUserLoggedIn = async () => {
    const accessToken = localStorage.getItem('jwtToken');
    const refreshToken = localStorage.getItem('refreshToken');


    if (accessToken && refreshToken) {
      const decodedToken = jwtDecode(accessToken);
  
      const currentTime = Date.now() / 1000;
      
      if (decodedToken.exp < currentTime) {
        try {
          const response = await api.post('api/token/refresh/', { 'refresh': refreshToken });

          const newAccessToken = response.data.access;
          const newRefresh = response.data.refresh;

          localStorage.setItem('jwtToken', newAccessToken);
          localStorage.setItem('refreshToken',newRefresh);
  
          return true;

        } catch (error) {
          return false;
        }

      } else {
        return true;
      }
    } else {
      return false;
    }
  
  };


  async function handleLogout() {
    try {

      const token = localStorage.getItem('jwtToken');
      const refreshToken = localStorage.getItem('refreshToken');




      const response = await fetch('/api/logout/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          refresh: refreshToken
        })
      });

      if (response.ok) {
        localStorage.removeItem('jwtToken');
        localStorage.removeItem('refreshToken');
        setIsLoggedIn(false);

      } else {
        // Manejo del error del token expirado
        if (response.status === 401) {
          localStorage.removeItem('jwtToken');
          localStorage.removeItem('refreshToken');
          setIsLoggedIn(false);
        }
      }
    } catch (error) {
      
      alert('Ocurrió un error al intentar cerrar sesión. Por favor, inténtalo de nuevo.');
    }
  }





  const [isLoggedIn, setIsLoggedIn] = useState(false);

  useEffect(() => {
    isUserLoggedIn().then(loggedIn => setIsLoggedIn(loggedIn));
  }, []);

  useEffect(() => {
    const handleTokenUpdated = () => {
      setIsLoggedIn(isUserLoggedIn());
    };

    window.addEventListener('tokenUpdated', handleTokenUpdated);

    return () => {
      window.removeEventListener('tokenUpdated', handleTokenUpdated);
    };

  }, []);



  

  return (
    
      <nav className="flex items-center justify-between flex-wrap bg-gradient-to-r from-blue-900 to-blue-300 p-6 w-full fixed top-0 left-0">
        <div className="flex items-center flex-shrink-0 text-white mr-6">
          <Link to="/"><img className="md:h-full md:w-52" src="/Logo.png"/></Link>
      
        </div>
       
        <div className="w-full block flex-grow lg:flex lg:items-center lg:w-auto">
          <div className="text-sm lg:flex-grow flex space-x-8">
            <Link
              to="/"
              className={`text-gray-300 hover:bg-gray-700 hover:text-white rounded-md px-2 py-2 text-sm font-medium mr-4"
              ${
                location.pathname === '/' ? 'bg-gray-700' : ''
              }`}>
              Home
            </Link>


            <Link
              to="/announcements"
              className={`text-gray-300 hover:bg-gray-700 hover:text-white rounded-md px-2 py-2 text-sm font-medium mr-4"
              ${
                location.pathname === '/announcements' ? 'bg-gray-700' : ''
              }`}>
              Anuncios
            </Link>

          </div>
          
            {isLoggedIn ? (
              <Link
                to="/"
                onClick={handleLogout}
                className={`inline-block text-sm font-medium px-4 py-2 leading-none border rounded text-black
                border-black hover:border-transparent hover:text-teal-700 hover:bg-white mt-4 lg:mt-0 border-width: 5px"
                ${
                  location.pathname === '/' ? '' : ''
                }`}>
                  Cerrar sesión
              </Link>



            ):(

              <Link
                to="/loginForm"
                className={`inline-block text-sm font-medium px-4 py-2 leading-none border rounded text-black
                border-black hover:border-transparent hover:text-teal-700 hover:bg-white mt-4 lg:mt-0 border-width: 5px"
                ${
                  location.pathname === '/loginForm' ? 'bg-black text-teal-700' : ''
                }`}>
              Iniciar sesión
            </Link>

            )}
            
        </div>
      </nav>

  );
}