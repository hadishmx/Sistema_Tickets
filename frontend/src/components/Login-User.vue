
<template>
  <form @submit.prevent="login" class="form-login">
      <h5>Inicio de Sesion</h5>
      <input class="controls" type="text" name="usuario" value="" placeholder="Usuario" v-model="username" >
      <input class="controls" type="password" name="contrasena" value="" placeholder="Contraseña" v-model="password" >
      <v-btn variant="text" type="sumbit">Iniciar Sesion </v-btn>
      <p><a href="#">¿Olvidastes tu Contraseña?</a></p>

  </form>
</template>

<script >
import eventBus from '../Services/eventBus';

export default {
  name: "Login",
  data() {
    return { //datos a almacenar
      username: "",
      password: "",
      token: null, 
    };
  },
  methods: {
    async login() {
      var payload = {
        username: this.username,
        password: this.password,
      };
      
      try {
        const response = await this.axios.post('http://localhost:8000/login/', payload); //obtiene los datos a travez del back y devuelve en una response
        console.log(response); 
  
        this.token = response.data.token;  //guardar token en una variable
        this.user_id = response.data.user.id;
        this.Nombre = response.data.Nombre;
        this.Apellido = response.data.Apellido;
        this.Grupo = response.data.user.grupos[0].name;
        

        // Guardadado en local storage
        localStorage.setItem('access_token', this.token); //guarda el token en el local
        localStorage.setItem('ID_Account', this.user_id);
        localStorage.setItem('Nombre', this.Nombre);
        localStorage.setItem('Apellido', this.Apellido);
        localStorage.setItem('Grupo', this.Grupo);
        eventBus.state.isAuthenticated = true;

        console.log('Token guardado:', this.token); 
        this.axios.defaults.headers.common['Authorization'] = `Token ${this.token}`; // guardar token en la cabezera
        this.$router.push({ name: 'InicioUser' }); // redireccion a account
        console.log(this.axios.defaults.headers.common['Authorization']); //verificar si token esta en la cabezera
        console.log(response.data.error);
        } catch (error) { // en caso de error de credenciales alertará al usuario
        if (error.response) {
          // Manejar errores específicos según el estado
          if (error.response.status === 400) {
            // Capturar mensajes específicos de la API
            const errorMessage = error.response.data.error || 'Verifique Usuario y Contraseña';
            this.errorMessage = errorMessage; // Captura el mensaje de error
            alert(errorMessage);
          } else if (error.response.status === 401) {
            // Para cuentas inactivas
            this.errorMessage = error.response.data.error || 'Cuenta inactiva';
            alert(this.errorMessage);
          } else {
            // Otros errores
            this.errorMessage = 'Ocurrió un error inesperado. Por favor, inténtelo de nuevo.';
            alert(this.errorMessage);
          }
        } else {
          // Error no relacionado con la respuesta
          this.errorMessage = 'Error de red. Por favor, Intente mas tarde.';
          alert(this.errorMessage);
        }
        console.error('Error al iniciar sesión:', error);
      }
    },
  },
};

</script>

<style scoped>

.form-login {
  width: 400px;
  height: 340px;
  background: #4e4d4d;
  margin: auto;
  margin-top: 5rem;
  margin-bottom: 5rem;
  box-shadow: 7px 13px 37px #000;
  padding: 20px 30px;
  border-top: 4px solid #017bab;
  color: white;
  display: grid;
  border-radius: 5px;
  place-items: center;
}

.form-login h5 {
  margin: 0;
  text-align: center;
  width: 100%;
  height: 40px;
  margin-bottom: 30px;
  border-bottom: 1px solid;
  font-size: 20px;
}

.controls {
  width: 100%;
  border: 1px solid #017bab;
  margin-bottom: 15px;
  padding: 11px 10px;
  background: #252323;
  font-size: 14px;
  font-weight: bold;
  border-radius: 4px;
  color: white;
}

button {
  width: 10rem;
  height: 40px;
  background: #017bab;
  font-family: 'Segoe UI';
  
  border-radius: 4px;
  color: white;
  margin-bottom: 16px;
}

.form-login p{
  width: 100%;
  height: 40px;
  text-align: center;
  border-bottom: 1px solid;
}

.form-login a {
  color: white;
  text-decoration: none;
  font-size: 14px;
}

.form-login a:hover {
  text-decoration: underline;
}
</style>
