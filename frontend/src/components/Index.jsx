import React from 'react'
import { Carousel } from './Carousel';
import { Feature } from './functions';


const actualAdvantages = [
  { icon: '🏢', text: 'Publicar anuncios de inmuebles como propietario'},
  { icon: '📱', text: 'Ver el teléfono de los propietarios registrados'},
  
  
  
  

];

const proxAdvantages = [
  { icon: '🎓', text: 'Publicar anuncios de estudiantes'},
  { icon: ' 📝 ', text: 'Publicar experiencias sobre tus viajes'},
  { icon: '💬', text: 'Enviar y recibir mensajes'},
  { icon: '⭐️', text: 'Realizar valoraciones'},
]


export const Index = ( ) => {

  
    return (

      <>
      <br></br>
      <br></br>
      <br></br>
      <br></br>

      <div className="p-4 text-center">
        <div className='flex items-center justify-center'>
          <h1 className="text-2xl font-bold mb-4 ml-14">BIENVENIDO A</h1>
          <img src="./Logo.png" alt="Logo" className="h-16 mb-3"/>
        </div>
        <p className="mb-2 text-xl">Somos una página que ayuda a los estudiantes a buscar pisos.</p>
        <p className="mb-2 text-xl">Al registrarte, podrás disfrutar de las siguientes ventajas:</p>


      <div className="flex flex-wrap">
      {actualAdvantages.map((advantage) => (
        <div key={advantage.text} className="w-1/2 p-2">
          <Feature icon={advantage.icon} text={advantage.text} />
        </div>
      ))}
      </div>

      <p className="mb-2 text-xl mt-3 font-bold">Proximamente:</p>
      <div className="flex flex-wrap">
      {proxAdvantages.map((advantage) => (
        <div key={advantage.text} className="w-1/2 p-2">
          <Feature icon={advantage.icon} text={advantage.text} />
        </div>
      ))}
      </div>



        <Carousel/>
      </div>


      

      




      </>
      
    );
  };
  

