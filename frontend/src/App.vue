<template>
  <div id="app">
    <header>
      <nav class="navbar">
        <div class="logo">
          <h1>Ticket System</h1>
        </div>
        <ul class="nav-links" >
          <template v-if="!isAuthenticated">
            <router-link to="/"><li><a href="/"><v-btn variant="text" color="">Inicio</v-btn></a></li></router-link>
            <router-link to="/Contact"><li><a href="/"><v-btn variant="text" color="">Contactanos</v-btn></a></li></router-link>
            <router-link to="/About"><li><a href="/"><v-btn variant="text" color="">Nosotros</v-btn></a></li></router-link>
          </template>
          <template v-else>
            <router-link to="/InicioUser"><li><a href="/"><v-btn variant="text" color="">Inicio</v-btn></a></li></router-link>
            <router-link to="/AccountsUserList" ><li><a href="/"><v-btn variant="text" color="">Cuentas</v-btn></a></li></router-link>
            <router-link to="/ClienteList"><li><a href="/"><v-btn variant="text" color="">Clientes</v-btn></a></li></router-link>
            <router-link to="/TiqueList"><li><a href="/"><v-btn variant="text" color="">Tiques</v-btn></a></li></router-link>
            <router-link to="/Contact"><li><a href="/"><v-btn variant="text" color="">Contacto</v-btn></a></li></router-link>
            <router-link to="/About"><li><a href="/"><v-btn variant="text" color="">Nosotros</v-btn></a></li></router-link>
          </template>
        </ul>
        <ul class="sesions-links">
          <template v-if="!isAuthenticated">
            <router-link to="/Login"><li><a href=""><v-btn variant="text" color="primary">Login</v-btn></a></li></router-link>
          </template>
          <template v-else>
            <router-link to="/AccountUser"><li><a href=""><v-btn variant="text">Account </v-btn></a></li></router-link>
            <a href="" @click.prevent="logOut"><v-btn variant="outlined" color="error">Log Out</v-btn></a>
          </template>
        </ul>
      </nav>
    </header>
    <main>
        <router-view></router-view>
    </main>
    <footer class="footer">
      <p>&copy; 2024 Ticket System. Todos los derechos reservados.</p>
      <ul class="footer-links">
        <li><a >Política de Privacidad</a></li>
        <li><a >Términos y Condiciones</a></li>
      </ul>
      <ul class="footer-links">
        <li><a >Instagram</a></li>
        <li><a >facebook</a></li>
        <li><a >X</a></li>
      </ul>
    </footer>
  </div>
</template>

<script>
import About from './components/About.vue';
import Login from './components/Login-User.vue';
import RegisterUser from './components/Register-User.vue';
import AccountUser from './components/Account-User.vue';
import eventBus from './Services/eventBus';
import TiqueList from './components/Tique-List.vue';
import ClienteList from './components/Cliente-List.vue';
import AccountsUserList from './components/AccountsUser-List.vue';
import Contact from './components/Contact.vue';
import InicioUser from './components/Inicio-User.vue';


export default {
  name: 'app',
  components: {
    Contact,
    About,
    RegisterUser,
    Login,
    AccountUser,
    TiqueList,
    ClienteList,
    AccountsUserList,
    InicioUser,
  },
  data() {
    return {
      eventBusState: eventBus.state,  // Importamos el estado reactivo
    };
  },
  mounted() {
    this.checkAuthentication();  // Verificar si el usuario está autenticado al montar el componente
  },
  computed: {
    isAuthenticated() {
      return this.eventBusState.isAuthenticated;  // Computamos el valor de autenticación basado en el estado global
    },
  },
  methods: {
    checkAuthentication() {
      // Verifica si hay un token en el local storage (esto indica que el usuario está autenticado)
      const token = localStorage.getItem('access_token');
      this.eventBusState.isAuthenticated = !!token;  // Si hay token, se considera autenticado
    },
    logOut() {
      // Elimina el token del local storage y actualiza el estado
      localStorage.removeItem('access_token');
      localStorage.removeItem('ID_Account');
      localStorage.removeItem('Nombre');
      localStorage.removeItem('Grupo');
      localStorage.removeItem('Apellido');
      this.eventBusState.isAuthenticated = false;  // Actualiza el estado global
      this.$router.push('/Login');  // Redirige al login
    },
  },
};
</script>


<style>
@import 'vuetify/styles';
/* Estilos generales */
#app {
  display: flex;
  flex-direction: column;
  min-height: 100vh; /* Ocupa al menos toda la pantalla */
}

main {
  flex: 1; /* Hace que el contenido principal crezca y ocupe el espacio restante */
  padding: 20px;
  font-family: Verdana;
}

/* Header */
header {
  background-color: #333;
  color: white;
  padding: 10px 20px;
  border-bottom: 4px solid #017bab;
  position: relative;
}

.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.nav-links,
.sesions-links {
  display: flex;
  list-style-type: none;
  padding: 0;
  margin: 0;
}

.nav-links li,
.sesions-links li {
  margin: 0 10px;
}

.nav-links a,
.sesions-links a {
  color: white;
  text-decoration: none;
  font-weight: bold;
  padding: 5px 10px;
  transition: color 0.3s ease;
}



/* Footer */
.footer {
  background-color: #333;
  color: white;
  padding: 10px 20px;
  text-align: center;
  border-top: 4px solid #017bab;
  position: relative;
  
}

.footer-links {
  list-style-type: none;
  padding: 0;
  display: flex;
  justify-content: center;
  margin: 10px 0;
}

.footer-links li {
  margin: 0 10px;
}

.footer-links a {
  color: white;
  text-decoration: none;
  font-weight: bold;
  transition: color 0.3s ease;
}

.footer-links a:hover {
  color: #ddd; /* Efecto hover para los enlaces del footer */
}


/* Responsivo para pantallas más pequeñas */
@media (max-width: 768px) {
  .navbar {
    flex-direction: column;
    align-items: center;
  }

  .nav-links,
  .sesions-links {
    flex-direction: column;
    text-align: center;
    margin: 10px 0;
  }

  .nav-links li,
  .sesions-links li {
    margin: 5px 0;
  }

  .footer-links {
    flex-direction: column;
  }

  .footer-links li {
    margin: 5px 0;
  }
}

</style>




