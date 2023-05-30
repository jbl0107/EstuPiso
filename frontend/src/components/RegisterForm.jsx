import React, { useRef, useState } from 'react'
import axios from 'axios'
import {Link} from 'react-router-dom'
import { UserCircleIcon } from '@heroicons/react/24/solid'
import { PhoneInput } from './PhoneInput'
import { useNavigate } from 'react-router-dom';
import api from '../api/api.js';


export const RegisterForm = () => {
    const navigate = useNavigate();

    const fileInputRef = useRef();
    const [fileName, setFileName] = useState('');
    const [imageSrc, setImageSrc] = useState(null);


    const handleFileChange = (event) => {
        if (event.target.files.length > 0) {
            const file = event.target.files[0];
            const imageUrl = URL.createObjectURL(file);
            setImageSrc(imageUrl);
            setFileName(file.name);
        }
    };

    const handleButtonClick = () => {
        fileInputRef.current.click();
    };

    const handleRemoveImage = () => {
        fileInputRef.current.value = null;
        setImageSrc(null);
        setFileName(null);
    }


    const [prefix, setPrefix] = useState('+34');

    const handlePrefixChange = (newPrefix) => {
        setPrefix(newPrefix);
    }




    const[errorMessageRegister, setErrorMessageRegister] = useState(null)

    const [dniError, setDniError] = useState(null);
    const [usernameError, setUsernameError] = useState(null);
    const [emailError, setEmailError] = useState(null);
    const [nameError, setNameError] = useState(null);
    const [surnameError, setSurnameError] = useState(null);
    const [telephoneError, setTelephoneError] = useState(null);
    const [passwordError, setPasswordError] = useState(null);
    const [password2Error, setPassword2Error] = useState(null);
    const [typeError, setTypeError] = useState(null);


    const handleSubmit = async (event) => {
        event.preventDefault();

        
        const formData = new FormData();
        if (event.target.photo.files[0]) {
            formData.append('photo', event.target.photo.files[0]);
        }
        formData.append('name', event.target.name.value);
        formData.append('surname', event.target.surname.value);
        formData.append('telephone', prefix + event.target.telephone.value);
        formData.append('dni', event.target.dni.value);
        formData.append('username', event.target.username.value);
        formData.append('email', event.target.email.value);
        formData.append('password', event.target.password.value);


        setDniError(null);
        setUsernameError(null);
        setEmailError(null);
        setNameError(null);
        setSurnameError(null);
        setTelephoneError(null);
        setPasswordError(null);
        setPassword2Error(null);
        setTypeError(null);
        setErrorMessageRegister(null);
        
        try {

            let response;

            if (event.target.type.value == "Estudiante"){
                response = await axios.post('/api/students/', formData);

            }
            else if(event.target.type.value == "Propietario"){
                response = await axios.post('/api/owners/', formData);
            }

            else{
                setTypeError('Eliga un tipo de usuario')
            }

            const loginResponse = await api.post('/api/login/', {
                username: event.target.username.value,
                password: event.target.password.value,
              });
              
              localStorage.setItem('jwtToken', loginResponse.data.access);
              localStorage.setItem('refreshToken', loginResponse.data.refresh);
              navigate('/');

            

        } catch (error) {


           
            if (error.response && error.response.data) {

                if (error.response.data.dni) {
                    setDniError(error.response.data.dni[0]);
                }
                if (error.response.data.username) {
                    setUsernameError(error.response.data.username[0]);
                }
                if (error.response.data.email) {
                    setEmailError(error.response.data.email[0]);
                }
                if (error.response.data.name) {
                    setNameError(error.response.data.name[0]);
                }
                if (error.response.data.surname) {
                    setSurnameError(error.response.data.surname[0]);
                }
                if (error.response.data.telephone) {
                    setTelephoneError(error.response.data.telephone[0]);
                }
                if (error.response.data.password) {
                    setPasswordError(error.response.data.password[0]);
                }
                if (error.response.data.telephone) {
                    setTelephoneError(error.response.data.telephone[0]);
                }

                if (event.target.password.value != event.target.password2.value){
                    setPassword2Error('Las contraseñas no coinciden')
                }


            } else {
                setErrorMessageRegister('Ocurrió un error al intentar crear un usuario.');
            }
        }
      };




  return (

    <div className='flex items-center justify-center bg-img bg-cover bg-no-repeat bg-center h-full'>
        <div className="w-full max-w-2xl border-4 border-solid border-white-50 rounded-20 backdrop-blur-lg">

            <div className='mt-5'>
                
            
        
            <form className="bg-transparent border-solid border-white rounded px-8 py-30 pt-6 pb-8 mb-4" onSubmit={handleSubmit}>
                
                <img className="relative left-9" src="/Logo.png"/>
                <h1 className="flex justify-center text-3xl font-bold mb-4 text-white">Registro</h1>

                <div className="col-span-full">
                    <label htmlFor="photo" className="block text-sm font-medium leading-6 text-white">
                        Photo
                    </label>
                    <div className="mt-2 flex items-center gap-x-3">
                        {imageSrc ? (
                            <>
                                <img src={imageSrc} alt="Avatar" className="h-12 w-12 rounded-full text-white" />
                                
                                {fileName && <p className='text-black'>{fileName}</p>}

                                <button type="button" className="rounded-full bg-white px-2.5 py-1.5 text-sm font-semibold
                                 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50"
                                    onClick={handleRemoveImage}>
                                    x
                                </button>
                            </>

                        ) : (
                            <UserCircleIcon className="h-12 w-12 text-gray-300" aria-hidden="true" />
                        )}

                        <button type="button" className="rounded-md bg-white px-2.5 py-1.5 text-sm font-semibold
                                text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50"
                            onClick={handleButtonClick}>
                                Subir
                        </button>
                        
                        <input type="file" id="photo" name="photo" accept="image/*" className="hidden" ref={fileInputRef} 
                        onChange={handleFileChange}/>

                        
                    </div>
                    
                </div>
 

                <div className="mt-10 grid grid-cols-1 gap-x-6 gap-y-8 sm:grid-cols-6">

                    <div className="sm:col-span-3">
                        <label className="block text-white text-sm font-bold mb-2" htmlFor="name">
                            Nombre
                        </label>

                        <input className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight 
                        focus:outline-none focus:shadow-outline" id="name" type="text" placeholder="Luis" name="name"
                        required={true}/>
                        {nameError && <p className="text-red-700 font-bold">{nameError}</p>}
                    </div>

                    <div className="sm:col-span-3">
                        <label className="block text-white text-sm font-bold mb-2" htmlFor="surname">
                            Apellidos
                        </label>

                        <input className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight 
                        focus:outline-none focus:shadow-outline" id="surname" type="text" placeholder="Perez Romero" name="surname"
                        required={true}/>
                        {surnameError && <p className="text-red-700 font-bold">{surnameError}</p>}
                    </div>


   
                    
                    <div className='sm:col-span-3'>
                        <label className="block text-white text-sm font-bold mb-2" htmlFor="telephone">
                            Telefono
                        </label>
                        <PhoneInput onPrefixChange={handlePrefixChange} error = {telephoneError} isUpdate={false}/>
                        
                    </div>

                    



                    <div className="sm:col-span-3">
                        <label className="block text-white text-sm font-bold mb-2" htmlFor="dni">
                            DNI
                        </label>

                        <input className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight 
                        focus:outline-none focus:shadow-outline" id="dni" type="text" placeholder="11223344A" name="dni"
                        required={true}/>
                        {dniError && <p className="text-red-700 font-bold">{dniError}</p>}
                    </div>


                    <div className="sm:col-span-3">
                        <label className="block text-white text-sm font-bold mb-2" htmlFor="username">
                            Nombre de usuario
                        </label>
                        
                        <div className='relative'>
                            <span className="absolute inset-y-0 left-0 flex items-center pl-2 mt-2">
                                <img src="/src/assets/user.svg" alt="Lock icon" className="w-6 h-5"/>
                            </span>

                            <input className="shadow appearance-none border rounded w-full py-2 px-3 pl-10
                            text-black leading-tight focus:outline-none focus:shadow-outline" id="username" type="text" 
                            placeholder="username" name="username" required={true}/>

                            {usernameError && <p className="text-red-700 font-bold">{usernameError}</p>}

                        </div>
                    </div>

                    <div className="sm:col-span-3">
                        <label className="block text-white text-sm font-bold mb-2" htmlFor="email">
                            Correo electrónico
                        </label>
                        
                        
                        <div className='relative'>
                            <span className="absolute inset-y-0 left-0 flex items-center pl-2 mt-2">
                                <img src="/src/assets/mail.svg" alt="Mail icon" className="w-6 h-6"/>
                            </span>
                            
                            <input className="shadow appearance-none border rounded w-full py-2 px-3 pl-10 text-gray-700 leading-tight 
                            focus:outline-none focus:shadow-outline" id="email" type="email" placeholder="example@gmail.com" name="email"
                            required={true}/>
                        </div>

                        {emailError && <p className="text-red-700 font-bold">{emailError}</p>}
                    </div>


                    <div className="sm:col-span-4">

                        <label htmlFor="type" className="block text-white text-sm font-bold mb-2">
                            Seleccione el tipo de usuario
                        </label>

                        <div className="mt-2">
                            <select id="type" name="type" defaultValue="valorPorDefecto" autoComplete="type-name"
                                className="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset
                                ring-gray-300 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:max-w-xs sm:text-sm 
                                sm:leading-6" required={true}>
                                <option value="valorPorDefecto">------</option>
                                <option value="Estudiante">Estudiante</option>
                                <option value="Propietario">Propietario</option>
                            
                            </select>
                            {typeError && <p className="text-red-700 font-bold">{typeError}</p>}
                        </div>
                    </div>

                    <div className="sm:col-span-3">

                        
                        <label className="block text-white text-sm font-bold mb-2" htmlFor="password">
                            Contraseña
                        </label>

                        <div className='relative'>
                            <span className="absolute inset-y-0 left-0 flex items-center pl-2 mt-2">
                                <img src="/src/assets/lock.svg" alt="Lock icon" className="w-6 h-5"/>
                            </span>

                            <input className="shadow appearance-none border rounded w-full py-2 px-3 pl-10 text-gray-700 mb-3 leading-tight 
                            focus:outline-none focus:shadow-outline" id="password" type="password" placeholder="***********" 
                            name="password" required={true}/>
                            {passwordError && <p className="text-red-600 font-bold">{passwordError}</p>}

                        </div>

                    </div>

                    <div className="sm:col-span-3">
                        <label className="block text-white text-sm font-bold mb-2" htmlFor="password2">
                            Repita la contraseña
                        </label>

                        <input className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 mb-3 leading-tight 
                        focus:outline-none focus:shadow-outline" id="password2" type="password" placeholder="***********" 
                        name="password2" required={true}/>
                        {password2Error && <p className="text-red-600 font-bold">{password2Error}</p>}

                    </div>
                    
                </div>

                

                <br/>

                    <div className="flex flex-col items-center">
                        {errorMessageRegister && <p className="text-red-700 font-bold">{errorMessageRegister}</p>}
                        <br></br>
                        <div className="mb-4">
                            <button className="bg-white hover:bg-sky-500 text-black font-bold py-2 px-4 rounded-lg
                             focus:outline-none focus:shadow-outline hover:text-white" type="submit">
                            Registrarse
                            </button>
                    </div>
            
                    
                

                    <div>
                        <span className="inline-block align-baseline font-bold text-sm text-white" to="#">
                        ¿Ya está registrado? <Link className="hover:text-white hover:underline" to="/loginForm">Inicie sesión aquí</Link>
                        </span>
                    </div>
                    
                </div>

            </form>
            
            </div>

        </div>
    </div>

    
  );
}


