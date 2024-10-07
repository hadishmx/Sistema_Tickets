<template>
    
    <div class="Section-father" >
        <div class="Account-Title">
            <h1>Datos Personales</h1>
        </div>
        <section class="Display-info" >
            <section class="personal-info" >
                <h2>Nombre</h2>
                <h2>Apellido</h2>
                <h2>Correo</h2>
                <h2>RUT</h2>
                <h2>Fecha Nacimiento</h2>
                <h2>Teléfono</h2>
            </section>
            <section class="personal-info" v-if="Usuariodata && Usuariodata.length > 0">
                <h2>{{  Usuariodata[0].nombre || 'cargando..' }}</h2>
                <h2>{{  Usuariodata[0].apellido || 'cargando..' }}</h2>
                <h2>{{  Usuariodata[0].correo || 'cargando..' }}</h2>
                <h2>{{  Usuariodata[0].rut || 'cargando..' }}</h2>
                <h2>{{  Usuariodata[0].fecha_nacimiento || 'cargando..' }}</h2>
                <h2>{{  Usuariodata[0].telefono || 'cargando..' }}</h2>
            </section>
            <section class="Account-info" >
                <div class="Avatar-info" >
                    <img :src="getAvatarUrl(Usuariodata[0].avatar)" alt="Avatar Usuario" class="Avatar-user" v-if="Usuariodata && Usuariodata[0].avatar">
                    <img :src="EjemploEmoji" alt="" v-else class="Avatar-user">
                </div>
                <div class="Account-data" >
                    <div>
                        <h2>Usuario</h2> 
                        <h2>Rol</h2>
                    </div>
                    <div v-if="Usuariodata && Usuariodata.length > 0">
                        <h2>{{  Usuariodata[0].user || 'cargando..' }}</h2>
                        <h2>{{  Usuariodata[0].tipo || 'cargando..' }}</h2>
                    </div>
                </div>
            </section>
        </section>
    </div>
  </template>

<script>
import EjemploEmoji from '../assets/EjemploEmoji.jpg';
import axios from 'axios';
export default {
    
    name: 'AccountUser',
    data() {
        return {
            EjemploEmoji,
            Usuariodata: null,
        };
    },
    mounted() {
    this.obtenerDatosUsuario(); // Llamamos la función al montar el componente
    },
    methods: {
        async obtenerDatosUsuario() {
        try {
            const token = localStorage.getItem('access_token'); // Obtenemos el token del local storage
            const response = await axios.get('http://localhost:8000/api/Usuario/', {
            headers: {
                Authorization: `Token ${token}`, // token a la cabecera
            },
            });
            this.Usuariodata = Array.from(response.data); // Guardamos los datos del usuario
            console.log(this.Usuariodata)
        } catch (error) {
            console.error('Error al obtener los datos del usuario:', error);
        }
        },
        getAvatarUrl(avatar) {
        // Comprueba si el campo avatar contiene la URL completa o solo el nombre del archivo
        if (avatar) {
            if (avatar.startsWith('http')) {
            return avatar; // Si es una URL completa, la usa directamente
            } else {
            return `http://localhost:8000/profile/${avatar}`; // Construye la URL completa si es relativa
            }
        }
        return ''; // Devuelve una cadena vacía si no hay avatar
        },
    },
    
};

</script>
  
<style scoped>
.Section-father {
  width: 1000px;
  height: 600px;
  background: #4e4d4d;
  margin: auto;
  margin-top: 5rem;
  margin-bottom: 5rem;
  box-shadow: 7px 13px 37px #000;
  padding: 20px 30px;
  border-top: 4px solid #017bab;
  color: white;
  border-radius: 5px;
}
.Account-Title h1{
    text-align: center;
    text-decoration: underline;
    
}


.Display-info{
    display: flex;
    margin: 2rem;
    justify-content: space-between;
    padding: 5px;
}

h2{
    padding: 5px;
    font-size: 15px;
}
.Avatar-user{
    width: 300px;
    height: 300px;
    border-radius: 200px
}

.Account-data{
    display: flex;
    margin: 2rem;
    justify-content: space-between;
    padding: 5px;
}


</style>


