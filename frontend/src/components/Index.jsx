import React from 'react'

export const Index = () => {
  return (
    <div className="flex flex-col items-center justify-center h-screen bg-gray-100">
      <h1 className="text-4xl font-bold mb-4">Bienvenido a Alquiler de Pisos para Estudiantes</h1>
      <p className="text-lg text-center mb-8">
        Encuentra el piso perfecto para ti y tus compañeros de estudio.
      </p>
      <button className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
        Ver pisos disponibles
      </button>
    </div>
  
  );
}
