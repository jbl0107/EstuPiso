import React, { useRef, useState, useEffect } from 'react'
import { UserCircleIcon } from '@heroicons/react/24/solid'
import { AuthContext } from '../api/AuthContext';
import { useContext } from 'react';
import { PhoneInput } from './PhoneInput'
import api from '../api/api.js';
import jwtDecode from 'jwt-decode';



export const UserProfile = () => {


  const storedUserInfo = localStorage.getItem('userInfo');
  const userInfo = storedUserInfo ? JSON.parse(storedUserInfo) : null;

  const { isLoggedIn, handleLogout, isOwner, isStudent } = useContext(AuthContext);


  const fileInputRef = useRef();
  const [fileName, setFileName] = useState("");
  const [imageSrc, setImageSrc] = useState(null);
  const [removePhoto, setRemovePhoto] = useState(false);


  const handleFileChange = (event) => {
    if (event.target.files.length > 0) {
      const file = event.target.files[0];
      const imageUrl = URL.createObjectURL(file);
      setImageSrc(imageUrl);
      setFileName(file.name);
      setRemovePhoto(false);
    }
  };

    const handleButtonClick = () => {
        fileInputRef.current.click();
    };




    const handleRemoveImage = () => {
      fileInputRef.current.value = null;
      setImageSrc(null);
      setFileName(null);
      setRemovePhoto(true);
    };

    
    


    const [prefix, setPrefix] = useState('+34');

    const handlePrefixChange = (newPrefix) => {
        setPrefix(newPrefix);
    }




    const[errorMessageRegister, setErrorMessageProfile] = useState(null)

    const [dniError, setDniError] = useState(null);
    const [usernameError, setUsernameError] = useState(null);
    const [emailError, setEmailError] = useState(null);
    const [nameError, setNameError] = useState(null);
    const [surnameError, setSurnameError] = useState(null);
    const [telephoneError, setTelephoneError] = useState(null);
    const [passwordError, setPasswordError] = useState(null);
    const [password2Error, setPassword2Error] = useState(null);


    const [showUpdateMessage, setShowUpdateMessage] = useState(false);
    const handleSubmit = async (event) => {
        event.preventDefault();

        
        const formData = new FormData();
       
        
        formData.append('name', event.target.name.value);
        formData.append('surname', event.target.surname.value);
        formData.append('telephone', prefix + event.target.telephone.value);
        formData.append('dni', event.target.dni.value);
        formData.append('username', event.target.username.value);
        formData.append('email', event.target.email.value);

    
       

        setDniError(null);
        setUsernameError(null);
        setEmailError(null);
        setNameError(null);
        setSurnameError(null);
        setTelephoneError(null);
        setErrorMessageProfile(null);
        
        
        try {

          let response;
        

          if (isStudent){
            const token = localStorage.getItem('jwtToken'); 
            response = await api.put(`/api/students/${jwtDecode(token).user_id}`, formData, {
            headers: {
              'Authorization': 'Bearer ' + token
            }
            
            }); 
            setShowUpdateMessage(true);
            setSuccessMessageAnimation('slide-in-from-left');
            setTimeout(() => {
              setSuccessMessageAnimation('slide-out-to-left');
              setTimeout(() => setShowUpdateMessage(false), 500);
            }, 3000);
            const newUserInfo = {
              ...response.data,
              id: jwtDecode(token).user_id
            };
            localStorage.setItem('userInfo', JSON.stringify(newUserInfo));
          }
          else if(isOwner){
            const token = localStorage.getItem('jwtToken');
            response = await api.put(`/api/owners/${jwtDecode(token).user_id}`, formData, {
              headers: {
                'Authorization': 'Bearer ' + token
              }
            }); 
            setShowUpdateMessage(true);
            setSuccessMessageAnimation('slide-in-from-left');
            setTimeout(() => {
              setSuccessMessageAnimation('slide-out-to-left');
              setTimeout(() => setShowUpdateMessage(false), 500);
            }, 3000);
            const newUserInfo = {
              ...response.data,
              id: jwtDecode(token).user_id
            };
            localStorage.setItem('userInfo', JSON.stringify(newUserInfo));

          }

          


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

            } else {
                setErrorMessageProfile('Ocurrió un error al intentar actualizar un usuario.');
            }
        }
      };


  const [showModal, setShowModal] = useState(false);

  const handleOpenModal = () => {
      setShowModal(true);

  }

  const handleCloseModal = () => {
    setShowModal(false);
    setCurrentPassword("");
    setShowChangePasswordForm(false);
    setErrorCurrentPassword(null);

  };


  const [currentPassword, setCurrentPassword] = useState("");
  const [showChangePasswordForm, setShowChangePasswordForm] = useState(false);
  const [errorCurrentPassword, setErrorCurrentPassword] = useState(false);


  const handleVerifyCurrentPassword = async(event) => {

    event.preventDefault();
    const password = event.target.current_password.value;
    const current_password = { password: password };

    let response;

    if (isStudent){
      const token = localStorage.getItem('jwtToken')
      response = await api.post('/api/students/verify-pass', JSON.stringify(current_password), {
      headers: {
        'Authorization': 'Bearer ' + token,
        'Content-Type': 'application/json'
      }
    }); 

    }
    else if(isOwner){
      const token = localStorage.getItem('jwtToken')
      response = await api.post('/api/owners/verify-pass', JSON.stringify(current_password), {
        headers: {
          'Authorization': 'Bearer ' + token,
          'Content-Type': 'application/json'
        }
      }); 
    }



    if (response.data.password_correct) {
      setShowChangePasswordForm(true);
      setErrorCurrentPassword(null);
    } else {
      setErrorCurrentPassword('Contraseña incorrecta');
    }


  };



  const [showSuccessMessage, setShowSuccessMessage] = useState(false);
  const [successMessageAnimation, setSuccessMessageAnimation] = useState('');


  
  const handleChangePassword = async(event) => {

    event.preventDefault();
    setPasswordError(null);
    setPassword2Error(null);
    const new_password = event.target.password.value;
    const password = { new_password: new_password };
    const password2 = event.target.password2.value;

    if (new_password !== password2) {
      setPasswordError('Las contraseñas no coinciden');
      return;
    }
    setPasswordError(null);
  
    if (new_password.length < 8) {
      setPassword2Error('La contraseña debe tener al menos 8 caracteres');
      return;
    }
    setPassword2Error(null);

    let response;

    if (isStudent){
      const token = localStorage.getItem('jwtToken')
      response = await api.put('/api/students/profile-pass-change', JSON.stringify(password), {
      headers: {
        'Authorization': 'Bearer ' + token,
        'Content-Type': 'application/json'
      }
    }); 
    setShowModal(false);
    setShowChangePasswordForm(false);
    setCurrentPassword("");
    setShowSuccessMessage(true);
    setSuccessMessageAnimation('slide-in-from-left');
    setTimeout(() => {
      setSuccessMessageAnimation('slide-out-to-left');
      setTimeout(() => setShowSuccessMessage(false), 500);
    }, 3000);
    
    }

    else if(isOwner){
      const token = localStorage.getItem('jwtToken')
      response = await api.put('/api/owners/profile-pass-change', JSON.stringify(password), {
        headers: {
          'Authorization': 'Bearer ' + token,
          'Content-Type': 'application/json'
        }
      }); 

      setShowModal(false);
      setShowChangePasswordForm(false);
      setCurrentPassword("");
      setShowSuccessMessage(true);
      setSuccessMessageAnimation('slide-in-from-left');
      setTimeout(() => {
        setSuccessMessageAnimation('slide-out-to-left');
        setTimeout(() => setShowSuccessMessage(false), 500);
      }, 3000);
    }

  };





  const [showPhotoMessage, setShowPhotoMessage] = useState(false);
  const handleChangePhoto = async (event) => {
    event.preventDefault();

    const formData = new FormData();

    if (removePhoto) {
      formData.append("photo", '');
    } else if (fileInputRef.current.files.length > 0) {
      formData.append("photo", fileInputRef.current.files[0]);
    }

    let response;

    if (isStudent) {
      const token = localStorage.getItem("jwtToken");
      response = await api.put(`/api/students/photo-update/${jwtDecode(token).user_id}`, formData, {
        headers: {
          'Authorization': 'Bearer ' + token
        }
      });
      setShowPhotoMessage(true);
      setSuccessMessageAnimation('slide-in-from-left');
      setTimeout(() => {
          setSuccessMessageAnimation('slide-out-to-left');
          setTimeout(() => setShowPhotoMessage(false), 500);
        }, 3000);

        const newUserInfo = {
          ...userInfo,
          photo: response.data.photo
        };
        localStorage.setItem('userInfo', JSON.stringify(newUserInfo));
        
        const event = new CustomEvent('photoUpdate', {
          detail: {
            photoUpdate: response.data.photo
          }
        });
        window.dispatchEvent(event);
    }

    else if (isOwner) {
      const token = localStorage.getItem("jwtToken");
      response = await api.put(`/api/owners/photo-update/${jwtDecode(token).user_id}`, formData, {
        headers: {
          'Authorization': 'Bearer ' + token
        }
      });
      setShowPhotoMessage(true);
      setSuccessMessageAnimation('slide-in-from-left');
      setTimeout(() => {
        setSuccessMessageAnimation('slide-out-to-left');
        setTimeout(() => setShowPhotoMessage(false), 500);
      }, 3000);


      const newUserInfo = {
        ...userInfo,
        photo: response.data.photo
      };
      localStorage.setItem('userInfo', JSON.stringify(newUserInfo));

      const event = new CustomEvent('photoUpdate', {
        detail: {
          photoUpdate: response.data.photo
        }
      });
      window.dispatchEvent(event);
    }
         
      
  
  };

  

  useEffect(() => {
    const fetchUserProfile = async () => {
      
      if (userInfo.photo) {
        const photoUrl = "api/" + userInfo.photo;
        setImageSrc(photoUrl);
      } else {
        setImageSrc(null);
      }
    };
    fetchUserProfile();
  }, []);


  
  if (!userInfo) {
    return <></>;
  }
  

  return (
    <>
    <br></br>
    <br></br>
    <br></br>
    <br></br>


    {showSuccessMessage && (
        <div
          className={`fixed bottom-4 left-4 bg-green-600 text-white p-4 rounded-md shadow-md ${successMessageAnimation}`}>
          La contraseña se ha actualizado correctamente
        </div>
    )}

    {showUpdateMessage && (
        <div
          className={`fixed bottom-4 left-4 bg-green-600 text-white p-4 rounded-md shadow-md ${successMessageAnimation}`}>
          Usuario actualizado correctamente
        </div>
    )}

    {showPhotoMessage && (
        <div
          className={`fixed bottom-4 left-4 bg-green-600 text-white p-4 rounded-md shadow-md ${successMessageAnimation}`}>
          Foto actualizada correctamente
        </div>
    )}
    

    <div className="flex flex-col items-center p-4">
    
      <h1 className="text-2xl font-bold mt-4">Bienvenido a tu perfil, {userInfo.username}</h1>
      <div className="my-hr"></div>
      <div className="col-span-full">

      
        <form onSubmit={handleChangePhoto}>
          <div className="mt-2 flex items-center gap-x-3">
            {imageSrc ? (
              <>
                <img src={imageSrc} alt="Avatar" className="h-32 w-32 rounded-full text-white" />

                {fileName && <p className="text-black">{fileName}</p>}

                <button type="button" className="rounded-full bg-white px-2.5 py-1.5 text-sm font-semibold text-gray-900 
                  shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50" onClick={handleRemoveImage}>
                  x
                </button>
              </>
            ) : (
              <UserCircleIcon
                className="h-32 w-32 text-gray-700"
                aria-hidden="true"
              />
            )}

            <button type="button" className="rounded-md bg-white px-2.5 py-1.5 text-sm font-semibold text-gray-900 
            shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50" onClick={handleButtonClick}>
              Cambiar foto de perfil
            </button>

            <input type="file" id="photo" name="photo" accept="image/*" className="hidden" ref={fileInputRef} 
              onChange={handleFileChange}/>

            <button className="bg-yellow-300 hover:bg-yellow-400 text-black font-bold py-2 px-4 rounded-lg  
              focus:outline-none focus:shadow-outline" type="submit">
              Actualizar
            </button>
          </div>
        </form>
      
      </div>
      <div className="my-hr"></div>
    </div>
      
      
    <div className="flex flex-col items-center p-4">
      <form onSubmit={handleSubmit}>
      <div className="mt-5 grid grid-cols-1 gap-x-6 gap-y-8 sm:grid-cols-6">

        <div className="sm:col-span-3">
          <label className="block text-black text-sm font-bold mb-2" htmlFor="name">
              Nombre
          </label>

          <input className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight 
          focus:outline-none focus:shadow-outline" id="name" type="text" placeholder="Luis" name="name"
          required={true} defaultValue={userInfo.name}/>
          {nameError && <p className="text-red-600 text-sm">{nameError}</p>}
        </div>

        <div className="sm:col-span-3">
          <label className="block text-black text-sm font-bold mb-2" htmlFor="surname">
              Apellidos
          </label>

          <input className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight 
          focus:outline-none focus:shadow-outline" id="surname" type="text" placeholder="Perez Romero" name="surname"
          required={true} defaultValue={userInfo.surname}/>
          {surnameError && <p className="text-red-600 text-sm">{surnameError}</p>}
        </div>


   
                    
        <div className='sm:col-span-3'>
          <label className="block text-black text-sm font-bold mb-2" htmlFor="telephone">
              Telefono
          </label>
          <PhoneInput onPrefixChange={handlePrefixChange} error = {telephoneError} isUpdate={true} 
          currentUserNumber={userInfo.telephone.slice(3)}/>
            
        </div>

                    



        <div className="sm:col-span-3">
          <label className="block text-black text-sm font-bold mb-2" htmlFor="dni">
              DNI
          </label>

          <input className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight 
          focus:outline-none focus:shadow-outline" id="dni" type="text" placeholder="11223344A" name="dni"
          required={true} defaultValue={userInfo.dni}/>
          {dniError && <p className="text-red-600 text-sm">{dniError}</p>}
        </div>


        <div className="sm:col-span-3">
          <label className="block text-black text-sm font-bold mb-2" htmlFor="username">
              Nombre de usuario
          </label>
            
            <div className='relative'>
              <span className="absolute inset-y-0 left-0 flex items-center pl-2 mt-2">
                  <img src="/src/assets/user.svg" alt="Lock icon" className="w-6 h-5"/>
              </span>

              <input className="shadow appearance-none border rounded w-full py-2 px-3 pl-10
              text-black leading-tight focus:outline-none focus:shadow-outline" id="username" type="text" 
              placeholder="username" name="username" required={true} defaultValue={userInfo.username}/>

              {usernameError && <p className="text-red-600 text-sm">{usernameError}</p>}

            </div>
        </div>


        <div className="sm:col-span-3">
          <label className="block text-black text-sm font-bold mb-2" htmlFor="email">
              Correo electrónico
          </label>
            
            
          <div className='relative'>
            <span className="absolute inset-y-0 left-0 flex items-center pl-2 mt-2">
                <img src="/src/assets/mail.svg" alt="Mail icon" className="w-6 h-6"/>
            </span>
              
            <input className="shadow appearance-none border rounded w-full py-2 px-3 pl-10
              text-gray-700 leading-tight focus:outline-none focus:shadow-outline" id="email" type="email" 
              placeholder="example@gmail.com" name="email" required={true} defaultValue={userInfo.email}/>
          </div>

          {emailError && <p className="text-red-600 text-sm">{emailError}</p>}
        </div>

      </div>


      <div className="flex flex-col items-center">
        {errorMessageRegister && <p className="text-red-700 font-bold">{errorMessageRegister}</p>}
        <br></br>
        <div className="mb-4">
          <button className="bg-sky-400 hover:bg-blue-400 text-white font-bold py-2 px-4 rounded-lg
            focus:outline-none focus:shadow-outline" type="submit">
          Actualizar
          </button>
        </div>
      </div>
      </form>            

      <button  className="px-4 py-2 text-white bg-sky-400 rounded-lg mt-7 hover:bg-blue-400 font-bold" 
        onClick={() => handleOpenModal(true)}>
        Actualizar contraseña
      </button>



      {showModal && (
        <>
        <div className="modal-backdrop" onClick={handleCloseModal} ></div>
          <div className="modal-container">
            <div className="bg-white p-8 rounded shadow transition duration-300 ease-in-out transform scale-100">
              <h2 className="text-2xl font-bold mb-4">Cambio de contraseña</h2>

              {!showChangePasswordForm && (
                <>

                <form onSubmit={handleVerifyCurrentPassword}>

                  <div className="sm:col-span-3">
                    <label
                      className="block text-black text-sm font-bold mb-2"
                      htmlFor="current_password" >
                      Contraseña actual
                    </label>

                    <input className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 mb-3 leading-tight 
                      focus:outline-none focus:shadow-outline" id="current_password" type="password" placeholder="***********"
                      value={currentPassword} onChange={(e) => setCurrentPassword(e.target.value)}/>
                      {errorCurrentPassword && <p className="text-red-600 text-sm">{errorCurrentPassword}</p>}
                  </div>

                  <div className="flex justify-center">

                    <button className="px-4 py-2 text-white bg-blue-500 rounded mt-2 hover:bg-blue-700" type='submit'>
                      Verificar contraseña actual
                    </button>
                  </div>
                </form>
                </>
      )}

      {showChangePasswordForm && (
        <>
        <form onSubmit={handleChangePassword}>
          <div className="sm:col-span-3">

            
            <label className="block text-black text-sm font-bold mb-2" htmlFor="password">
                Nueva contraseña
            </label>

            <div className='relative'>
              <span className="absolute inset-y-0 left-0 flex items-center pl-2 mt-2">
                  <img src="/src/assets/lock.svg" alt="Lock icon" className="w-6 h-5"/>
              </span>

              <input className="shadow appearance-none border rounded w-full py-2 px-3 pl-10 text-gray-700 mb-3 leading-tight 
              focus:outline-none focus:shadow-outline" id="password" type="password" placeholder="***********" 
              name="password" required={true}/>
              {passwordError && <p className="text-red-600 text-sm">{passwordError}</p>}

            </div>

          </div>

          <div className="sm:col-span-3">
            <label className="block text-black text-sm font-bold mb-2" htmlFor="password2">
                Repita la contraseña
            </label>

            <input className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 mb-3 leading-tight 
            focus:outline-none focus:shadow-outline" id="password2" type="password" placeholder="***********" 
            name="password2" required={true}/>
            {password2Error && <p className="text-red-600 text-sm">{password2Error}</p>}

          </div>

          <div className="flex justify-center">

            <button className="px-4 py-2 text-white bg-blue-500 rounded mt-2 hover:bg-blue-700" type='submit'>
              Cambiar contraseña
            </button>
          </div>
        </form>
        </>
      )}

                            
            </div>
          </div>
        </>
        )}

    </div>

    
  </>
  );
};