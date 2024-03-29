import React, { useState } from 'react';
import { UserCircleIcon } from '@heroicons/react/24/solid'


export const DropdownMenu = ({ children, userInfo, setIsOpen, isOpen  }) => {
  
    const handleToggle = () => setIsOpen(!isOpen);

    
  
    return (
      <div className="relative">
        <button onClick={handleToggle} title='Desplegable'>
          {userInfo && userInfo.photo ? (
            <img className="h-12 w-12 rounded-full" src={'api/'+userInfo.photo} title='Foto de perfil'/>
          ) : (
            <UserCircleIcon className="h-12 w-12 text-gray-700" aria-hidden="true" />
          )}
        </button>
        {isOpen && (
        <div className="absolute right-4 mt-2 w-48 rounded-md shadow-lg bg-white ring-1 ring-black ring-opacity-5">
          {React.Children.map(children, child => {
            if (child.props.nocloseonclick) {
              return child;
            } else {
              return React.cloneElement(child, { onClick: () => setIsOpen(false) });
            }
          })}
        </div>
        )}
      </div>
    );
  };