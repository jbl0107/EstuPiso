import React from 'react'
import { useState, useEffect } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import { fetchRules, fetchPhotos, fetchServices, fetchOwner, fetchOwnerStudent } from '../api/properties';
import jwtDecode from 'jwt-decode';
import { UserCircleIcon } from '@heroicons/react/24/solid'

import { useContext } from 'react';
import { AuthContext } from '../api/AuthContext';
import api from '../api/api.js'


export const AnnouncementDetails = () => {


  const { isLoggedIn, handleLogout, isOwner } = useContext(AuthContext);


  const [property, setProperty] = useState(null);
  const { id } = useParams();

  const [owner, setOwner] = useState(null);


  const [photos, setPhotos] = useState([]);
  const [currentPhotoIndex, setCurrentPhotoIndex] = useState(0);

  const handleNextPhoto = () => {
    setCurrentPhotoIndex((currentPhotoIndex + 1) % photos.length);
  };

  const handlePrevPhoto = () => {
    setCurrentPhotoIndex(
      (currentPhotoIndex - 1 + photos.length) % photos.length
    );
  };




  const [rules, setRules] = useState([]);
  const [services, setServices] = useState([]);


  useEffect(() => {
    fetchRules(id).then((data) => setRules(data));
    fetchPhotos(id).then((data) => setPhotos(data));
    fetchServices(id).then((data) => setServices(data));
    if (property) {
      fetchOwner(property.owner).then((data) => setOwner(data));
    }
    
  }, [property]);

  


  useEffect(() => {
    fetch(`/api/properties/${id}`)
      .then((response) => response.json())
      .then((data) => setProperty(data));
  }, [id]);





  const [ownerStudent, setOwnerStudent] = useState(null);

  useEffect(() => {
    if (isLoggedIn) {
      (async () => {
        const token = localStorage.getItem("jwtToken");
        const decoded = jwtDecode(token);
        const userId = decoded.user_id;
  
        const userTypeResponse = await fetch(`/api/users/${userId}/type`);
        const userTypeData = await userTypeResponse.json();
  
        if (property) {
          if (userTypeData.userType === "student" || userTypeData.userType === "admin") {
            fetchOwnerStudent(property.owner, token).then((data) =>
              setOwnerStudent(data)
            );
          }
        }
      })();
    }
  }, [isLoggedIn, property]);


  let user_id;
  let token;
  if(isLoggedIn){
    token = localStorage.getItem('jwtToken');
    user_id = jwtDecode(token).user_id;
  }
  



  const[errorMessage, setErrorMessage] = useState(null);

  const navigate = useNavigate();
  const handleDelete = async (event) => {
    event.preventDefault();

    try {

      const token = localStorage.getItem('jwtToken');
      let response = await api.delete(`/api/properties/${property.id}`, {
      headers: {
        'Authorization': 'Bearer ' + token,
      }

      });
      navigate('/announcements');

    } catch(error) {

      setErrorMessage('Ocurrió un error al borrar el anuncio.');
    }
    

    
  }


  if (!property) {
    return <></>;
  }
  


  return (

    <>
    <br></br>
    <br></br>
    <br></br>
    <br></br>
 
    <div className="p-4">
    {photos.length > 0 && (
            <img src={'/api' + photos[currentPhotoIndex].photo} alt="Foto del inmueble" className="w-3/4 mx-auto rounded-lg mb-2 h-96"/>
          )}
          {photos.length > 1 && (
            <>
              <button onClick={handlePrevPhoto}
                className="absolute left-0 top-1/2 transform -translate-y-1/2 bg-sky-300 text-gray-700 p-2 rounded-full
                hover:bg-blue-400">
                &#x276E;
              </button>
              
              <button onClick={handleNextPhoto}
                className="absolute right-0 top-1/2 transform -translate-y-1/2 bg-sky-300 text-gray-700 p-2 rounded-full
                hover:bg-blue-400 ml-AnnouncementDetails">
                &#x276F;
              </button>
            </>
          )}

      
      <h2 className="text-lg font-medium mb-2">{property.title}</h2>
      
      <div className='p-4 border rounded-lg shadow-md'>
        <h2 className="text-lg font-medium mb-2">Detalles</h2>
        <div className="flex">
          <div>
            <p className="text-gray-700 mb-2">{property.type}</p>
            <p className="text-gray-700 mb-2">{property.price}€/mes</p>
            <p className="text-gray-700 mb-2">Tamaño: {property.size}m2</p>
            {property.type == 'Habitacion' ? (
              property.baths == 1 ? (
                <p className="text-gray-700 mb-2">Tiene baño privado</p>
              ):(
                <p className="text-gray-700 mb-2">No tiene baño privado</p>
              )
            ) : (
              property.type == 'Cama' ? (
                <></>
              ) : (
                <p className="text-gray-700 mb-2">Baños: {property.baths}</p>
              )
              
            )}


            {property.type == 'Habitacion' || property.type == 'Cama' ? (
              <></>
            ) : (
              <p className="text-gray-700 mb-2">Dormitorios: {property.dormitories}</p>
            )}
            
            <p className="text-gray-700 mb-2">Dirección: {property.localization}</p>
          </div>


          {isLoggedIn ? (
            isOwner ? (
              <div className="ml-96 self-center">
                {owner && <p className="text-gray-700 mb-2">Propietario: {owner.username}</p>}
                <p className="text-sky-600 mb-2">
                  ¿Quieres ver más información sobre el propietario o chatear con él?{" "}
                  <Link className="hover:underline" to="/registerForm">
                    Registrate como estudiante aquí
                  </Link>
                </p>
              </div>
            ) : (
              <div className="ml-96 self-center">
                <div className="max-w-sm p-4 border rounded-lg shadow-md">
                  {ownerStudent && (
                    <p className="text-gray-700 mb-2">
                      Datos del propietario
                      <span className="text-red-500"> {ownerStudent.username}</span>: <br />
                      {ownerStudent && ownerStudent.photo ? (
                        <img className="h-12 w-12 rounded-full" src={"/api" + ownerStudent.photo} />
                      ) : (
                        <UserCircleIcon className="h-12 w-12 text-gray-700" aria-hidden="true" />
                      )}
                      Nombre: <span className="text-red-500">{ownerStudent.name}</span>
                      <br />
                      Número de teléfono:{" "}
                      <span className="text-red-500">{ownerStudent.telephone}</span>
                      <br />
                    </p>
                  )}
                </div>
              </div>
            )
          ) : (
            <div className="ml-96 self-center">
              {owner && <p className="text-gray-700 mb-2">Propietario: {owner.username}</p>}
              <p className="text-sky-600 mb-2">
                ¿Quieres ver más información sobre el propietario o chatear con él?{" "}
                <Link className="hover:underline" to="/registerForm">
                  Registrate como estudiante aquí
                </Link>
              </p>
            </div>
          )}

        
            

            

      </div>
    </div>

      <hr className="my-4 border border-gray-300" />
      <h3 className="text-lg font-medium mb-2">Reglas</h3>
      {property.rules.length === 0 ? (
        <span className="inline-block bg-gray-200 rounded-full px-3 py-1 text-sm font-semibold text-gray-700 mr-2 mb-2">
          
          No hay reglas
        </span>

      ) : (

        rules.map((rule) => (
          <span key={rule.id}  className="inline-block bg-red-500 rounded-full px-3 py-1 text-sm font-semibold
           text-white mr-2 mb-2">
            
            <span className="flex items-center">
              <img src="/src/assets/rule.svg" alt="Rule icon" className="w-5 h-5 mr-2"/>
              { rule.name }
            </span>
          </span>
        ))
      )}


      <hr className="my-4 border border-gray-300" />
      <h3 className="text-lg font-medium mb-2">Servicios</h3>
      {property.services.length === 0 ? (
        <span className="inline-block bg-gray-200 rounded-full px-3 py-1 text-sm font-semibold text-gray-700 mr-2 mb-2">
          No hay servicios
        </span>

      ) : (

        services.map((service) => (
          <span key={service.id}  className="inline-block bg-green-500 rounded-full px-3 py-1 text-sm font-semibold
           text-white mr-2 mb-2">

            <span className="flex items-center">
              <img src="/src/assets/check-service.svg" alt="Check-Service icon" className="w-5 h-5 mr-2"/>
              {service.name}
            </span>  
          </span>
        ))
      )}
      
    </div>

    {isOwner && property.owner == user_id ? (
      <div className='flex justify-center mb-7'>
      <form onSubmit={handleDelete}>
        <button className="bg-red-500 hover:bg-red-600 text-white font-bold py-2 px-4 rounded-lg focus:outline-none
         focus:shadow-outline" type="submit">
          Eliminar
        </button>
        {errorMessage && <p className="text-red-600 font-bold">{errorMessage}</p>}
      </form>
    </div>
    ):(
      <></>
    )}
    
    </>
  );
};
