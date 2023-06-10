import axios from 'axios';


// crea una instancia de axios con la URL base de tu API
const api = axios.create({
  baseURL: ''
});


api.interceptors.response.use(
  response => response,
  async error => {
    const { config, response: { status } } = error;
    const originalRequest = config;

    if (status === 401) {
      const refreshToken = localStorage.getItem('refreshToken');


      if (refreshToken) {
        try {
          const response = await api.post('/token/refresh/', { refreshToken });
          const token = response.data.access;
          const refreshToken = response.data.refresh;

          localStorage.setItem('jwtToken', token);
          localStorage.setItem('refreshToken', refreshToken)

          // dispara un evento personalizado para notificar que el token ha sido actualizado
          const event = new CustomEvent('tokenUpdated');
          window.dispatchEvent(event);

          originalRequest.headers['Authorization'] = `Bearer ${token}`;

          return api(originalRequest);
        } catch (error) {
          //history.push('/login');
          
        }
      } else {
        //history.push('/login');
      }
    }

    return Promise.reject(error);
  }
);

export default api;