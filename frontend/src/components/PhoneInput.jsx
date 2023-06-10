import { useState } from 'react';

export function PhoneInput({onPrefixChange, error, isUpdate, currentUserNumber}) {
  const [prefix, setPrefix] = useState('+34'); //se utiliza para actualizar estado interno del componente
  const [number, setNumber] = useState(isUpdate ? currentUserNumber : '');

  const prefixes = ['+1', '+44', '+33', '+34'];

  const handleNumberChange = (event) => {
    setNumber(event.target.value);
  }

  const handlePrefixChange = (event) => {
    setPrefix(event.target.value);
    onPrefixChange(event.target.value); //esto es necesario para notificar al componente padre (RegisterForm)
  }

  return (
    
    <div className='flex flex-col items-start'>

      <div className='relative'>
        <span className="absolute inset-y-0 left-0 flex items-center pl-2 mt-2 ml-16">
          <img src="/src/assets/phone.svg" alt="Mail icon" className="w-6 h-6"/>
        </span>
        
        <div className='flex'>
          
          <select value={prefix} onChange={handlePrefixChange} className='shadow border rounded w-full py-1 px-2
          text-gray-700 leading-tight focus:outline-none focus:shadow-outline prefNumber' style={{ width: '77px', height: '38px' }}>
            {prefixes.map(p => (
              <option key={p} value={p}>{p}</option>
            ))}
          </select>
          

          <input type="text" value={number} onChange={handleNumberChange} placeholder="687098123" id="telephone" name="telephone"
            className='shadow appearance-none border rounded w-full py-2 px-3 pl-10 text-gray-700 leading-tight focus:outline-none
            focus:shadow-outline'/>
        </div>
      </div>
      {error && <p className="text-red-700 font-bold">{error}</p>}
    </div>
    
    
    
  );
}