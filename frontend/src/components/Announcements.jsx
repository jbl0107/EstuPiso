import React from 'react'
import { AnnouncementCard } from './AnnouncementCard';
import { useState, useEffect } from 'react';


export const Announcements = () => {
  
  const [announcements, setAnnouncements] = useState([]);

  useEffect(() => {
    fetch('/api/properties/')
      .then((response) => response.json())
      .then((data) => setAnnouncements(data))
      .catch((error) => {
        
      });
  }, []);

  return (

    <>
    <br></br>
    <br></br>
    <br></br>
    <br></br>

    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4 text-center">Anuncios disponibles</h1>
      <div className="grid grid-cols-3 gap-4">
        {announcements.map((announcement) => (
          <AnnouncementCard key={announcement.id} announcement={announcement} />
        ))}
      </div>
    </div>
    </>
  )
}
