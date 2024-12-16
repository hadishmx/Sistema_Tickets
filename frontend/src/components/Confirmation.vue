<template>
  <div>
    <div v-if="loading">Cargando resultado de la transacción...</div>
    <div v-else-if="result.status === 'success'">
      <h2>¡Transacción exitosa!</h2>
      <p>{{ result.message }}</p>
      <pre>{{ result.details }}</pre>
    </div>
    <div v-else-if="result.status === 'failed'">
      <h2>Transacción fallida</h2>
      <p>{{ result.message }}</p>
      <pre>{{ result.details }}</pre>
    </div>
    <div v-else-if="result.status === 'error'">
      <h2>Error al procesar la transacción</h2>
      <p>{{ result.message }}</p>
      <pre>{{ result.details }}</pre>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name:'Confirmation',
  data() {
    return {
      loading: true,
      result: {},
      token:null,
    };
  },
  methods: {
    async fetchTransactionResult(token) {
      console.log('Token enviado al backend:', token);

    }
  },
  created() {
    // Obtenemos los parámetros de la URL usando this.$route.query
    
  },
  mounted() {
    // Capturar los parámetros de la URL
    const status = this.$route.query.status;
    const message = this.$route.query.message;
    const token = this.$route.query.token;

    // Mostrar en consola
    console.log('Estado de la transacción:', status);
    console.log('Mensaje:', message);
    console.log('Token:', token);
  }
  
};
</script>

<style scoped>
h2 {
  color: #2e7d32;
}
</style>
