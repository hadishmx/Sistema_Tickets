<template>
    <div>
      <h1>Verificar Transacción</h1>
      <div v-if="estadoTransaccion">
        <p>Estado: {{ estadoTransaccion.status }}</p>
        <p>Monto: {{ estadoTransaccion.amount }}</p>
      </div>
      <p v-else>Cargando...</p>
    </div>
  </template>
  
  <script>
  import transbankAPI from '../Services/Axios'; // Importa tu configuración de Axios
  
  export default {
    name: 'Verificar',
    data() {
      return {
        estadoTransaccion: null,
      };
    },
    async mounted() {
      // Capturar token desde la URL
      const token = new URLSearchParams(window.location.search).get('token_ws');
      if (token) {
        try {
          // Verificar la transacción
          const response = await transbankAPI.put(`/rswebpaytransaction/api/webpay/v1.2/transactions/${token}`);
          this.estadoTransaccion = response.data; // Guardar el estado de la transacción
        } catch (error) {
          console.error('Error al verificar la transacción:', error.response?.data || error.message);
        }
      }
    },
  };
  </script>
  