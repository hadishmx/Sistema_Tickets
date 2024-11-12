<template>
  <v-container class="about-section" max-width="800">
    <v-card class="pa-5" elevation="3">
      <v-card-title class="headline text-center">
        Sobre Nosotros
      </v-card-title>
      
      <v-divider class="my-4"></v-divider>
      
      <v-card-text class="about-text">
        En nuestra empresa, sabemos que la eficiencia en la gestión y resolución de problemas es clave para el éxito.
        Nuestro sistema de tickets permite a nuestro equipo responder de manera rápida y efectiva a las solicitudes de nuestros clientes.
        Con estadísticas detalladas y reportes en tiempo real, monitorizamos y gestionamos cada caso, asegurando una alta tasa de satisfacción y eficiencia.
      </v-card-text>

      <v-divider class="my-4"></v-divider>

      <router-link to="/Contact"><v-btn variant="text" color="">Trabaja con Nosotros</v-btn></router-link>
    </v-card>
  </v-container>
</template>

<script>
export default {
  name: 'About',
};
</script>

<style scoped>
.about-section {
  margin-top: 5rem;
  margin-bottom: 5rem;
}

.v-card-title {
  color: #017bab;
}

.about-text {
  font-size: 1.1rem;
  line-height: 1.6;
  color: #424242;
  text-align: center;
}
</style>

