import api from './api';

export const fetchRules = async (id) => {
    try {
      const response = await fetch(`/api/properties/${id}/rules`);
      const data = await response.json();
      return data;
    } catch (error) {
      console.error('error:', error);
    }
};



export const fetchPhotos = async (id) => {
    try {
      const response = await fetch(`/api/properties/${id}/photos`);
      const data = await response.json();
      return data;
    } catch (error) {
      console.error('error:', error);
    }
};



export const fetchServices = async (id) => {
  try {
    const response = await fetch(`/api/properties/${id}/services`);
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('error:', error);
  }
};

export const fetchOwner = async (id) => {
  try {
    const response = await fetch(`/api/owners/${id}/public`);
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('error:', error);
  }
};


export const fetchOwnerStudent = async (id, token) => {
  try {
    const response = await api.get(`/api/owners/${id}/student`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    return response.data;
  } catch (error) {
    console.error('error:', error);
  }
};