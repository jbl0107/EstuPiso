import api from './api';
import jwtDecode from 'jwt-decode';



  export const getUserInfo = async (userId, token) => {
    const response = await fetch(`/api/users/${userId}`, {
      headers: {
        'Authorization': 'Bearer ' + token
      }
    });
    const data = await response.json();
    return data;
  };

  
  export const isUserLoggedIn = async () => {
    const accessToken = localStorage.getItem('jwtToken');
    const refreshToken = localStorage.getItem('refreshToken');
  
    if (accessToken && refreshToken) {
      const decodedToken = jwtDecode(accessToken);
  
      const currentTime = Date.now() / 1000;
  
      if (decodedToken.exp < currentTime) {
        try {
          const response = await api.post('/api/token/refresh/', { 'refresh': refreshToken });
  
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