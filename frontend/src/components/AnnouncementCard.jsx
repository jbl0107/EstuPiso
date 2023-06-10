import React from 'react'
import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { fetchRules, fetchPhotos } from '../api/properties';


export const AnnouncementCard = ({ announcement }) => {

  const [photos, setPhotos] = useState([]);
  const [currentPhotoIndex, setCurrentPhotoIndex] = useState(0);
  const [rules, setRules] = useState([]);



  useEffect(() => {
    fetchRules(announcement.id).then((data) => setRules(data));
    fetchPhotos(announcement.id).then((data) => setPhotos(data));
  }, []);


  const handleNextPhoto = () => {
    setCurrentPhotoIndex((currentPhotoIndex + 1) % photos.length);
  };

  const handlePrevPhoto = () => {
    setCurrentPhotoIndex(
      (currentPhotoIndex - 1 + photos.length) % photos.length
    );
  };


    return (
      
        <div className="p-4 border rounded-lg shadow-md">
        <div className="mb-2 relative">
          {photos.length > 0 && (
            <img src={'api/' + photos[currentPhotoIndex].photo} alt="Foto del inmueble" className="w-full rounded-lg mb-2 h-80"/>
          )}
          {photos.length > 1 && (
            <>
              <button onClick={handlePrevPhoto}
                className="absolute left-0 top-1/2 transform -translate-y-1/2 bg-gray-100 text-gray-700 p-2 rounded-full
                hover:bg-blue-300">
                &#x276E;
              </button>
              
              <button onClick={handleNextPhoto}
                className="absolute right-0 top-1/2 transform -translate-y-1/2 bg-gray-100 text-gray-700 p-2 rounded-full
                hover:bg-blue-300 ml-AnnouncementCard">
                &#x276F;
              </button>
            </>
          )}
        </div>

        <Link to={`/announcements/${announcement.id}`}>
          <h2 className="text-lg font-medium mb-2 hover:underline">{announcement.title}</h2>
        </Link>


        <p className="text-gray-700 mb-2">{announcement.type}</p>
        <p className="text-gray-700">{announcement.price}€</p>
        <br></br>

        {rules.length === 0 ? (
          <span className="inline-block bg-gray-200 rounded-full px-3 py-1 text-sm font-semibold text-gray-700 mr-2 mb-2">
            No hay reglas
          </span>

        ) : (

          rules.map((rule) => (
            <span key={rule.id} className="inline-block bg-red-500 rounded-full px-3 py-1 text-sm font-semibold
            text-white mr-2 mb-2">{rule.name}</span>
          ))
        )}

      </div>
    );
  };