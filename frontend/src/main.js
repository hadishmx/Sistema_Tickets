import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import axios from 'axios'
import VueAxios from 'vue-axios'

import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import 'vuetify/dist/vuetify.min.css';


// Crear una instancia de Axios con configuración personalizada
const axiosInstance = axios.create({
  baseURL: 'http://localhost:8000', // Cambia la URL base si es necesario
  headers: {
    'Content-Type': 'application/json',
  },
});

// Crear la instancia de Vuetify
const vuetify = createVuetify({
  components,
  directives,
  theme: {
    dark: true, // Habilita el tema oscuro globalmente
  },
})



// Añadir interceptor para incluir el token en cada petición si está disponible
axiosInstance.interceptors.request.use(config => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Token ${token}`;
  }
  return config;
}, error => {
  return Promise.reject(error);
});

const app = createApp(App).use(router).use(VueAxios, axiosInstance).use(vuetify);

// Definir axios globalmente
app.config.globalProperties.$axios = axiosInstance;

app.mount('#app');







