import React from "react";
import { Link, useLocation } from "react-router-dom";
import { useState, useEffect, useRef } from 'react';
import jwtDecode from 'jwt-decode';
import { DropdownMenu } from "./DropDown.jsx";
import { getUserInfo } from '../api/auth';

import { useContext } from 'react';
import { AuthContext } from '../api/AuthContext';


export function Navbar() {

  const location = useLocation();
  const { isLoggedIn, handleLogout, isOwner } = useContext(AuthContext);


  const [userInfo, setUserInfo] = useState(null);

  useEffect(() => {
    const storedUserInfo = localStorage.getItem('userInfo');
    if (storedUserInfo) {
      setUserInfo(JSON.parse(storedUserInfo));

    } else if (isLoggedIn) {

      const fetchUserInfo = async () => {
        const token = localStorage.getItem('jwtToken');
        const decoded = jwtDecode(token);
        const userId = decoded.user_id;

        const data = await getUserInfo(userId, token);
        setUserInfo(data);
        localStorage.setItem('userInfo', JSON.stringify(data));
      };
      fetchUserInfo();
    }
    
    return () => {
      localStorage.removeItem('userInfo');
      setUserInfo(null);
    };


  }, [isLoggedIn]);

  useEffect(() => {
    const handleProfilePhotoUpdate = (event) => {
      setUserInfo(prevUserInfo => ({
        ...prevUserInfo,
        photo: event.detail.photoUpdate
      }));
    };
  
    window.addEventListener('photoUpdate', handleProfilePhotoUpdate);
  
    return () => {
      window.removeEventListener('photoUpdate', handleProfilePhotoUpdate);
    };
  }, []);

  const [isOpen, setIsOpen] = useState(false);

  const menuRef = useRef(null);

  useEffect(() => {
    const handleClickOutside = event => {
      if (menuRef.current && !menuRef.current.contains(event.target)) {
        setIsOpen(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, [menuRef]);


  return (
    
      <nav className="flex items-center justify-between flex-wrap bg-gradient-to-r from-blue-700 to-blue-300 p-6 w-full 
      fixed top-0 left-0 z-10">
        <div className="flex items-center flex-shrink-0 text-white mr-6">
          <Link to="/"><img className="md:h-full md:w-52" src="/Logo.png"/></Link>
      
        </div>
       
        <div className="w-full block flex-grow lg:flex lg:items-center lg:w-auto">
          <div className="text-sm lg:flex-grow flex space-x-8">
            <Link to="/" className={`text-gray-300 hover:bg-gray-700 hover:text-white rounded-md px-2 py-2 text-sm
             font-medium mr-4
              ${
                location.pathname === '/' ? 'bg-gray-700' : ''
              }`}>
              Home
            </Link>


            <Link to='/announcements' className={`text-gray-300 hover:bg-gray-700 hover:text-white rounded-md px-2 py-2 
               text-sm font-medium mr-4 ${
                location.pathname === '/announcements' ? 'bg-gray-700' : ''
              }`}>
                
              Anuncios
            </Link>

            {isLoggedIn && isOwner ? (
              <Link to='/createAnnouncement' className={`text-gray-300 hover:bg-gray-700 hover:text-white rounded-md px-2
               py-2 text-sm font-medium mr-4 ${
                location.pathname === '/createAnnouncement' ? 'bg-gray-700' : ''
              }`}>
                
              Publicar anuncio
            </Link>

            ):(
              <></>
            )}

          </div>

          
            {isLoggedIn ? (
              <div className="mr-8 mb-10">
                <span className="absolute inset-y-0 left-0 flex items-center pl-2 mt-2">
                    <img src="/src/assets/bell.svg" alt="Lock icon" className="w-6 h-6"/>
                </span>
              </div>

            ):(
              <></>
            )}



            {isLoggedIn ? (
              <div className="ml-5" ref={menuRef}>
              <DropdownMenu userInfo={userInfo} isOpen={isOpen} setIsOpen={setIsOpen}>
                <span className="absolute inset-y-0 left-0 flex items-center pl-2 mt-2">
                  <img src="/src/assets/user.svg" alt="Lock icon" className="w-6 h-5"/>
                </span>

                
                <Link to="/userProfile" className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100
                 hover:text-blue-800 rounded-t-md pl-10" onClick={() => setIsOpen(false)}>Mi perfil</Link>



                {isOwner ? (
                  
                  <>
                  <span className="absolute inset-y-0 left-0 flex items-center pl-2 mt-2">
                  <img src="/src/assets/euro.svg" alt="Lock icon" className="w-6 h-5"/>
                  </span>

                  <Link to="/yourAnnouncements" className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100
                  hover:text-blue-800 rounded-t-md pl-10" onClick={() => setIsOpen(false)}>Mis anuncios</Link>
                 </>
                ):(
                  <></>

                )}
                



                <span className="absolute inset-y-0 left-0 flex items-center pl-2 mt-2">
                  <img src="/src/assets/logout.svg" alt="Lock icon" className="w-6 h-5"/>
                </span>
                
                <Link to="/" onClick={handleLogout} nocloseonclick="true" className={`block px-4 py-2 text-sm text-gray-700 
                hover:bg-gray-100 hover:text-blue-800 pl-10 rounded-b-md
                ${
                  location.pathname === '/' ? '' : ''
                }`}>
                  Cerrar sesión
              </Link>
              </DropdownMenu>
            </div>
              
            ):(

              
              <Link to="/loginForm" className={`inline-block text-sm font-medium px-4 py-2 leading-none border rounded
               text-black border-black hover:border-transparent hover:text-teal-700 hover:bg-white mt-4 lg:mt-0
                border-width: 5px
                ${
                  location.pathname === '/loginForm' ? 'bg-black text-teal-700' : ''
                }`}>
              Iniciar sesión
            </Link>

            )}

            {isLoggedIn ? (
              <div className="flex items-center">
                <span className="ml-3">{userInfo?.username}</span>
              </div>
            ) : (
              <></>
            )}


        </div>
      </nav>

  );
}