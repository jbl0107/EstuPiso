import React, { createContext, useState, useEffect } from 'react';
import { isUserLoggedIn } from './auth';
import { useLocation } from 'react-router-dom';


export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {


  const [isLoggedIn, setIsLoggedIn] = useState(false);

  const location = useLocation();

  useEffect(() => {
    isUserLoggedIn().then(loggedIn => {
      setIsLoggedIn(loggedIn);
    });
  }, [location]);




  useEffect(() => {
    const handleTokenUpdated = () => {
      isUserLoggedIn().then(loggedIn => setIsLoggedIn(loggedIn));
    };

    window.addEventListener('tokenUpdated', handleTokenUpdated);

    return () => {
      window.removeEventListener('tokenUpdated', handleTokenUpdated);
    };
  }, []);




  useEffect(() => {
    const interval = setInterval(() => {
      isUserLoggedIn();
    }, 60000);

    return () => clearInterval(interval);
  }, []);





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




  return (
    <AuthContext.Provider value={{ isLoggedIn, handleLogout }}>
      {children}
    </AuthContext.Provider>
  );
};