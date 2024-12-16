import axios from 'axios';

const transbankAPI = axios.create({
    baseURL: 'https://webpay3gint.transbank.cl/', // Cambia a producción cuando sea necesario
    headers: {
      'Tbk-Api-Key-Id': 'tu_api_key_id', // Reemplaza con tu API Key ID
      'Tbk-Api-Key-Secret': 'tu_api_key_secret', // Reemplaza con tu API Key Secret
      'Content-Type': 'application/json',
    },
  });
  
  export default transbankAPI;