import React, { useRef, useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom';
import { FilePond } from 'react-filepond';
import 'filepond/dist/filepond.min.css';
import api from '../api/api'
import jwtDecode from 'jwt-decode';

export const CreateAnnouncement = () => {

  const navigate = useNavigate();

  
  // Obtener opciones para reglas, servicios y tipo de inmueble desde la API

  const [rulesOptions, setRulesOptions] = useState([]);
  const [servicesOptions, setServicesOptions] = useState([]);
  const [propertyTypeOptions, setPropertyTypeOptions] = useState([]);


  useEffect(() => {
    async function getData() {
      const rulesResponse = await fetch(`/api/rules/`);
      const dataRules = await rulesResponse.json();
      setRulesOptions(dataRules);
  
      const servicesResponse = await fetch(`/api/services/`);
      const dataServices = await servicesResponse.json();
      setServicesOptions(dataServices);

      const propertyTypeResponse = await fetch(`/api/properties/types`);
      const dataPropertyType = await propertyTypeResponse.json();
      setPropertyTypeOptions(dataPropertyType);
      
    }
  
    getData();
  }, []);


  const[errorMessageRegisterProp, setErrorMessageRegisterProp] = useState(null)
  
  const [titleError, setTitleError] = useState(null);
  const [localizationError, setLocalizationError] = useState(null);
  const [priceError, setPriceError] = useState(null);
  const [typeError, setTypeError] = useState(null);
  const [dormitoriesError, setDormitoriesError] = useState(null);
  const [sizeError, setSizeError] = useState(null);
  const [bathsError, setBathsError] = useState(null);

  const [rulesError, setRulesError] = useState(null);
  const [servicesError, setServicesError] = useState(null);
  const [photosError, setPhotosError] = useState(null); //errores del array photoIds


  const [photoPostError, setPhotoPostError] = useState(null);

  const [uniqueTogetherError, setUniqueTogetherError] = useState(null);




  const handleSubmit = async (event) => {
    event.preventDefault();

    const files = pond.current.getFiles();
    

    const token = localStorage.getItem('jwtToken');
    const decoded = jwtDecode(token);
    const userId = decoded.user_id;


    


    //realizar peticion post para subir las fotos asociadas, para despues pasar los ids a la peticion de property
    const photoIds = [];

    setPhotoPostError(null)
    for (const file of files) {

      if (!file.file.type.startsWith('image/')) {
        setPhotoPostError('Solo puede subir imágenes')
      }
      const formDataPhoto = new FormData();
      formDataPhoto.append('photo', file.file);
      formDataPhoto.append('owner', userId);
    
      const token = localStorage.getItem('jwtToken');
      const responsePhoto = await api.post('/api/photos/', formDataPhoto, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      const photoId = responsePhoto.data.id;
      photoIds.push(photoId);
    }


    const selectedRuleIds = Array.from(event.target.elements.rules)
    .filter((checkbox) => checkbox.checked)
    .map((checkbox) => checkbox.value);

    const selectedServiceIds = Array.from(event.target.elements.services)
    .filter((checkbox) => checkbox.checked)
    .map((checkbox) => checkbox.value);
  
    

    //peticion de property
    const formData = new FormData();

    photoIds.forEach(photoId => {
      formData.append('photos', photoId);
    });

    formData.append('title', event.target.title.value);
    formData.append('localization', event.target.localization.value);
    formData.append('price', event.target.price.value);
    formData.append('type', event.target.type.value);
    formData.append('dormitories', parseInt(dormitoriesValue) || 1);
    formData.append('size', event.target.size.value);

    if (hasPrivateBathroomOption) {
      const privateBathroomValue = event.target.privateBathroom.value;
      if (privateBathroomValue === 'yes') {
        formData.append('baths', 1);
      } else {
        formData.append('baths', 0);
      }
      
    } else {
      formData.append('baths', parseInt(event.target.baths.value));
    }

    formData.append('owner', userId);

    if(selectedRuleIds.length > 0){
      selectedRuleIds.forEach((ruleId) => {
        formData.append('rules', ruleId);
      });
    }
    if(selectedServiceIds.length > 0){
      selectedServiceIds.forEach((serviceId) => {
        formData.append('services', serviceId);
      });
    }


    setTitleError(null);
    setLocalizationError(null);
    setPriceError(null);
    setTypeError(null);
    setDormitoriesError(null);
    setSizeError(null);
    setBathsError(null);
    setRulesError(null);
    setServicesError(null);
    setPhotosError(null);
    setErrorMessageRegisterProp(null);
    setUniqueTogetherError(null);



    try {

      const token = localStorage.getItem('jwtToken');
      
      const response = await api.post('/api/properties/', formData, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      if (event.target.type.value == "------"){
        setTypeError('Eliga un tipo de inmueble válido');
      }
      navigate('/announcements');


    } catch (error) {
      
      if (error.response && error.response.data) {
        

          if (error.response.data.title) {
            setTitleError(error.response.data.title[0]);
          }
          if (error.response.data.localization) {
            setLocalizationError(error.response.data.localization[0]);
          }
          if (error.response.data.price) {
            setPriceError(error.response.data.price[0]);
          }
          if (error.response.data.type) {
            setTypeError(error.response.data.type[0]);
          }
          if (error.response.data.dormitories) {
            setDormitoriesError(error.response.data.dormitories[0]);
          }
          if (error.response.data.size) {
            setSizeError(error.response.data.size[0]);
          }
          if (error.response.data.baths) {
            setBathsError(error.response.data.baths[0]);
          }
          if (error.response.data.owner) {
            setOwnerError(error.response.data.owner[0]);
          }

          if (error.response.data.rules){
            setRulesError(error.response.data.rules[0])
          }
          if (error.response.data.services){
            setServicesError(error.response.data.services[0])
          }
          if (error.response.data.photos){
            setPhotosError(error.response.data.photos[0])
          }

          if (isNaN(dormitoriesValue)){
            setDormitoriesError('El valor de este campo debe ser un número');
          }

          if (error.response.data.non_field_errors) {
            let message = error.response.data.non_field_errors[0];
            message = message.replace('Los campos', 'Ya existe una propiedad con esa combinación de');
            message = message.replace('localization', 'dirección');
            message = message.replace('type', 'tipo');
            message = message.replace('price, ', 'precio y ');
            message = message.replace('size', 'tamaño');
            message = message.replace('deben formar un conjunto único', '');
            

            setUniqueTogetherError(message);
          }


      } else {
        setErrorMessageRegisterProp('Ocurrió un error al intentar publicar el inmueble.');
      }
    }

  }



  const pond = useRef();


  const [isReadOnly, setIsReadOnly] = useState(false);
  const [hasPrivateBathroomOption, setHasPrivateBathroomOption] = useState(false);
  const [dormitoriesValue, setDormitoriesValue] = useState('');



  const handleTypeChange = (event) => {
    const selectedType = event.target.value;
    setFirstDropdownValue(selectedType);
    if (selectedType === 'Habitacion' || selectedType === 'Cama') {
      setIsReadOnly(true);
      if (selectedType === 'Habitacion') {
        setHasPrivateBathroomOption(true);
      } else {
        setHasPrivateBathroomOption(false);
      }
    } else {
      setIsReadOnly(false);
      setHasPrivateBathroomOption(false);
    }
  }
  



  useEffect(() => {
    if (isReadOnly) {
      setDormitoriesValue(1);
      
    }
    else{
      setDormitoriesValue('');
    }
  }, [isReadOnly]);




  const [privateBathroom, setPrivateBathroom] = useState('no');


  const [bathsValue, setBathsValue] = useState('');
  const [firstDropdownValue, setFirstDropdownValue] = useState('------');

  useEffect(() => {
    if (firstDropdownValue === 'Habitacion') {
      if (privateBathroom === 'yes') {
        setBathsValue(1);
      } else if (privateBathroom === 'no') {
        setBathsValue(0);
      }
    } 
    else if (firstDropdownValue === 'Cama') {
      setBathsValue(0);
    }

    else if (firstDropdownValue === 'Inmueble completo' || firstDropdownValue === 'valorPorDefecto') {
    // permitir que el usuario actualice el valor del campo de baños manualmente
      setBathsValue('');
    }


  }, [firstDropdownValue, privateBathroom]);

  return (
    <>
    <br></br>
    <br></br>
    <br></br>
    <br></br>


    <div className='flex items-center justify-center bg-cover bg-no-repeat bg-center h-full'>
      <div className="w-full max-w-2xl border-4 border-solid border-white-50 rounded-20 backdrop-blur-lg">

        <div className='mt-5'>
                
            
        
          <form className="bg-transparent border-solid border-white rounded px-8 py-30 pt-6 pb-8 mb-4" onSubmit={handleSubmit}>
            <div className="mt-10 grid grid-cols-1 gap-x-6 gap-y-8 sm:grid-cols-6">

              
              
            

              <div className="sm:col-span-4">
                <label className="block text-black text-sm font-bold mb-2" htmlFor="title">
                    Título
                </label>

                <input className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight 
                focus:outline-none focus:shadow-outline" id="title" type="text" 
                placeholder="Habitación en el centro de Madrid" name="name" required={true}/>
                {titleError && <p className="text-red-600 text-sm">{titleError}</p>}
              </div>


              <div className="sm:col-span-4">
                <label className="block text-black text-sm font-bold mb-2" htmlFor="localization">
                    Dirección
                </label>

                <input className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight 
                focus:outline-none focus:shadow-outline" id="localization" type="text" placeholder="Calle XXX, número 3" name="localization"
                required={true}/>
                {localizationError && <p className="text-red-600 text-sm">{localizationError}</p>}
              </div>




              <div className='sm:col-span-4 flex flex-col'>
                <label className="block text-black text-sm font-bold mb-2" htmlFor="localization">
                    Imágenes
                </label>
                <FilePond credits={false} allowMultiple={true} ref={pond} labelIdle='Arrastra tus imagenes aquí o 
                <span class="filepond--label-action">seleccionalas</span> desde tu dispositivo' required={true}/>
                {photosError && <p className="text-red-600 text-sm">{photosError}</p>}
                {photoPostError && <p className="text-red-600 text-sm">{photoPostError}</p>}
              </div>




              <div className="sm:col-span-3">
                <label className="block text-black text-sm font-bold mb-2" htmlFor="price">
                    Precio (€/mes)
                </label>

                <input className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight 
                focus:outline-none focus:shadow-outline" id="price" type="text" placeholder="150" name="price"
                required={true}/>
                {priceError && <p className="text-red-600 text-sm">{priceError}</p>}
              </div>


              <div className="sm:col-span-3">

                <label htmlFor="type" className="block text-black text-sm font-bold mb-2">
                    Tipo de inmueble
        
                </label>

                <div className="mt-2">
                  <select id="type" name="type" defaultValue="valorPorDefecto" autoComplete="type-name" className="block w-full 
                  rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:ring-2 pl-3
                  focus:ring-inset focus:ring-indigo-600 sm:max-w-xs sm:text-sm sm:leading-6" required={true} 
                  onChange={handleTypeChange}>

                    <option value="valorPorDefecto">------</option>
                    {propertyTypeOptions.map((option) => (
                      <option key={option} value={option}>
                        {option}
                      </option>
                    ))}
                  </select>
                  {typeError && <p className="text-red-600 text-sm">{typeError}</p>}
                </div>
              </div>




              <div className="sm:col-span-2">
                <label className="block text-black text-sm font-bold mb-2" htmlFor="dormitories">
                    Número de dormitorios
                </label>

                <input className= {`shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight 
                focus:outline-none focus:shadow-outline ${isReadOnly ? 'bg-gray-300' : ''}`} id="dormitories" type="text" 
                placeholder="2" name="dormitories" required={true} readOnly={isReadOnly} value={isReadOnly ? 1 : dormitoriesValue}
                onChange={(event) => setDormitoriesValue(event.target.value)}/>
                {dormitoriesError && <p className="text-red-600 text-sm">{dormitoriesError}</p>}
              </div>


              <div className="sm:col-span-2">
                <label className="block text-black text-sm font-bold mb-2" htmlFor="baths">
                  Número de baños
                </label>
                <input className={`shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight 
                focus:outline-none focus:shadow-outline ${isReadOnly ? 'bg-gray-300' : ''}`} id="baths" type="text" 
                placeholder="1" name="baths" required={true} readOnly={isReadOnly} value={bathsValue} 
                onChange={(event) => setBathsValue(event.target.value)}/>
                {bathsError && <p className="text-red-600 text-sm">{bathsError}</p>}
              </div>
              

              {hasPrivateBathroomOption && (
                <div className="sm:col-span-3">
                  <label className="block text-black text-sm font-bold mb-2" htmlFor="privateBathroom">
                    ¿Tiene baño privado?
                  </label>
                  <select id="privateBathroom" name="privateBathroom" className='block w-full 
                  rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:ring-2 pl-3
                  focus:ring-inset focus:ring-indigo-600 sm:max-w-xs sm:text-sm sm:leading-6 animate-highlight'
                  onChange={(event) => setPrivateBathroom(event.target.value)} value={privateBathroom}>
                    <option value="no">No</option>
                    <option value="yes">Sí</option>
                  </select>
                  
                </div>
              )}


              <div className="sm:col-span-2">
                <label className="block text-black text-sm font-bold mb-2" htmlFor="size">
                    Tamaño (en m2)
                </label>

                <input className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight 
                focus:outline-none focus:shadow-outline" id="size" type="text" placeholder="60" name="size"
                required={true}/>
                {sizeError && <p className="text-red-600 text-sm">{sizeError}</p>}
              </div>

              

              <div className='sm:col-span-3'> 
                <h3 className='text-black text-sm font-bold mb-2'>Seleccione las reglas deseadas</h3>
                {rulesOptions.map((option) => (
                <label key={option.id} className="mt-3 inline-flex items-center cursor-pointer">
                  <input type="checkbox" className="form-checkbox h-5 w-5 text-gray-600 cursor-pointer" value={option.id}
                  id="rules" name="rules" />
                  <span className="ml-2 bg-red-500 rounded-full px-3 py-1 text-sm font-semibold text-white
                   mr-2 flex items-center">
                    <img src="/src/assets/rule.svg" alt="Rule icon" className="w-5 h-5 mr-1"/>
                    {option.name}</span> 
                </label>
                ))}
                {rulesError && <p className="text-red-600 text-sm">{rulesError}</p>}
              </div>



              <div className='sm:col-span-3'> 
                <h3 className='text-black text-sm font-bold mb-2'>Seleccione los servicios de su inmueble</h3>
                {servicesOptions.map((option) => (
                <label key={option.id} className="mt-3 inline-flex items-center cursor-pointer min-w-[13rem]">
                  <input type="checkbox" className="form-checkbox h-5 w-5 text-gray-600 cursor-pointer" value={option.id}
                  id="services" name="services" /> 
                  <span className="ml-2 bg-green-500 rounded-full px-3 py-1 text-sm font-semibold text-white
                   mr-2 flex items-center">
                    <img src="/src/assets/check-service.svg" alt="Check-Service icon" className="w-5 h-5 mr-1"/>
                    {option.name}</span>
                </label>
                ))}
                {servicesError && <p className="text-red-600 text-sm">{servicesError}</p>}
              </div>



              
              
            </div>
            
            <br/>
            <div className="flex flex-col items-center">
                {errorMessageRegisterProp && <p className="text-red-600 text-sm">{errorMessageRegisterProp}</p>}
                {uniqueTogetherError && <p className="text-red-600 text-sm">{uniqueTogetherError}</p>}
                <br></br>
                <div className="mb-4">
                    <button className="bg-sky-400 hover:bg-sky-500 text-white font-bold py-2 px-4 rounded-lg
                      focus:outline-none focus:shadow-outline" type="submit">
                      Publicar
                    </button>
                </div>
            </div>

          </form>
            
        </div>

      </div>
    </div>
    </>
  );
}
