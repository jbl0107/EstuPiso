import React, { useState } from 'react'
import {Link, useNavigate } from 'react-router-dom'
import api from '../api/api.js'


export const LoginForm = () => {

    //para redirigir al usuario a la pagina principal
    const navigate = useNavigate();


    const[errorMessage, setErrorMessage] = useState(null);

    const handleSubmit = async (event) => {
        event.preventDefault();

        const data = {
            username: event.target.username.value,
            password: event.target.password.value
        };
        try {
            const response = await api.post('/api/login/', data);
            const token = response.data.access;
            const refreshToken = response.data.refresh;
            
            localStorage.setItem('jwtToken', token);
            localStorage.setItem('refreshToken', refreshToken);
            navigate('/');
          // guardar el token y usarlo para hacer solicitudes autenticadas a otros puntos finales en tu API
        
        } catch (error) {
            
            if (error.response && error.response.status === 401) {
                setErrorMessage('Credenciales incorrectas. Inténtalo de nuevo.');

            } else if (error.response && error.response.data) {
                setErrorMessage(error.response.data.message);

            } else {
                setErrorMessage('Ocurrió un error al intentar iniciar sesión.');
            }
        }
      };

  return (

    <div className='flex items-center justify-center h-screen w-screen bg-img bg-cover bg-no-repeat bg-center'>
        <div className="w-full max-w-lg border-4 border-solid border-white-50 rounded-20">

            <form className="bg-transparent border-solid border-white rounded px-8 py-30 pt-6 pb-8 mb-4" onSubmit={handleSubmit}>
                <img className="relative left-9" src="/Logo.png"/>
                <h1 className="flex justify-center text-2xl font-bold mb-4 text-white">Inicio de sesión</h1>

                <div className="mb-4">
                    <label className="block text-white text-sm font-bold mb-2" htmlFor="username">
                        Username
                    </label>

                    <div className='relative'>

                        <span className="absolute inset-y-0 left-0 flex items-center pl-2 mt-2">
                            <img src="/src/assets/user.svg" alt="Lock icon" className="w-6 h-5"/>
                        </span>

                        <input className="shadow appearance-none border rounded w-full py-2 px-3 pl-10 text-gray-700 leading-tight 
                            focus:outline-none focus:shadow-outline" id="username" type="text" placeholder="Username" 
                            name="username" required={true}/>
                    </div>
                    
                </div>

                <div className="mb-6">
                    <div className="flex justify-between items-center">

                        <label className="block text-white text-sm font-bold mb-2" htmlFor="password">
                            Password
                        </label>

                        <Link className="text-sm font-bold text-white hover:text-cyan-300
                            hover:underline" to="#">
                        Olvidaste tu contraseña?
                        </Link>
                        
                    </div>

                    <div className='relative'>
                        <span className="absolute inset-y-0 left-0 flex items-center pl-2 mt-2">
                            <img src="/src/assets/lock.svg" alt="Lock icon" className="w-6 h-5"/>
                        </span>

                        <input className="shadow appearance-none border rounded w-full py-2 px-3 pl-10 text-gray-700 mb-3 leading-tight 
                        focus:outline-none focus:shadow-outline" id="password" type="password" placeholder="***********" 
                        name="password" required={true}/>

                        {errorMessage && <p className="text-red-600 font-bold">{errorMessage}</p>}
                    </div>

                </div>

                <br/>

                <div className="flex flex-col items-center">
                    <div className="mb-4">
                        <button className="bg-white hover:bg-blue-700 text-black font-bold py-2 px-4 rounded hover:text-white
                        focus:outline-none focus:shadow-outline" type="submit">
                        Iniciar sesión
                        </button>
                    </div>
                    
                    


                    <div>
                        <span className="inline-block align-baseline font-bold text-sm text-white" to="#">
                         <Link className="hover:text-blue-300 hover:underline" to="/registerForm">¿Aún no estas registrado?</Link>
                        </span>
                    </div>
                    
                </div>

            </form>

        </div>
    </div>

    
  );
}
