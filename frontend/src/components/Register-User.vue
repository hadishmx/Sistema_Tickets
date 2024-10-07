<template>
  <section class="form-register">
    
    <form @submit.prevent="Register">
    <!-- Paso 1: Registro de Cuenta -->
    <div>
      <h5>Registro de Cuenta</h5>
      
      <input class="controls" type="text" v-model="username" placeholder="Usuario">
      <input class="controls" type="password" v-model="password" placeholder="Contraseña">
      <input class="controls" type="password" v-model="repeatpassword" placeholder="Repetir Contraseña">
      <input class="controls" type="email" v-model="email" placeholder="Correo@gmail.com">
    </div>
    <div>
      <h5>Datos Personales</h5>
      <input class="controls" type="text" v-model="nombre" placeholder="Nombre">
      <input class="controls" type="text" v-model="apellido" placeholder="Apellido">
      <input class="controls" type="text" v-model="rut" placeholder="RUT">
    </div>
    <div>
      <div class="button-control">
        <v-btn variant="outlined" color="" type="submit">Crear</v-btn>
      </div>
    </div>
    </form>
  </section>
</template>

<script>
import axios from 'axios';

export default {
  name: 'RegisterUser',
  data() {
    return { //datos a almacenar
      username : "",
      password : "",
      repeatpassword : "",
      email :"",
      nombre : "",
      apellido : "",
      rut : "",
    };
  },
  methods: {
    async Register(){
      var data = {
        username: this.username,
        password: this.password,
        email: this.email,
        nombre: this.nombre,
        apellido: this.apellido,
        rut: this.rut,
        
      };
      console.log(data);


      try{
        const response = await this.axios.post('http://localhost:8000/register/', data); //obtiene los datos a travez del back y devuelve en una response
        console.log(response);
        

      } catch (error){
        console.log(error)
      }
    },
  }
};
</script>

<style scoped>



.form-register {
  width: 400px;
  height: 640px;
  background: #4e4d4d;
  margin: auto;
  margin-top: 5rem;
  margin-bottom: 5rem;
  box-shadow: 7px 13px 37px #000;
  padding: 20px 30px;
  border-top: 4px solid #017bab;
  color: white;
  border-radius: 5px;
  display: grid;
  place-items: center;
  
}

.form-register h5 {
  margin: 0;
  width: 100%;
  text-align: center;
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
  color: #017bab;
}

.button-control{
  display: flex;
  justify-content: center;
}



.form-register p{
  height: 40px;
  width: 100%;
  text-align: center;
  border-bottom: 1px solid;
}

.form-register a {
  color: white;
  text-decoration: none;
  font-size: 14px;
}

.form-register a:hover {
  text-decoration: underline;
}
</style>