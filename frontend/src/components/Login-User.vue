
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
        const response = await this.axios.post('http://localhost:8000/api/login/', payload); //obtiene los datos a travez del back y devuelve en una response
        console.log(response); 
  
        this.token = response.data.token;  //guardar token en una variable
        this.user_id = response.data.user_id;

        console.log(this.user_id)
        

        // Guardadado en local storage
        localStorage.setItem('access_token', this.token); //guarda el token en el local
        localStorage.setItem('ID_Account', this.user_id);
        eventBus.state.isAuthenticated = true;

        console.log('Token guardado:', this.token); 
        this.axios.defaults.headers.common['Authorization'] = `Token ${this.token}`; // guardar token en la cabezera
        this.$router.push({ name: 'AccountUser' }); // redireccion a account
        console.log(this.axios.defaults.headers.common['Authorization']); //verificar si token esta en la cabezera
      } catch (error) { //en caso de error de credenciales alertará al usuario
        if (error.response && error.response.status === 401) {
          
          this.errorMessage = error.response.data.error; // Captura el mensaje de error
          
          alert('La cuenta esta deshabilitada')
        } else {
          this.errorMessage = 'Error inesperado, por favor intenta nuevamente.';
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
